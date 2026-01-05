import MetaTrader5 as mt5
import pandas as pd
from typing import Dict
from datetime import datetime

class data_provider():
    def __init__(self,symbol_list:  list, timeframe ):
        self.symbols= symbol_list
        self.timeframe = timeframe

        #Guardamos un diccionario para guardar el datetime de la ultima vela que hemos visto para cada simbolo
        self.last_bar_datetime : Dict[str,datetime] = {symbol : datetime.min for symbol in self.symbols}
    
    def _map_tf(self,timeframe: str):
        timeframe_mapping = {
            '1min': mt5.TIMEFRAME_M1,
            '2min': mt5.TIMEFRAME_M2,                        
            '3min': mt5.TIMEFRAME_M3,                        
            '4min': mt5.TIMEFRAME_M4,                        
            '5min': mt5.TIMEFRAME_M5,                        
            '6min': mt5.TIMEFRAME_M6,                        
            '10min': mt5.TIMEFRAME_M10,                       
            '12min': mt5.TIMEFRAME_M12,
            '15min': mt5.TIMEFRAME_M15,
            '20min': mt5.TIMEFRAME_M20,                       
            '30min': mt5.TIMEFRAME_M30,                       
            '1h': mt5.TIMEFRAME_H1,                          
            '2h': mt5.TIMEFRAME_H2,                          
            '3h': mt5.TIMEFRAME_H3,                          
            '4h': mt5.TIMEFRAME_H4,                          
            '6h': mt5.TIMEFRAME_H6,                          
            '8h': mt5.TIMEFRAME_H8,                          
            '12h': mt5.TIMEFRAME_H12,
            '1d': mt5.TIMEFRAME_D1,                       
            '1w': mt5.TIMEFRAME_W1,                       
            '1M': mt5.TIMEFRAME_MN1}
        try:
            return timeframe_mapping[timeframe]
        except Exception as e:
            print(f"{e}")

    def get_lastest_closed_bars(self,symbol: str, timeframe: str,num_bars=1) -> pd.DataFrame:
        
        tf = self._map_tf(timeframe)
        from_position = 1
        bars_count = num_bars if num_bars >1 else 1

        bars = mt5.copy_rates_from_pos(symbol,tf,from_position,bars_count)
        if bars is None:
            print("No se han podido cargar los datos")
            bars = pd.Series()
        else:
            bars=pd.DataFrame(bars)
            bars=pd.to_datetime(bars['time'],unit='s')
            bars.set_index('time',inplace=True)
            bars.rename({'tick_volume':"tickvol","real_volume":"vol"})
            bars=bars[['open','high','low','close','tickvol','vol','spread']]

        if bars.empty:
            return pd.DataFrame()
        else:
            return bars
        
    def get_lastest_tick(self,symbol: str):

        try:
            tick = mt5.symbol_info_tick(symbol) 
            if tick is None:
                print(f"No se ha podido recuperar el ultimo tick de {symbol}")
                return {}
        except Exception as e:
            print(fr"Algo ha ido mal recuperando el último tick, {e}, el error de aplicacion es {mt5.last_error()}")
        
        else:
            return tick._asdict()
        
    def check_for_new_data(self)-> None:

        for symbol in self.symbols:

            latest_bar = self.get_lastest_closed_bars(symbol,self.timeframe)
       
            if latest_bar is None:
                continue

            if not latest_bar.empty and latest_bar.iloc[-1].name > self.last_bar_datetime[symbol]:
                
                self.last_bar_datetime[symbol] = latest_bar.iloc[-1].name
