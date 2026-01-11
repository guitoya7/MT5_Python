from ..position_sizers.min_size_position_sizer import IPositionSizer
from events.events import signal_event
from data_provider.data_provider import data_provider
import MetaTrader5 as mt5

class MinSizePosition(IPositionSizer):
    def size_signal(self,signal_event : signal_event, data_provider: data_provider):
        
        volume_min = mt5.simbol_info(signal_event.symbol).volume_min

        if volume_min is not None:
            return volume_min
        else:
            print(f"ERROR (MinSizePosition) no se ha podido determinar el volumen minimo de {signal_event.symbol}")
            return 0.0 