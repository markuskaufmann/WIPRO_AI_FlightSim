from threading import Thread
from time import sleep


class FGCloseBroker:

    _instance = None

    def __init__(self):
        self.close_request = False
        self.running = True
        self.delegates = set()
        Thread(target=self.process).start()

    def add_delegate(self, delegate):
        self.delegates.add(delegate)

    def remove_delegate(self, delegate):
        self.delegates.remove(delegate)

    def process(self):
        while self.running:
            sleep(0.5)
            if not self.close_request:
                continue
            for delegate in self.delegates:
                delegate()
            self.stop()
        FGCloseBroker._instance = None

    def request_fg_close(self):
        self.close_request = True

    def stop(self):
        self.running = False

    @staticmethod
    def get_instance():
        if FGCloseBroker._instance is None:
            FGCloseBroker._instance = FGCloseBroker()
        return FGCloseBroker._instance
