from fastapi import APIRouter, Depends

from app.database import get_db
from utils.token import validate_token
from .services import *

router = APIRouter(
    tags=["业务查询"],
    dependencies=[Depends(validate_token)]
)


#   基站 eNodeB 信息查询
@router.get('/query/eNodeB', response_model=ListResponse)
async def get_eNodeBs(params: eNodeB_params = Depends(), db: Session = Depends(get_db)):
    return list_eNodeB(db, params)


#   基站 eNodeB 信息查询
@router.get('/query/Cell', response_model=ListCellOut)
async def get_Cells(params: Cell_params = Depends(), db: Session = Depends(get_db)):
    return list_Cell(db, params)


#   小区KPI指标信息查询
@router.get('/query/KPI', response_model=ListResponse)
async def get_KPI(params: Kpi_params = Depends(), db: Session = Depends(get_db)):
    return query_Kpi(db, params)


# 查看取各PRB的噪声信息
@router.get('/query/PRB', response_model=ListResponse)
async def get_KPI(params: PRB_params = Depends(), db: Session = Depends(get_db)):
    return query_PRB(db, params)


# 获取小区名列表，供前端实现下拉列表使用
@router.get('/query/cell_name', response_model=ListResponse)
async def get_cell_name(db: Session = Depends(get_db)):
    return cell_name_list(db)


# 获取基站名列表，供前端实现下拉列表使用
@router.get('/query/ENodeB_name', response_model=ListResponse)
async def get_cell_name(db: Session = Depends(get_db)):
    return ENodeB_name_list(db)


