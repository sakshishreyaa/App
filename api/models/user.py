from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    fullname: str 
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Salki Sreya",
                "email": "ss@gmail.com",
                "password": "pass",
            }
        }


class UpdateUserModel(BaseModel):
    fullname: Optional[str] =None 
    email: Optional[EmailStr] =None
    password : Optional[str] =None
    dob : Optional[datetime] = None
    blood_group : Optional[str]=None

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Salki Sreya",
                "email": "ss@gmail.com",
                "password": "pass",
                "dob": datetime(1998, 11, 9),
                "blood_group": "O (+ve)",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}