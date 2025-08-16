from .database import  pbp_collection
from typing import List
from schemas import Action

def pltime_to_sec(x: str) -> int:
    """
    Parse a string in MM:SS format into total seconds.
    Example: "12:34" -> 754
    """
    s = str(x).strip()
    if ":" not in s:
        return 0
    m, ss = s.split(":")
    return int(m) * 60 + int(ss)

async def insert_actions(parsed: dict[str,dict[str, str]], championship_id: int): 
    #count_mongo = await pbp_collection.count_documents({"Game": parsed["gameinfo"][0]["Game"], "championship": championship_name})
    #actions_to_process =parsed["actions"][count_mongo:]
    actions_to_process =parsed["actions"]
    for action in actions_to_process:
        action["championship"] = championship_id
        action["Time"] = pltime_to_sec(action["PLTime"])
        exists = await pbp_collection.find_one({
            "Game": action["Game"],
            "championship": action["championship"],
             "Time": action["Time"],
            "Team": action["Team"],
            "Name": action["Name"],
            "Nr": action["Nr"],
            "Text": action["Text"]
        })
        if not exists:
            try:
                await pbp_collection.insert_one(action)
            except Exception as e:
                print(f"Insertion of one of the actions failed:", e)

async def checker (match_id:str, championship_id: int)->bool:
    if await pbp_collection.find_one({"Game": match_id, "championship": championship_id}):
        return True
    else:
        return False

async def action_page(match_id:str, page_no:int,championship_id:id)-> List [Action]:
    skip_count = (page_no - 1) * 5
    cursor = pbp_collection.find({"Game": str(match_id),"championship" : championship_id}).sort("Time", -1).skip(skip_count).limit(5)
    results = await cursor.to_list(length=5)
    return [Action(**r) for r in results]