import csv

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from openpyxl.reader.excel import load_workbook
from sqlalchemy.orm import Session
import os

from ..sql import schemas, crud
from .basic import get_db
from ..sql.utils import convert_excel_to_csv
from .token import validate_token_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # 这表示当请求到达路由之前，该依赖项必须被处理，即该依赖项的结果会在请求处理函数中作为参数被注入。
    dependencies=[Depends(validate_token_admin)]
)


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
    failed_lines = []
    if file.filename.endswith(".xlsx"):
        # 暂存文件
        with open(file.filename, 'wb') as f:
            f.write(await file.read())
        f.close()
        # 将文件转换问csv文件
        temp_csv = table_name + ".csv"
        convert_excel_to_csv(file.filename, temp_csv)
        # 逐行插入
        with open(temp_csv, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_dict = {k: v for k, v in row.items() if v}
                try:
                    crud.create_table_by_line(db, row_dict, table_name)
                except Exception as e:
                    failed_lines.append(e)
        f.close()
        # 删除临时文件
        os.remove(temp_csv)
        os.remove(file.filename)

    elif file.filename.endswith(".csv"):
        data = await file.read()  # 获取上传的csv文件数据
        data_str = data.decode("utf-8")  # 将csv文件数据处理为字符串类型，方便后面的处理

        csv_reader = csv.reader(data_str.splitlines(), delimiter=',')  # csv reader
        header = next(csv_reader)
        for row in csv_reader:
            row_dict = {header[i]: row[i] for i in range(len(row)) if row[i]}
            try:
                crud.create_table_by_line(db, row_dict, table_name)
            except Exception as e:
                failed_lines.append(e)

    if failed_lines:
        return HTTPException(410,detail=failed_lines)
    else:
        return {"filename": file.filename}
