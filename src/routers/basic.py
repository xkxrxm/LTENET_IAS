from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..sql import crud, schemas
from ..sql.database import SessionLocal
from ..sql.utils import password_verify

router = APIRouter(
    tags=["basic"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.User)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=401, detail="The user name or password is invalid")
    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.User)
async def login(data: schemas.UserIn, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=data.username)

    if not user.is_active:
        raise HTTPException(status_code=422, detail="User inactive")
    elif password_verify(data.password, user.hashed_password):
        return user
    else:
        raise HTTPException(status_code=410, detail="The username or password is incorrect!")
