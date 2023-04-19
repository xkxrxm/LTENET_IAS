import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth.crud import root_init
from auth.router import router as auth_router
from UserManage.router import router as user_router
from DataManage.router import router as data_router
from app.database import generate_tables, SessionLocal

app = FastAPI()

app.include_router(auth_router)
app.include_router(data_router)
app.include_router(user_router)

generate_tables()


@app.on_event("startup")
async def init():
    db = SessionLocal()
    root_init(db=db)


@app.get('/')
async def toweb():
    return RedirectResponse('/docs')


# 项目程序的入口
if __name__ == '__main__':
    uvicorn.run(app=app)