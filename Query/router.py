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

@router.get('/query/Cell', response_model=CellPageResponse)
async def get_eNodeBs(params: Cell_params = Depends(), db: Session = Depends(get_db)):
    return list_Cell(db, params)