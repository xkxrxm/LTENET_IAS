import csv
from openpyxl import load_workbook

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
@router.post("/database/upload/{table_name}")
async def create_upload_file(table_name: str, db: Session = Depends(get_db), file: UploadFile = File(...)):
    values_dict = []
    if file.filename.endswith(".csv"):
        data = await file.read()  # 获取上传的csv文件数据
        data_str = data.decode("utf-8")  # 将csv文件数据处理为字符串类型，方便后面的处理
        csv_reader = csv.reader(data_str.splitlines(), delimiter=',')  # csv reader
        header = next(csv_reader)
        for row in csv_reader:
            # 将每一行转换为一个字典
            values_dict .append({header[i]: row[i] for i in range(len(row))})
    elif file.filename.endswith(".xlsx"):
        with open(file.filename, 'wb') as f:
            f.write(await file.read())
        workbook = load_workbook(file.filename)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            values_dict.append(row_dict)
    try:
        crud.create_table(db, values_dict, table_name)
    except Exception as e:
        raise HTTPException(410, detail="failed")
    finally:
        os.remove(file.filename)
    return {"filename": file.filename}
