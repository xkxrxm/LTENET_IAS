from typing import List, Optional

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


class eNodeBPageResponse(BaseModel):
    count: int      # 总记录数
    list: List[eNodeBOut]      # 数据列表


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


class CellPageResponse(BaseModel):
    count: int
    list: List[CellOut]


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