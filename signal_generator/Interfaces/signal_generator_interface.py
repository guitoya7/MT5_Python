from typing import Protocol
from events.events import data_event

class ISignalGenerator(Protocol):

    def generate_signal(self,data_event : data_event) -> None:
        ...
    
