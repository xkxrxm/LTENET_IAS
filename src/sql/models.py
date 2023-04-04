from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, CheckConstraint, text
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
    SECTOR_NAME = Column(String, nullable=False)
    ENODEBID = Column(Integer)
    ENODEB_NAME = Column(String,  nullable=False)
    EARFCN = Column(Integer)
    PCI = Column(Integer)
    PSS = Column(Integer, server_default=text("G2 % 3"))
    SSS = Column(Integer, server_default=text("G2 // 3"))
    TAC = Column(Integer)
    VENDOR = Column(String)
    LONGITUDE = Column(Float,  nullable=False)
    LATITUDE = Column(Float)
    STYLE = Column(String)
    AZIMUTH = Column(Float,  nullable=False)
    HEIGHT = Column(Float)
    ELECTTILT = Column(Float)
    MECHTILT = Column(Float)
    TOTLETILT = Column(Float)
    CheckConstraint('PCI between 0 and 503',name="PCI_RANGE")
    CheckConstraint('LONGITUDE between -180 and 180',name="LONGITUDE_RANGE")
    CheckConstraint('LATITUDE between -90 and 90',name="LATITUDE_RANGE")

