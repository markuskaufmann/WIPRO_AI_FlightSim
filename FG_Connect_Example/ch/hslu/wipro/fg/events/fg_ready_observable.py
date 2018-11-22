from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.events.fg_observable import FGObservable
from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_broker_restart import FGRestartBroker
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader


class FGReadyObservable(FGObservable):

    def __init__(self, important_observers: [FGObserver] = None,
                 emergency_restart_start_delegate=None,
                 emergency_restart_stop_delegate=None):
        super().__init__()
        self.important_observers = important_observers
        self.emergency_restart_start_delegate = emergency_restart_start_delegate
        self.emergency_restart_stop_delegate = emergency_restart_stop_delegate
        self.t_wait = Thread(target=self.wait_until_fg_ready)
        self.fg_ready = False

    def start(self):
        self.t_wait.start()

    def wait_until_fg_ready(self):
        print("Wait until FlightGear is ready")
        read_count = 0
        while not self.fg_ready:
            props = FGPropertyReader.get_properties()
            if props is None:
                continue
            if props['fdm-initialized'] == 'true':
                read_count += 1
            if read_count == 20:
                sleep(10)
                self.fg_ready = True
        print("FlightGear is ready")
        # if there are any important observers, notify them first
        if self.important_observers is not None:
            for observer in self.important_observers:
                try:
                    observer.on_update(self, "FlightGear is ready")
                except RuntimeError as re:
                    print("Error while notifying important observers: {0}".format(re))
                    print("Try to restart FlightGear...")
                    self.restart_fg()
                    return
        # notify observers
        self.notify_observers("FlightGear is ready")

    def restart_fg(self):
        FGRestartBroker(observers=self.observers,
                        start_delegate=self.emergency_restart_start_delegate,
                        stop_delegate=self.emergency_restart_stop_delegate,
                        stop_delegate_force=True).request_fg_restart()
