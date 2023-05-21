import uuid
from io import BytesIO

from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks
from starlette.responses import StreamingResponse

from utils.token import validate_token_admin, validate_token
from .schemes import TableName, TableOut
from .services import *

router = APIRouter(
    tags=["数据管理"]
)


# 批量导入数据的接口
@router.post("/database/upload/{table_name}")
async def upload_file(
        table_name: TableName,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        _=Depends(validate_token_admin)):
    task_id = uuid.uuid4().hex
    temp_csv = task_id + ".csv"

    with open(temp_csv, 'wb') as f:
        f.write(await file.read())
    f.close()
    background_tasks.add_task(upload_data_background, csv_path=temp_csv, task_id=task_id, table_name=table_name,
                              chunk_size=50)

    return {"detail": "上传成功"}


@router.get("/download/{filename}")
async def download_file(
        filename: TableOut,
        _=Depends(validate_token)):
    sql = f"SELECT * FROM {filename.value}"
    df = pd.read_sql(sql, engine)
    task_id = uuid.uuid4().hex
    temp_csv = task_id + ".csv"
    try:
        df.to_csv(temp_csv)

        # 读取文件内容
        with open(temp_csv, "rb") as f:
            contents = f.read()

        # 构造响应对象，设置文件内容和Content-Disposition Header
        response = StreamingResponse(BytesIO(contents))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.value + ".csv")
    except Exception:
        raise
    finally:
        os.remove(temp_csv)
    return response
