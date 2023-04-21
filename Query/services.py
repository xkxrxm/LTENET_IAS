from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from DataManage.models import tbCell, tbKPI
from Query.schames import *


def list_eNodeB(db: Session, params: eNodeB_params):
    qcnt = db.query(func.count('*'))
    q = db.query(tbCell)
    conditions = []
    if params.ENODEBID:
        conditions.append(tbCell.ENODEBID == params.ENODEBID)
    if params.ENODEB_NAME:
        conditions.append(tbCell.ENODEB_NAME == params.ENODEB_NAME)
    cnt = qcnt.filter(*conditions).scalar()
    data = q.filter(*conditions).limit(params.size).offset((params.page - 1) * params.size)
    return {'count': cnt, 'list': data.all()}


def list_Cell(db: Session, params: Cell_params):
    qcnt = db.query(func.count('*'))
    q = db.query(tbCell)
    conditions = []
    if params.SECTOR_ID:
        conditions.append(tbCell.SECTOR_ID == params.SECTOR_ID)
    if params.SECTOR_NAME:
        conditions.append(tbCell.SECTOR_NAME == params.SECTOR_NAME)
    cnt = qcnt.filter(*conditions).scalar()
    data = q.filter(*conditions).limit(params.size).offset((params.page - 1) * params.size)
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
    cnt = len(data.all())

    return {'count': cnt, 'list': data.all()}