from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from auth import schemas
from utils.token import validate_token_admin
from .services import *

router = APIRouter(
    prefix="/admin",
    tags=["用户管理"],
    # 这表示当请求到达路由之前，该依赖项必须被处理，即该依赖项的结果会在请求处理函数中作为参数被注入。
    dependencies=[Depends(validate_token_admin)]
)


@router.get("/user_list", response_model=list[schemas.UserOut])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/activate/{userid}")
async def activate(userid: str, db: Session = Depends(get_db)):
    try:
        active_user(db=db, userid=userid)
    except Exception as e:
        print(e)
        print("aaa")
        raise HTTPException(status_code=400, detail="Activation failure!")
    else:
        return "Successful activation!"


@router.delete("/delete/{userid}")
async def delete(userid: str, db: Session = Depends(get_db)):
    try:
        delete_user(db=db, userid=userid)
    except:
        raise HTTPException(status_code=400, detail="Deletion failure!")
    return "Deleted successfully!"
