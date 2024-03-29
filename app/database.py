from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE

# @param echo :是否打开sql语句执行的info信息
engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_tables():
    Base.metadata.create_all(bind=engine)
