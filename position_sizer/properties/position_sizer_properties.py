from pydantic import BaseModel


class FixedSizinProps(BaseModel):
    
    volume: float

class MinSizinProps(BaseModel):
    ...
    
    