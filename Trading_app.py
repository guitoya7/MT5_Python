from platform_connector.platform_connector import platform_connector
from data_provider.data_provider import data_provider
from queue import Queue
from trading_director.trading_director import trading_director
from signal_generator.signals.ma_crossover import ma_crossover

if __name__ == "__main__":
    
    symbols = ["EURUSD","USDJPY"]#,"SP500","GBPUSD"]
    timeframe = '1min'
    slow_ma_period=50
    fast_ma_period=25
    #Creacion de la cola de evenetos principal
    events_queue = Queue()

    CONNECT = platform_connector(symbol_list=symbols)
    DATA_PROVIDER : data_provider = data_provider(events_queue=events_queue,symbol_list=symbols,timeframe=timeframe)
    SIGNAL_GENERATOR : ma_crossover = ma_crossover(events_queue=events_queue, data_provider=DATA_PROVIDER, 
                                                   timeframe=timeframe,fast_period= fast_ma_period,
                                                   slow_period=slow_ma_period)

    TRADING_DIRECTOR = trading_director(events_queue=events_queue,data_provider=DATA_PROVIDER,signal_generator=SIGNAL_GENERATOR)
    TRADING_DIRECTOR.execute()