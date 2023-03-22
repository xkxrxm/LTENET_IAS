from fastapi import FastAPI, Depends

from .sql import models
from .sql.database import engine, SessionLocal
from .routers import basic, admin, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(basic.router)
app.include_router(admin.router)
app.include_router(user.router)



