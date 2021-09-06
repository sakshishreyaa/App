from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.db import (
    add_user,
    retrieve_user,
    retrieve_users,
    # retrieve_usere,
)
from api.models.user import (
    UserModel,
    ResponseModel,
)


router = APIRouter()

@router.post("/signup", response_description="Successfully creted account")
async def signup(user: UserModel ):
    user = jsonable_encoder(user)
    
    # user = await retrieve_usere(user["email"])
    # if user:
    #     return ResponseModel(user, "email already exists")
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.post("/signin", response_description="User data retrieved")
async def get_user_data(email:str,password:str):
    user = await retrieve_user(email,password)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "incorrect email or password")

@router.get("/get_all", response_description="User data retrieved")
async def get_all_users():
    user = await retrieve_users()
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "incorrect email or password")
