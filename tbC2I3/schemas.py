from pydantic import BaseModel


class tbC2Inew(BaseModel):
    SCELL: str
    NCELL: str
    C2I_Mean: float
    Std: float
    PrbC2I9: float
    PrbABS6: float
    num:int


class tbC2i3Out(BaseModel):
    CEll_A: str
    CEll_B: str
    CEll_C: str
    x: float

