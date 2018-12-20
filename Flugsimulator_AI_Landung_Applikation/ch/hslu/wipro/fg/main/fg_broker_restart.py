from threading import Thread
from time import sleep


class FGRestartBroker:

    def __init__(self, observers: [],
                 start_delegate=None,
                 stop_delegate=None,
                 stop_delegate_force=False,
                 sleep_between_stop_start: int = 5,
                 log_file_suffix: str = "restart"):
        self.restart_request = False
        self.observers = observers
        self.start_delegate = start_delegate
        self.stop_delegate = stop_delegate
        self.stop_delegate_force = stop_delegate_force
        self.sleep_stop_start = sleep_between_stop_start
        self.log_file_suffix = log_file_suffix
        self.running = True
        Thread(target=self.process).start()

    def process(self):
        while self.running:
            sleep(0.3)
            if not self.restart_request:
                continue
            print("Restart FlightGear")
            self.stop_fg()
            sleep(self.sleep_stop_start)
            self.start_fg()
            self.stop()

    def request_fg_restart(self):
        self.restart_request = True

    def stop(self):
        self.running = False

    def stop_fg(self):
        print("Stopping FlightGear...")
        self.stop_delegate(self.stop_delegate_force)

    def start_fg(self):
        print("Starting FlightGear...")
        self.start_delegate(self.log_file_suffix, self.observers)
