import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .crud import crud
from .models import models,tb
from app.utils.database import engine, SessionLocal
from .routers import basic, admin, user

models.Base.metadata.create_all(bind=engine)
tb.Base.metadata.create_all(bind=engine)

# 设置debug等级
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

app = FastAPI()

app.include_router(basic.router)
app.include_router(admin.router)
app.include_router(user.router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def root_init():
    db = SessionLocal()
    if not crud.get_user_by_username(db, username="root"):
        crud.create_root(db=db)
        logging.info("创建root用户成功")
    db.close()
