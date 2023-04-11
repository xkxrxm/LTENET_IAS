from typing import Optional

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


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    expires_in: int = 0


class UploadTask(BaseModel):
    task_id: str
    processed: int = 0
    failed: int = 0
    failed_msg: list = []
    done: bool = False
