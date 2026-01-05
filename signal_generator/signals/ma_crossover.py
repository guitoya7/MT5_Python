from ..Interfaces.signal_generator_interface import ISignalGenerator
from events.events import data_event
from queue import Queue
from data_provider.data_provider import data_provider
import pandas as pd

class ma_crossover(ISignalGenerator):

    def __init__(self,events_queue: Queue, data_provider: data_provider, fast_period: int, slow_period: int,timeframe: str):
        
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        self.fast_period = fast_period if fast_period >1 else 2
        self.slow_period = slow_period if slow_period >2 else 3
        self.timeframe = timeframe

        if self.fast_period >= self.slow_period:
            raise Exception("Slow period no es mayor al fast period, no tiene sentido")

    
    def _create_and_put_signal_event(self,symbol : str, signal : str, target_order: str, price: float, strategic_id: int,sl: float,tp: float):
        signal_event = signal_event(symbol=symbol,signal=signal,target_order=target_order,target_order =target_order,target_price = target_price,strategic_id : int,sl: float,tp: floa)


    
    def generate_signal(self, data_event: data_event) -> None:

        symbol = data_event.symbol

        #recuperamos los datos necesarios para el signal

        bars = self.DATA_PROVIDER.get_lastest_closed_bars(symbol=symbol,timeframe=self.timeframe,num_bars= self.slow_period)

        fast_avg = bars['close'].iloc[-self.fast_period:].mean()
        slow_avg = bars['close'].iloc[-self.slow_period:].mean()

        #Detectamos compra
        if fast_avg>slow_avg:
            signal = "BUY"
        elif fast_avg<slow_avg:
            signal = "SELL"
        else:
            signal = ""

        if signal !="":


        


        