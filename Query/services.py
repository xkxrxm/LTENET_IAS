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
    stmt = text("SELECT * FROM tbprbnew WHERE StartTime >= :StartTime AND StartTime <= :EndTime AND SECTOR_NAME = "
                ":SECTOR_NAME")
    if params.Mode == PRB_mode.perQuarter:
        stmt = text("SELECT * FROM tbprb WHERE StartTime >= :StartTime AND StartTime <= :EndTime AND SECTOR_NAME = "
                    ":SECTOR_NAME")
    stmt = stmt.bindparams(StartTime=str(params.StartTime), EndTime=str(params.EndTime), SECTOR_NAME=params.SECTOR_NAME)
    result = db.execute(stmt)
    data = [PRBOut(**dict(zip(["Time", "data"],
                              [str(i._mapping["StartTime"]), i._mapping["AvgNoise"+str(params.PRB)]]))) for i in result]
    return {'count': len(data), 'list': data}
