import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from auth import schemas, crud
from auth.crud import get_user_by_username
from auth.models import User
from auth.schemas import Token, UserOut
from utils.hash import password_verify
from utils.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, token_info

router = APIRouter(
    tags=["系统界面"],
)


@router.post("/register", response_model=schemas.UserOut)
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
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not password_verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    if not user.is_active:
        raise HTTPException(status_code=402, detail="用户未激活，请联系管理员")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    logging.info("获取token成功")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/info", response_model=UserOut)
async def get_info(db: Session = Depends(get_db), username=Depends(token_info)):
    me = db.query(User).filter(User.username == username).first()
    return me
