from pydantic import BaseModel


class FixedSizinProps(BaseModel):
    
    volume: float

class MinSizinProps(BaseModel):
    ...

class RiskPctSizinProps(BaseModel):
    risk_pct: float
    