from enum import Enum
import pandas as pd
from pydantic import BaseModel


#Definicion de los distintos tipos de eventos

class event_type(str,Enum):
    DATA = "DATA"
    SIGNAL = "SIGNAL"

class base_event(BaseModel):
    EventType : event_type

    class Config:
        arbitrary_types_allowed = True

class signal_type(str,Enum):
    BUY = "BUY"
    SELL = "SELL"

class order_type(str,Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"

class data_event(base_event):
    EventType: event_type = event_type.DATA
    symbol: str 
    data: pd.Series

class signal_event(base_event):
    EventType: event_type = event_type.SIGNAL
    symbol: str
    signal: signal_type
    target_order : order_type
    target_price : float
    strategic_id : int
    sl: float
    tp: float


