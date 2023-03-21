from sqlalchemy.orm import Session

from . import models, schemas

# ͨ��id��ѯ�����û�
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ͨ��Email��ѯ�����û�
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# ��ѯ����û�
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# ʹ���������ݴ���һ�� SQLAlchemy ģ��ʵ����
# ʹ��add������ʵ��������ӵ��������ݿ⡣
# ʹ��commit�������ݿ�������ύ���Ա㱣�����ǣ���
# ʹ��refresh��ˢ���������ݿ�ʵ�����Ա��������������ݿ���κ������ݣ��������ɵ� ID����
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ��ѯ�����Ŀ
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item