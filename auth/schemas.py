from typing import Optional

from pydantic import BaseModel


# User基类
class UserBase(BaseModel):
    username: str


# User请求数据模型
class UserIn(UserBase):
    password: str


# User响应数据模型
class UserOut(UserBase):
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


# User业务数据模型
class UserDB(UserOut):
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    expires_in: int = 0


