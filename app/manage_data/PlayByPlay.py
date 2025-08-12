from .database import  pbp_collection
from typing import List
from schemas import Action

async def insert_actions(parsed: dict[str,dict[str, str]], championship_id: int): 
    #count_mongo = await pbp_collection.count_documents({"Game": parsed["gameinfo"][0]["Game"], "championship": championship_name})
    #actions_to_process =parsed["actions"][count_mongo:]
    actions_to_process =parsed["actions"]
    for action in actions_to_process:
        action["championship"] = championship_id
        exists = await pbp_collection.find_one({
            "Game": action["Game"],
            "championship": action["championship"],
            "Team": action["Team"],
            "Name": action["Name"],
            "Nr": action["Nr"],
            "Text": action["Text"],
            "PLTime": action["PLTime"]
        })
        if not exists:
            try:
                await pbp_collection.insert_one(action)
            except Exception as e:
                print(f"Insertion of one action failed:", e)

async def checker (match_id:str, championship_id: int)->bool:
    if await pbp_collection.find_one({"Game": match_id, "championship": championship_id}):
        return True
    else:
        return False

async def action_page(match_id:str, page_no:int,championship_id:id)-> List [Action]:
    skip_count = (page_no - 1) * 5
    cursor = pbp_collection.find({"Game": str(match_id),"championship" : championship_id}).sort("_id", -1).skip(skip_count).limit(5)
    results = await cursor.to_list(length=5)
    return [Action(**r) for r in results]