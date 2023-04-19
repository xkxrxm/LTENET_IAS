from sqlalchemy.orm import Session

from auth import schemas, models
from utils.hash import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserIn):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def root_init(db: Session):
    if not get_user_by_username(db, username="root"):
        hashed_password = get_password_hash("123456")
        root = models.User(
            username="root",
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True)
        db.add(root)
        db.commit()
        db.refresh(root)
    db.close()
