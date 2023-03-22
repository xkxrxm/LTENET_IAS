from sqlalchemy.orm import Session
from sqlalchemy import update, delete

from . import models, schemas
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
    except:
        db.rollback()
        raise
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
    except:
        db.rollback()
        raise
    else:
        db.commit()
