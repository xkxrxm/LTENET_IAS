from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..sql import schemas, crud
from .basic import get_db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/userlist", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/activate/{userid}")
async def active_user(userid: str, db: Session = Depends(get_db)):
    try:
        crud.active_user(db, userid)
    except:
        raise HTTPException(status_code=400, detail="Activation failure!")
    else:
        return "Successful activation!"


@router.delete("/delete/{userid}")
async def delete_user(userid: str, db: Session = Depends(get_db)):
    try:
        crud.delete_user(db, userid)
    except:
        raise HTTPException(status_code=400, detail="Deletion failure!")
    return "Deleted successfully!"
