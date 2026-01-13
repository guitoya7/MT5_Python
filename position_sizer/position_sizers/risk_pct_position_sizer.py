from ..position_sizers.min_size_position_sizer import IPositionSizer
from events.events import signal_event
from data_provider.data_provider import data_provider
import MetaTrader5 as mt5
from ..properties.position_sizer_properties import RiskPctSizingProps 


class riskpctpositionsizer(IPositionSizer):

    def __init__(self,properties: RiskPctSizingProps):
        self.risk_pct = properties.risk_pct
        


    def size_signal(self,signal_event : signal_event, data_provider: data_provider):
        risk_pct = self.risk_pct
        
        if risk_pct<=0.0:
            print(f"ERROR (RiskPositionSizer): El porcentaje de riesgo introducido {risk_pct} no es valido")
            return 0.0

        if signal_event.sl <=0.0:
            print(f"ERROR (RiskPositionSizer): El stop loss introducido {signal_event.sl} no es valido")
            return 0.0

        #Acceder informacion a la divisa de la cuenta para calcular el riesgo

        account_info = mt5.account_info()
        symbol_info = mt5.symbol_info(signal_event.symbol)
        # recuperamos el precio de entrada estimado
        if signal_event.target_order == "MARKET":
            #Obtener el precio de mercado actual
            last_tick = data_provider.get_last_tick(signal_event.symbol)
            entry_price = last_tick['ask'] if signal_event.signal == "BUY" else last_tick['bid']
        
        # si es una orden pendiente (limit o stop)
        else:
            entry_price = signal_event.target_price

        
        #Conseguimos los valores que nos faltan para los calculos
        equity = account_info.equity
        volume_step = symbol_info.volume_step #Cambio minimo de volumen
        tick_size = symbol_info.trade_tick_size #Cambio minimo del precio
        account_currency = account_info.currency #Divisa de la cuenta
        profit_currency = symbol_info.profit_currency #Divisa de beneficios del simbolo
        contract_size = symbol_info.trade_contract_size #Tamaño del contrato (1 lote)
        
        #tick_size
        tick_value_proffit_ccy = contract_size * tick_size

        #convertir el tick value en profit currency a la divisa de la cuenta
        ticket_value_account_ccy = 

        #Calculo del tamaño de la posicion
        price_distante_int_ticks = int(abs(entry_price - signal_event.sl) / tick_size)
        monetary_risk = equity * self.risk_pct
        volume = monetary_risk / (price_distante_int_ticks * ticket_value_account_ccy)
        volume = round(volume / volume_step) * volume_step
        return volume


