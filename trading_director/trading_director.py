import queue 
from data_provider import data_provider
from typing import Dict,Callable
from events.events import data_event,signal_event
import time
from datetime import datetime
from signal_generator.Interfaces.signal_generator_interface import ISignalGenerator

class trading_director():
    def __init__(self, events_queue: queue.Queue, data_provider : data_provider,signal_generator: ISignalGenerator):
        self.events_queue =  events_queue
        self.DATA_PROVIDER = data_provider
        self.SIGNAL_GENERATOR = signal_generator

        self.continue_trading : bool = True

        #creacion del event handler
        self.events_handler : Dict[str,Callable] = {
            "DATA" : self.handle_data_event,
            "SIGNAL": self.handle_signal_event

        }

    def handle_data_event(self,event: data_event):
        print(f"{event.data.name} - Recibidos nuevos datos {event.symbol} - ultimo precio de cierre {event.data.close}")
        self.SIGNAL_GENERATOR.generate_signal(event)

    def handle_signal_event(self,event: signal_event):
        print(f" Signal event receibed {event.signal} para {event.symbol}")


    def execute(self) -> None:
        while self.continue_trading == True:
            try:
                event = self.events_queue.get(block=False)
            
            except queue.Empty:
                self.DATA_PROVIDER.check_for_new_data()

            else:
                if event is not None:
                    handler = self.events_handler.get(event.EventType)
                    handler(event)
                else:
                    self.continue_trading = False
                    print("ERROR: Recibido evento nulo. Terminado ejecucion del Framework")
            
            time.sleep(0.1)
        print("FIN")