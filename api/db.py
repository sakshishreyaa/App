import motor.motor_asyncio
import os 

from bson.objectid import ObjectId
from .env import MONGO as mongo_url

MONGO_URL = mongo_url

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.user

user_collection = database.get_collection("user_collection")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user["password"],
    }

# Add a new user into the database or replace if already exists
async def add_user(user_data: dict) -> dict:
    user = await user_collection.replace_one({"email":user_data["email"]},user_data,upsert=True)
    new_user = await user_collection.find_one({"email": user_data["email"]})
    return user_helper(new_user)


# Retrieve a user with a matching email and pass(signin)
async def retrieve_user(email: str,password:str) -> dict:
    user = await user_collection.find_one({"email": email,"password":password})
    if user:
        return user_helper(user)

# Check if user already  exists
# async def retrieve_usere(email: str) -> dict:
#     user = await user_collection.find_one({"email": email})
#     if user:
#         return user_helper(user)

# Retrieve all users
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users
