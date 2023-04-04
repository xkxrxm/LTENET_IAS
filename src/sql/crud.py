from csv import reader

from sqlalchemy.orm import Session
from sqlalchemy import update, delete, insert

from . import models, schemas
from .database import Base
from .utils import get_password_hash


def get_user_by_username(db: Session, username: str) -> schemas.UserInDB:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserIn):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def active_user(db: Session, userid: str):
    db.begin()
    if not db.query(models.User).filter(models.User.username == userid).first():
        raise
    try:
        stmt = (
            update(models.User).where(models.User.username == userid).values(is_active=True)
        )
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()


def delete_user(db: Session, userid: str):
    if not db.query(models.User).filter(models.User.username == userid).first():
        raise
    try:
        stmt = (
            delete(models.User).where(models.User.username == userid)
        )
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()


def get_table_by_name(name: str):
    """根据表格名获取对应的表格模型对象"""
    tables = Base.metadata.tables
    if name in tables:
        return tables[name]
    else:
        raise ValueError(f"Table {name} not found.")


# 批量导入数据
def create_table(db: Session, csv_reader: reader, table_name: str):
    value_dict = []
    header = next(csv_reader)  # 获取csv文件的列名作为表头
    try:
        for row in csv_reader:
            # 将每一行转换为一个字典
            value_dict .append({header[i]: row[i] for i in range(len(row))})
        table = get_table_by_name(table_name)
        stmt = insert(table).values(value_dict)
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()  # 提交到数据库
