from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["SupportBot"]
users = db["users"]


async def add_user(user_id: int):
    if not await users.find_one({"_id": user_id}):
        await users.insert_one({"_id": user_id})


async def get_users():
    data = []
    async for user in users.find():
        data.append(user["_id"])
    return data


async def get_user_count():
    return await users.count_documents({})
