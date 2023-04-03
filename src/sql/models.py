from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from typing import Optional

from .database import Base


class User(Base):
    __tablename__ = "User"

    username = Column(String, primary_key=True, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)


class TbCell(Base):
    __tablename__ = "tbCell"

    CITY = Column(String)
    SECTOR_ID = Column(String, primary_key=True)
    SECTOR_NAME = Column(String)
    ENODEBID = Column(Integer)
    ENODEB_NAME = Column(String)
    EARFCN = Column(Integer)
    PCI = Column(Integer)
    PSS = Column(Integer)
    SSS = Column(Integer)
    TAC = Column(Integer)
    VENDOR = Column(String)
    LONGITUDE = Column(Float)
    LATITUDE = Column(Float)
    STYLE = Column(String)
    AZIMUTH = Column(Float)
    HEIGHT = Column(Float)
    ELECTTILT = Column(Float)
    MECHTILT = Column(Float)
    TOTLETILT = Column(Float)
