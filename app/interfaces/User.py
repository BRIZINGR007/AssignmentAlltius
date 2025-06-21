from typing import TypedDict
from pydantic import BaseModel


class UserModelTH(TypedDict):
    userId: str
    email: str
    name: str
    password: str


class SignUp_PM(BaseModel):
    name: str
    email: str
    password: str


class Login_PM(BaseModel):
    email: str
    password: str
