import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class tbCellBase(BaseModel):
    CITY: str
    SECTOR_ID: str
    SECTOR_NAME: str
    ENODEBID: int
    ENODEB_NAME: str
    EARFCN: int
    PCI: int
    PSS: Optional[int]
    SSS: Optional[int]
    TAC: int
    VENDOR: str
    LONGITUDE: float
    LATITUDE: float
    STYLE: str
    AZIMUTH: float
    HEIGHT: Optional[float]
    ELECTTILT: Optional[float]
    MECHTILT: Optional[float]
    TOTLETILT: Optional[float]

    class Config:
        orm_mode = True

    @validator("PCI", pre=True)
    def PCI_validator(cls, value):
        value = int(value)
        if value < 0 or value > 503:
            raise ValueError("Invalid PCI")
        return value

    @validator("LONGITUDE", pre=True)
    def LONGITUDE_validator(cls, value):
        if value is None:
            raise ValueError("Invalid LONGITUDE")
        value = float(value)
        if value < -180 or value > 180:
            raise ValueError("Invalid LONGITUDE")
        return value

    @validator("LATITUDE", pre=True)
    def LATITUDE_validator(cls, value):
        if value is None:
            raise ValueError("Invalid LATITUDE")
        value = float(value)
        if value < -90 or value > 90:
            raise ValueError("Invalid LATITUDE")
        return value


class tbKPI(BaseModel):
    StartTime: str
    ENODEB_NAME: str
    SECTOR_DESCRIPTION: str
    SECTOR_NAME: str
    RCCConnSUCC: int
    RCCConnATT: int
    RCCConnRATE: Optional[float]

    class Config:
        orm_mode = True

    @validator("SECTOR_DESCRIPTION", pre=True)
    def SECTOR_DESCRIPTION_validator(cls, value):
        if value is None:
            raise ValueError("Invalid SECTOR_DESCRIPTION")
        return value

    @validator("RCCConnSUCC", pre=True)
    def RCCConnSUCC_validator(cls, value):
        return int(value)

    @validator("RCCConnATT", pre=True)
    def RCCConnATT_validator(cls, value):
        return int(value)


class tbMROData(BaseModel):
    TimeStamp: str
    ServingSector: str
    InterferingSector: str
    LteScRSRP: float
    LteNcRSRP: float
    LteNcEarfcn: int
    LteNcPci: int

    class Config:
        orm_mode = True

    @validator("LteScRSRP", pre=True)
    def LteScRSRP_validator(cls, value):
        return float(value)

    @validator("LteNcRSRP", pre=True)
    def LteNcRSRP_validator(cls, value):
        return float(value)

    @validator("LteNcEarfcn", pre=True)
    def LteNcEarfcn_validator(cls, value):
        return int(value)

    @validator("LteNcPci", pre=True)
    def LteNcPci_validator(cls, value):
        return int(value)


class tbPRB(BaseModel):
    StartTime: datetime.datetime
    ENODEB_NAME: str
    SECTOR_DESCRIPTION: str
    SECTOR_NAME: str
    AvgNoise0: float
    AvgNoise1: float
    AvgNoise2: float
    AvgNoise3: float
    AvgNoise4: float
    AvgNoise5: float
    AvgNoise6: float
    AvgNoise7: float
    AvgNoise8: float
    AvgNoise9: float
    AvgNoise10: float
    AvgNoise11: float
    AvgNoise12: float
    AvgNoise13: float
    AvgNoise14: float
    AvgNoise15: float
    AvgNoise16: float
    AvgNoise17: float
    AvgNoise18: float
    AvgNoise19: float
    AvgNoise20: float
    AvgNoise21: float
    AvgNoise22: float
    AvgNoise23: float
    AvgNoise24: float
    AvgNoise25: float
    AvgNoise26: float
    AvgNoise27: float
    AvgNoise28: float
    AvgNoise29: float
    AvgNoise30: float
    AvgNoise31: float
    AvgNoise32: float
    AvgNoise33: float
    AvgNoise34: float
    AvgNoise35: float
    AvgNoise36: float
    AvgNoise37: float
    AvgNoise38: float
    AvgNoise39: float
    AvgNoise40: float
    AvgNoise41: float
    AvgNoise42: float
    AvgNoise43: float
    AvgNoise44: float
    AvgNoise45: float
    AvgNoise46: float
    AvgNoise47: float
    AvgNoise48: float
    AvgNoise49: float
    AvgNoise50: float
    AvgNoise51: float
    AvgNoise52: float
    AvgNoise53: float
    AvgNoise54: float
    AvgNoise55: float
    AvgNoise56: float
    AvgNoise57: float
    AvgNoise58: float
    AvgNoise59: float
    AvgNoise60: float
    AvgNoise61: float
    AvgNoise62: float
    AvgNoise63: float
    AvgNoise64: float
    AvgNoise65: float
    AvgNoise66: float
    AvgNoise67: float
    AvgNoise68: float
    AvgNoise69: float
    AvgNoise70: float
    AvgNoise71: float
    AvgNoise72: float
    AvgNoise73: float
    AvgNoise74: float
    AvgNoise75: float
    AvgNoise76: float
    AvgNoise77: float
    AvgNoise78: float
    AvgNoise79: float
    AvgNoise80: float
    AvgNoise81: float
    AvgNoise82: float
    AvgNoise83: float
    AvgNoise84: float
    AvgNoise85: float
    AvgNoise86: float
    AvgNoise87: float
    AvgNoise88: float
    AvgNoise89: float
    AvgNoise90: float
    AvgNoise91: float
    AvgNoise92: float
    AvgNoise93: float
    AvgNoise94: float
    AvgNoise95: float
    AvgNoise96: float
    AvgNoise97: float
    AvgNoise98: float
    AvgNoise99: float
    __DATETIME_PATTERN = "%m/%d/%Y %H:%M:%S"

    class Config:
        orm_mode = True

    @validator("StartTime", pre=True)
    def parse_datetime(cls, value):
        return datetime.datetime.strptime(value, cls.__DATETIME_PATTERN)


class TableIn(str, Enum):
    tbCell = "tbcell"
    tbKPI = "tbkpi"
    tbPRB = "tbprb"
    tbMROData = "tbmrodata"


class TableOut(str, Enum):
    tbCell = "tbcell"
    tbKPI = "tbkpi"
    tbC2i = "tbc2inew"

