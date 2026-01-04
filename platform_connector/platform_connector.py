import MetaTrader5 as mt5
import os 
from dotenv import load_dotenv, find_dotenv
class platform_connector:
    def __init__(self,symbol_list : list):
        
        load_dotenv(find_dotenv())
        self._initialize_platform()
        self._live_account_warning()
        self._check_trading_algoritmico()
        self._add_symbols_to_mw(symbol_list)
        self._print_account_info()

    def _initialize_platform(self) -> None: 
        """
        MT5 CONNECTION
        
        """
        if mt5.initialize(
        path=os.getenv("MT5_PATH"),                     
        login=int(os.getenv("MT5_LOGIN")),              
        password=os.getenv("MT5_PASWORD"),      
        server=os.getenv("MT5_SERVER"),          
        timeout=int(os.getenv("MT5_TIMEOUT")),          
        portable=eval(os.getenv("MT5_PORTABLE"))):
            print("Conexion establecida con éxito!!!")
        
        else:
            raise Exception(f"Conexion erronea {mt5.last_error()}")
        
    def _live_account_warning(self) -> None:

        if mt5.account_info().trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("cuenta de tipo demo")

        elif mt5.account_info().trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            
            if not input("ALERTA! Cuenta de tipo real detectada. Capital en riesgo, quiere continuar? (y/n): ").lower() == "y":
                mt5.shutdown()
                raise Exception("Se ha desconectado la cuenta") 

        else:
            print("cuenta de tipo consurso")

    def _check_trading_algoritmico(self)-> None:

        if not mt5.terminal_info().trade_allowed:
            raise Exception("El trading algorítmico está desactivado, se debe actualizar manualmente desde la app")
        

    def _add_symbols_to_mw(self,symbols: list)-> None:

        #Simbolo en el mw?
        for symbol in symbols:
            if mt5.symbol_info(symbol) is None:
                print(f"No se ha podido añadir el simbolo al mw: {mt5.last_error()}")
                continue
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol,True):
                    print(f"No se ha podido añadir el simbolo al mw: {mt5.last_error()}")
                else:
                    print(f"Simbolo {symbol} añadido al mw")
            else:
                print(f"Simbolo {symbol} ya estaba visible en mw")
    
    def _print_account_info(self)-> None:
        
        account_info = mt5.account_info()._asdict()

        print("Informacion de la cuenta: ")
        print(f"Account ID: {account_info['login']}")
        print(f"Nombre trader: {account_info['name']}")
        print(f"Broker: {account_info['company']}")
        print(f"Servidor: {account_info['server']}")
        print(f"Apalancamiento: {account_info['leverage']}")
        print(f"Divisa: {account_info['currency']}")
        print(f"Balance: {account_info['balance']}")


        
        