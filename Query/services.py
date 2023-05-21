from sqlalchemy import text
from sqlalchemy.orm import Session

from DataManage.models import tbCell, tbKPI
from Query.schames import *


def list_eNodeB(db: Session, params: eNodeB_params):
    q = db.query(tbCell)
    conditions = []
    if params.ENODEBID:
        conditions.append(tbCell.ENODEBID == params.ENODEBID)
    if params.ENODEB_NAME:
        conditions.append(tbCell.ENODEB_NAME == params.ENODEB_NAME)
    data = q.filter(*conditions).limit(params.size).offset((params.page - 1) * params.size)
    cnt = data.count()
    return {'count': cnt, 'list': data.all()}


def list_Cell(db: Session, params: Cell_params):
    q = db.query(tbCell)
    conditions = []
    if params.SECTOR_ID:
        conditions.append(tbCell.SECTOR_ID == params.SECTOR_ID)
    if params.SECTOR_NAME:
        conditions.append(tbCell.SECTOR_NAME == params.SECTOR_NAME)
    data = q.filter(*conditions).limit(params.size).offset((params.page - 1) * params.size)
    cnt = data.count()
    return {'count': cnt, 'list': data.all()}


def query_Kpi(db: Session, params: Kpi_params):
    q = db.query(tbKPI)
    conditions = []
    if params.SECTOR_NAME:
        conditions.append(tbKPI.SECTOR_NAME == params.SECTOR_NAME)
    if params.StartTime:
        conditions.append(params.StartTime <= tbKPI.StartTime)
    if params.EndTime:
        conditions.append(tbKPI.StartTime <= params.EndTime)

    data = q.filter(*conditions)
    cnt = data.count()

    return {'count': cnt, 'list': data.all()}


def cell_name_list(db: Session):
    result = db.query(tbCell.SECTOR_NAME).all()
    data = [x[0] for x in result]
    return {'count': len(data), 'list': data}


def ENodeB_name_list(db: Session):
    result = db.query(tbCell.ENODEB_NAME).distinct().all()
    data = [x[0] for x in result]
    return {'count': len(data), 'list': data}


def query_PRB(db: Session, params: PRB_params):
    sql = f"SELECT StartTime,ENODEB_NAME,AVG(AvgNoise{params.PRB}) FROM " \
          f"{'tbprb' if params.Mode == PRB_mode.perQuarter else 'tbprbnew'} WHERE " \
          f"StartTime >= :StartTime AND StartTime <= :EndTime AND ENODEB_NAME = :ENODEB_NAME" \
          f" GROUP BY ENODEB_NAME,StartTime"
    stmt = text(sql)
    stmt = stmt.bindparams(StartTime=str(params.StartTime), EndTime=str(params.EndTime),
                           ENODEB_NAME=str(params.ENODEB_NAME))
    result = db.execute(stmt)
    data = [PRBOut(**dict(zip(["Time", "data"], [str(i[0]), i[2]]))) for i in result]
    return {'count': len(data), 'list': data}
