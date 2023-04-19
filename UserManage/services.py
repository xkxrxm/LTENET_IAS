from sqlalchemy.orm import Session
from sqlalchemy import update, delete

from auth.models import User


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def active_user(db: Session, userid: str):
    # 这么写是错误的：如果在下面的if语句成立，这个事务就无法被提交或者回滚
    # db.begin()
    if not db.query(User).filter(User.username == userid).first():
        print("bb")
        raise
    try:
        stmt = (
            update(User).where(User.username == userid).values(is_active=True)
        )
        db.execute(stmt)
    except Exception as e:
        print("cc")
        print(e)
        db.rollback()
        raise e
    else:
        db.commit()


def delete_user(db: Session, userid: str):
    if not db.query(User).filter(User.username == userid).first():
        raise
    try:
        stmt = (
            delete(User).where(User.username == userid)
        )
        db.execute(stmt)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()