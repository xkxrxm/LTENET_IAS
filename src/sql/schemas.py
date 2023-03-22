from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    password: str


class User(UserBase):
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True
