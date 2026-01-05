from platform_connector.platform_connector import platform_connector
from data_provider.data_provider import data_provider
from queue import Queue
from trading_director.trading_director import trading_director

if __name__ == "__main__":
    
    symbols = ["EURUSD","USDJPY","SP500","GBPUSD"]
    timeframe = '1min'
    #Creacion de la cola de evenetos principal
    events_queue = Queue()

    CONNECT = platform_connector(symbol_list=symbols)

    DATA_PROVIDER : data_provider = data_provider(events_queue=events_queue,symbol_list=symbols,timeframe=timeframe)

    TRADING_DIRECTOR = trading_director(events_queue=events_queue,data_provider=DATA_PROVIDER)
    TRADING_DIRECTOR.execute()