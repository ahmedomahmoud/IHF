import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]

# Collections
user_collection = db["users"]
pbp_collection= db["PlayByPlay"] 

# Ensure indexes for frequently queried fields
pbp_collection.create_index([("match_id", -1), ("Time", -1)])
