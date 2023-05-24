import uuid
from io import BytesIO

from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks
from starlette.responses import StreamingResponse

from app.database import get_db
from utils.token import validate_token_admin, validate_token
from .schemes import TableIn, TableOut
from .services import *

router = APIRouter(
    tags=["数据管理"]
)


# todo: excel文件 插入或更新
# 批量导入数据的接口
@router.post("/database/upload/{table_name}")
async def upload_file(
        table_name: TableIn,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        _=Depends(validate_token_admin),
        db: Session = Depends(get_db),
        chunk_size: int = 50,
):

    with open(file.filename, 'wb') as f:    # 暂存文件
        f.write(await file.read())
    f.close()
    background_tasks.add_task(upload_data_background, file_path=file.filename, table_name=table_name,
                              chunk_size=chunk_size, db=db)

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
        df.to_csv(temp_csv, index=False)
        # 读取文件内容
        with open(temp_csv, "rb") as f:
            contents = f.read()
        # 构造响应对象，设置文件内容和Content-Disposition Header
        response = StreamingResponse(BytesIO(contents))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.value + ".csv")
    except Exception:
        raise
    finally:
        f.close()
        os.remove(temp_csv)
    return response
