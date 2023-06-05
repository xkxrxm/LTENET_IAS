from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
import xml.etree.ElementTree as et
from utils.token import validate_token

router = APIRouter(
    tags=["MRO数据解析"]
)





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

def mro_parse(file_path: str, db: Session) :
    tree = et.parse(file_path)
    for item in tree.findall('term'):
        a = item.find('timestamp').text
        b = item.find('servingsector').text
        c = item.find('interferingsector').text
        d = float(item.find('ltescrsrp').text)
        e = float(item.find('ltencrsrp').text)
        f = int(item.find('ltencearfcn').text)
        g = int(item.find('ltencpci').text)
        if g<0 or g>503 or d<0 or d>97 or e<0 or e>97 or b=='NULL' or c=='NULL' or f!=38400 :
            continue
        h = "insert into tbmrodata values('{}','{}','{}',{},{},{},{});".format(a, b, c, d, e, f, g)
        db.commit()
        db.begin()
        db.execute((text(h)))
        db.commit()
