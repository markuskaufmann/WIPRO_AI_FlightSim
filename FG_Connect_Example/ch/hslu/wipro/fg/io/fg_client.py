from threading import Thread


class FGClient:

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.running = True
        self.thread = Thread(target=self.process)

    def start_process(self):
        self.thread.start()

    def stop_process(self):
        self.running = False

    def process(self):
        raise NotImplementedError("Abstract method - to be implemented in subclasses")
