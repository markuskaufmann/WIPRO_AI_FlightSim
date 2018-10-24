from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.events.fg_observable import FGObservable
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader


class FGReadyObservable(FGObservable):

    def __init__(self):
        super().__init__()
        self.t_wait = Thread(target=self.wait_until_fg_ready)
        self.fg_ready_fired = False

    def start(self):
        self.t_wait.start()

    def wait_until_fg_ready(self):
        while not self.fg_ready_fired:
            props = FGPropertyReader.get_properties()
            if props is None:
                continue
            if props['engine-running'] == 'true':
                sleep(10)
                self.fg_ready_fired = True
        # notify observers
        self.notify_observers("FlightGear is ready")
