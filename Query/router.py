from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Query.schames import eNodeBPageResponse
from app.database import get_db
from utils.token import validate_token
from .services import *

router = APIRouter(
    tags=["业务查询"],
    dependencies=[Depends(validate_token)]
)


#   基站 eNodeB 信息查询
@router.get('/query/eNodeB', response_model=eNodeBPageResponse)
async def get_eNodeBs(params: eNodeB_params = Depends(), db: Session = Depends(get_db)):
    return list_eNodeB(db, params)


#   基站 eNodeB 信息查询
@router.get('/query/Cell', response_model=CellPageResponse)
async def get_eNodeBs(params: Cell_params = Depends(), db: Session = Depends(get_db)):
    return list_Cell(db, params)


#   小区KPI指标信息查询
@router.get('/query/KPI', response_model=KPIResponse)
async def get_KPI(params: Kpi_params = Depends(),db: Session = Depends(get_db)):
    return query_Kpi(db, params)

#   todo PRB 信息统计与查询
