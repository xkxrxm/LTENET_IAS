import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..crud import crud
from ..schemas import schemas
from app.utils.database import get_db
from app.schemas.schemas import Token
from app.crud.crud import get_user_by_username
from ..utils.hash import password_verify

router = APIRouter(
    tags=["basic"],
)


@router.post("/register", response_model=schemas.User)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=401, detail="The user name or password is invalid")
    return crud.create_user(db=db, user=user)


# 登录并获取access token
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm是FastAPI中用于处理OAuth2 Password流程验证请求的专用请求体类。
    # 这个类的作用是从请求体中解析出用户名和密码，并将它们传递给后面的业务逻辑。
    db = next(get_db())
    user = await get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not password_verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    logging.info("获取token成功")
    return {"access_token": access_token, "token_type": "bearer"}
