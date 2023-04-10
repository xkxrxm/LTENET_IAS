import logging
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from .sql import models, crud, schemas
from .sql.database import engine, SessionLocal
from .routers import basic, admin, user, token

models.Base.metadata.create_all(bind=engine)

# 设置debug等级
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')


app = FastAPI()

app.include_router(basic.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(token.router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def root_init():
    db = SessionLocal()
    if not crud.get_user_by_username(db, username="root"):
        crud.ceate_root(db=db)
        logging.info("创建root用户成功")
    db.close()
