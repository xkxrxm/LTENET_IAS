from io import BytesIO

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from app.utils.token import validate_token

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(validate_token)]
)


@router.get("/database/download/{filename}")
async def download_file(filename: str):
    # 读取文件内容
    with open(filename, "rb") as f:
        contents = f.read()

    # 构造响应对象，设置文件内容和Content-Disposition Header
    response = StreamingResponse(BytesIO(contents))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response
