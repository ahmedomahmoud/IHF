from database import db
import motor.motor_asyncio
import asyncio 
import json
from parser import parse_cp_file

class Action:
    def __init__(self, GameID, TeamName, PlayerName, PlayerNumber, Text, TimeStamp):
        self.GameID = GameID
        self.TeamName = TeamName
        self.PlayerName = PlayerName
        self.PlayerNumber = PlayerNumber
        self.Text = Text
        self.TimeStamp = TimeStamp

    def to_dict(self):
        return {
            "GameID": self.GameID,
            "TeamName": self.TeamName,
            "PlayerName": self.PlayerName,
            "PlayerNumber": self.PlayerNumber,
            "Text": self.Text,
            "TimeStamp": self.TimeStamp
        }


async def action_insertion(parsed: dict[str,dict[str, str]]):
    collection=db["PlayByPlay"]
    for action in parsed["actions"]:
        action_obj = Action(
            action["Game"],
            action["Team"],
            action["Name"],
            action["Nr"],
            action["Text"],
            action["PLTime"]
        )
        await collection.insert_one(action_obj.to_dict())


parsed=parse_cp_file("01.CP")
asyncio.run(action_insertion(parsed))

async def show_all_documents():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://saraandlilly557:ynvpAPvcsi45pIGT@projectihf.lyjlazt.mongodb.net/")
    db = client["PlayByPlay"]
    collection=db["PlayByPlay"]

    async for document in collection.find():
        print(document)

asyncio.run(show_all_documents()) 
