from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db

from utils.token import validate_token

router = APIRouter(
    tags=["MRO数据解析"]
)


def mro_parse(file_path: str, db: Session):
    pass  # todo 实现对mro文件的解析


@router.post("/mro")
async def get_mro(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        _=Depends(validate_token),
):
    with open(file.filename, 'wb') as f:  # 暂存文件
        f.write(await file.read())
    f.close()
    background_tasks.add_task(mro_parse, file_path=file.filename, db=db)
    return {"detail": "上传成功"}
