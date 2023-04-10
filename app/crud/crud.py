from sqlalchemy.orm import Session
from sqlalchemy import update, delete, insert

from app.models import models
from app.schemas import schemas
from app.utils.database import Base
from app.utils.hash import get_password_hash


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


# 初始化root用户
def ceate_root(db: Session):
    hashed_password = get_password_hash("123456")
    root = models.User(
        username="root",
        hashed_password=hashed_password,
        is_active=True,
        is_admin=True)
    db.add(root)
    db.commit()
    db.refresh(root)


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
def create_table_by_file(db: Session, values_dict_list: list, table_name: str):
    try:
        table = get_table_by_name(table_name)
        stmt = insert(table).values(values_dict_list)
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()  # 提交到数据库


def create_table_by_line(db: Session, values_dict: dict, table_name: str):
    try:
        table = get_table_by_name(table_name)
        stmt = insert(table).values(values_dict)
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()  # 提交到数据库
