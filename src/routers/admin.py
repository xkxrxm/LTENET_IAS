import csv

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os

from ..sql import schemas, crud
from .basic import get_db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

UPLOAD_DIR = "./uploads"  # 文件上传目录


@router.get("/user_list", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/activate/{userid}")
async def active_user(userid: str, db: Session = Depends(get_db)):
    try:
        crud.active_user(db, userid)
    except:
        raise HTTPException(status_code=400, detail="Activation failure!")
    else:
        return "Successful activation!"


@router.delete("/delete/{userid}")
async def delete_user(userid: str, db: Session = Depends(get_db)):
    try:
        crud.delete_user(db, userid)
    except:
        raise HTTPException(status_code=400, detail="Deletion failure!")
    return "Deleted successfully!"

# 批量导入数据的接口
@router.post("/database/upload/{tablename}")
async def create_upload_file(tablename: str, db: Session = Depends(get_db), file: UploadFile = File(...)):
    data = await file.read()  # 获取上传的csv文件数据
    data_str = data.decode("utf-8")  # 将csv文件数据处理为字符串类型，方便后面的处理
    csv_reader = csv.reader(data_str.splitlines(), delimiter=',')  # csv reader
    try:
        crud.create_table(db, csv_reader, tablename)
    except ValueError as e:
        raise
    return {"filename": file.filename}
