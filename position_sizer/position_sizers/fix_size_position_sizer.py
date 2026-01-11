from ..position_sizers.min_size_position_sizer import IPositionSizer
from events.events import signal_event
from data_provider.data_provider import data_provider
import MetaTrader5 as mt5
from ..properties.position_sizer_properties import FixedSizinProps

class FixSizePosition(IPositionSizer):

    def __init__(self,properties: FixedSizinProps):
        self.fixed_volume = properties.volume


    def size_signal(self,signal_event : signal_event, data_provider: data_provider):
        return self.fixed_volume