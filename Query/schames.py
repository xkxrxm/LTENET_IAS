import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class eNodeBOut(BaseModel):
    CITY: str
    ENODEBID: str
    ENODEB_NAME: str
    VENDOR: str
    LONGITUDE: float
    LATITUDE: float
    STYLE: str  # 基站类型

    class Config:
        orm_mode = True


class eNodeB_params:
    def __init__(self,
                 ENODEBID: Optional[int] = None,
                 ENODEB_NAME: Optional[str] = None,
                 page: Optional[int] = 1,
                 size: Optional[int] = 10
                 ):
        self.ENODEBID = ENODEBID
        self.ENODEB_NAME = ENODEB_NAME
        self.page = page
        self.size = size


class CellOut(BaseModel):
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
    AZIMUTH: float
    HEIGHT: Optional[float]
    ELECTTILT: Optional[float]
    MECHTILT: Optional[float]
    TOTLETILT: Optional[float]

    class Config:
        orm_mode = True


class Cell_params:
    def __init__(self,
                 SECTOR_ID: Optional[int] = None,
                 SECTOR_NAME: Optional[str] = None,
                 page: Optional[int] = 1,
                 size: Optional[int] = 10
                 ):
        self.SECTOR_ID = SECTOR_ID
        self.SECTOR_NAME = SECTOR_NAME
        self.page = page
        self.size = size


class KpiProperty(str, Enum):
    RCCConnSUCC = "RCCConnSUCC",
    RCCConnRATE = "RCCConnRATE",
    RCCConnATT = "RCCConnATT"


class Kpi_params:
    def __init__(self,
                 SECTOR_NAME: str,
                 Property: KpiProperty,
                 StartTime: datetime.datetime = "2020-07-17 00:00:00",
                 EndTime: datetime.datetime = "2020-07-19 00:00:00"
                 ):
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.SECTOR_NAME = SECTOR_NAME
        self.Property = Property



class KPIOut(BaseModel):
    StartTime: datetime.datetime
    SECTOR_NAME: str
    RCCConnSUCC: int
    RCCConnATT: int
    RCCConnRATE: Optional[float]

    class Config:
        orm_mode = True


class PRB_mode(str, Enum):
    perHour = "perHour",  # 小时级
    perQuarter = "perQuarter"  # 分钟级 每15分钟


# PRB 请求参数约束
class PRB_params:
    def __init__(self,
                 ENODEB_NAME: str,
                 Mode: PRB_mode,
                 PRB: int,
                 StartTime: datetime.datetime = "2020-07-17 00:00:00",
                 EndTime: datetime.datetime = "2020-07-19 00:00:00",
                 ):
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.ENODEB_NAME = ENODEB_NAME
        self.Mode = Mode
        self.PRB = PRB



class PRBOut(BaseModel):
    Time: str
    data: float


class ListResponse(BaseModel):
    count: int
    list: List[Union[PRBOut, str, eNodeBOut, KPIOut]]


class ListCellOut(BaseModel):
    count: int
    list: List[CellOut]

