import csv
import logging
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session

from utils.database import get_db
from utils.token import validate_token_admin
from crud.data_update import create_table_by_batch
from schemas import schemas
from schemas.schemas import UploadTask
from utils.data import upload_dict, batch, str2schemas
from utils.hash import convert_excel_to_csv

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
        await crud.active_user(db=db, userid=userid)
    except:
        raise HTTPException(status_code=400, detail="Activation failure!")
    else:
        return "Successful activation!"


@router.delete("/delete/{userid}")
async def delete_user(userid: str, db: Session = Depends(get_db)):
    try:
        await delete_user(db=db, userid=userid)
    except:
        raise HTTPException(status_code=400, detail="Deletion failure!")
    return "Deleted successfully!"


def upload_data_background(csvfile: str, task_id: str, table_name: str, db: Session):
    try:
        cur = 1
        with open(csvfile, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fifty_rows in batch(iter(reader), 50):
                to_update = list()
                for i in fifty_rows:
                    try:
                        cur += 1
                        # time.sleep(0.1)
                        # 数据清洗：从要插入的记录中删除不满足约束条件的项,主要靠validator实现
                        t = str2schemas(table_name=table_name, **i)
                        to_update.append(t.dict())
                    except Exception as e:
                        upload_dict[task_id].failed += 1
                        upload_dict[task_id].failed_msg.append(
                            {
                                "line": cur,
                                "msg": e
                            }
                        )
                    finally:
                        upload_dict[task_id].processed += 1
                try:
                    create_table_by_batch(db=db, table_name=table_name, values_batch=to_update)
                except Exception as e:
                    raise e
    except Exception as e:
        raise e
    finally:
        f.close()
        # 删除临时文件
        os.remove(csvfile)
        upload_dict[task_id].done = True


# 批量导入数据的接口
@router.post("/database/upload/{table_name}")
async def upload_file(table_name: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                      file: UploadFile = File(...)):
    task_id = uuid.uuid4().hex
    temp_csv = task_id + ".csv"
    if file.filename.endswith(".xlsx"):
        # 暂存文件
        with open(file.filename, 'wb') as f:
            f.write(await file.read())
        f.close()
        # 将文件转换问csv文件
        convert_excel_to_csv(file.filename, temp_csv)
        # 删除临时文件
        os.remove(file.filename)

    elif file.filename.endswith(".csv"):
        # 暂存文件
        with open(temp_csv, 'wb') as f:
            f.write(await file.read())
        f.close()
    # 创建一个UploadTask记录当前任务的状态
    upload_dict[task_id] = UploadTask(task_id=task_id)
    try:
        # 注意： 加入到background_tasks中的任务一定不要是 async
        background_tasks.add_task(upload_data_background, csvfile=temp_csv, task_id=task_id, table_name=table_name,
                                  db=db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="上传失败")
    return {"task_id": task_id, "url": f"admin/upload/status?task_id={task_id}"}


@router.get("/upload/status")
def upload_status(task_id: str):
    logging.info(upload_dict)
    if task_id in upload_dict:
        return upload_dict[task_id]
    raise HTTPException(status_code=404, detail="Item not found")
