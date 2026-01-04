import MetaTrader5 as mt5
import os 
from dotenv import load_dotenv, find_dotenv
class platform_connector:
    def __init__(self):
        
        load_dotenv(find_dotenv())
        self._initialize_platform()
        self._live_account_warning()
        self._check_trading_algoritmico()

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
        
        