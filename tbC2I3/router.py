from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import engine
from tbC2I3.schemas import tbC2i3Out, tbC2Inew
from utils.token import validate_token

router = APIRouter(
    tags=["主邻小区C2I干扰分析 和 重叠覆盖干扰小区三元组分析"],
    dependencies=[Depends(validate_token)]
)


@router.get("/c2i3")
async def get_c2i3(x: float):
    stmt = text("SELECT * FROM tbc2i3 WHERE tbc2i3.x >= :inx")
    stmt = stmt.bindparams(inx=x)
    result = engine.connect().execute(stmt).fetchall()
    data = [tbC2i3Out(**dict(zip(["CEll_A", "CEll_B", "CEll_C", "x"], i))) for i in result]
    return {'count': len(data), "data": data}


@router.get("/c2inew")
async def get_tbC2Inew(min_num: int):
    stmt = text("SELECT * FROM tbc2inew WHERE tbc2inew.num >= :in_num")
    stmt = stmt.bindparams(in_num=min_num)
    result = engine.connect().execute(stmt).fetchall()
    data = [tbC2Inew(**dict(zip(["SCELL", "NCELL", "C2I_Mean", "Std", "PrbC2I9", "PrbABS6", "num"], i))) for i in
            result]
    return {'count': len(data), "data": data}
