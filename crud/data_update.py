import logging

from sqlalchemy.orm import Session

from utils.data import str2models
from utils.database import Base


def get_table_by_name(name: str):
    """根据表格名获取对应的表格模型对象"""
    tables = Base.metadata.tables
    # logging.info(tables)
    if name in tables:
        return tables[name]
    else:
        raise ValueError(f"Table {name} not found.")


def create_table_by_batch(db: Session, values_batch: list, table_name: str):
    for item in values_batch:
        try:
            record = str2models(table_name=table_name, **item)
            db.merge(record)
        except Exception as e:
            db.rollback()
            print(e)
            raise e
    db.commit()
    logging.info("插入成功")
