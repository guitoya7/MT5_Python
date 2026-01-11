from typing import Protocol
from events.events import signal_event
from data_provider.data_provider import data_provider

class IPositionSizer(Protocol):
    def size_signal(self,signal_event : signal_event, data_provider: data_provider) -> float:
        ...