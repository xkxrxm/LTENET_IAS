from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from crud.crud import get_user_by_username
from utils.database import get_db
from schemas.schemas import TokenData
import logging

# 定义token相关配置
SECRET_KEY = "SECRET KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 表示access token的过期时间为30分钟。

# OAuth2密码授权流程，获取access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# 创建access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证access token
async def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> bool:
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 检查用户名是否有效
        username = payload.get("sub")
        exp = payload.get("exp")
        if username is None or exp is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        # 检测token时间戳
        logging.info(exp)
        if exp is not None:
            # fromtimestamp 是 Python datetime 模块中的一个类方法，
            # 它用于将 Unix 时间戳（从 1970 年 1 月 1 日零点开始计算的秒数）转换为日期时间对象。
            exp_datetime = datetime.fromtimestamp(exp)
            logging.info(exp_datetime)
            if exp_datetime < datetime.now():
                raise HTTPException(status_code=401, detail="Token has expired")
        token_data = TokenData(username=username)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user.is_admin


# 对于管理员用户，需要检查管理员权限
async def validate_token_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_admin = await validate_token(token=token, db=db)
    if not is_admin:
        raise HTTPException(status_code=401, detail="Permission denied")
