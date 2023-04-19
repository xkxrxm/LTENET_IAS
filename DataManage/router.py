import uuid
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import RedirectResponse
from starlette.responses import StreamingResponse

from app.database import get_db
from utils.token import validate_token_admin, validate_token
from .schemes import UploadTask
from .services import *

router = APIRouter(
    tags=["数据管理"]
)


# 批量导入数据的接口
@router.post("/database/upload/{table_name}")
async def upload_file(
        table_name: str,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        file: UploadFile = File(...),
        _=Depends(validate_token_admin)):
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
    return RedirectResponse(url="admin/upload/status?task_id="+task_id)


@router.get("/upload/status")
def upload_status(task_id: str):
    logging.info(upload_dict)
    if task_id in upload_dict:
        return upload_dict[task_id]
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/download/{filename}")
async def download_file(
        filename: str,
        _=Depends(validate_token)):
    # 读取文件内容
    with open(filename, "rb") as f:
        contents = f.read()

    # 构造响应对象，设置文件内容和Content-Disposition Header
    response = StreamingResponse(BytesIO(contents))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response
