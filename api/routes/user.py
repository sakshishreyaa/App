import json
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.db import (
    add_user,
    retrieve_user,
    retrieve_users,
    retrieve_profile,
)
from api.redis_cache import redis_connection
from api.models.user import UserModel, ResponseModel, ErrorResponseModel


router = APIRouter()


@router.post("/signup", response_description="Successfully creted account")
async def signup(user: UserModel):
    user = jsonable_encoder(user)

    # user = await retrieve_usere(user["email"])
    # if user:
    #     return ResponseModel(user, "email already exists")
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.post("/signin", response_description="User data retrieved")
async def signin(email: str, password: str):
    user = await retrieve_user(email, password)
    if user:
        return ResponseModel(user, "signed in successfully")
    return ErrorResponseModel("An error occurred.", 404, "incorrect email or password")


@router.get("/get_all_users", response_description="User data retrieved")
async def get_all_users():
    user = await retrieve_users()
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "no data found")


@router.get("/get_user_profile", response_description="User data retrieved")
async def get_user_profile(email: str):
    redis_db = await redis_connection()
    cached_profile = redis_db.get(email)
    if cached_profile:
        return ResponseModel(
            json.loads(cached_profile), "User data retrieved successfully(c)"
        )
    user_profile_data = await retrieve_profile(email)
    if user_profile_data:
        redis_db.set(email, json.dumps(user_profile_data))
        return ResponseModel(user_profile_data, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, " user does not exist")
