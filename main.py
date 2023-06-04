import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth.crud import root_init
from auth.router import router as auth_router
from UserManage.router import router as user_router
from DataManage.router import router as data_router
from Query.router import router as query_router
from interStruAnalysis.router import router as inter_router
from app.database import SessionLocal
from tbC2I3.router import router as c2irouter
from MRO.router import router as mro_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(data_router)
app.include_router(user_router)
app.include_router(query_router)
app.include_router(c2irouter)
app.include_router(inter_router)
app.include_router(mro_router)



@app.on_event("startup")
async def init():
    db = SessionLocal()
    root_init(db=db)


@app.get('/')
async def toweb():
    return RedirectResponse('/docs')


# 项目程序的入口
if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
# uvicorn main:app --reload --port=8080

