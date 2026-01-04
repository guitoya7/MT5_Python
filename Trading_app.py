from platform_connector.platform_connector import platform_connector

if __name__ == "__main__":
    
    symbols = ["EURUSD","USDJPY"]

    CONNECT = platform_connector(symbol_list=symbols)