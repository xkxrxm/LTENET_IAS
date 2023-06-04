from fastapi import APIRouter, Depends, HTTPException
import app.config as config

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


@router.get("/database/config")
async def get_database_config():
    return {
        "DB_partition": config.DB_partition,
        "DB_time": config.DB_time,
        "DB_buffer_size": config.DB_buffer_size
    }


@router.post("/database/modify")
async def modify_database_config(partition: str = r"D:\datas", time: int = 30, buffer_size: int = 1000):
    config.DB_partition = partition
    config.DB_time = time
    config.DB_buffer_size = buffer_size
    return {
        "DB_partition": config.DB_partition,
        "DB_time": config.DB_time,
        "DB_buffer_size": config.DB_buffer_size
    }


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
