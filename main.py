import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from crud import crud
from models import models, tb
from utils.database import engine, SessionLocal
from routers import user, admin, basic

models.Base.metadata.create_all(bind=engine)
tb.Base.metadata.create_all(bind=engine)

# 设置debug等级
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

app = FastAPI()

app.include_router(basic.router)
app.include_router(admin.router)
app.include_router(user.router)

# 挂载静态文件
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def root_init():
    db = SessionLocal()
    if not crud.get_user_by_username(db, username="root"):
        crud.create_root(db=db)
        logging.info("创建root用户成功")
    db.close()

@app.get('/')
def toweb():
    return RedirectResponse('/docs')

# 项目程序的入口
if __name__ == '__main__':
    uvicorn.run(app=app)