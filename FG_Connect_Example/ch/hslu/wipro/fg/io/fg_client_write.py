import threading

from ch.hslu.wipro.fg.io.fg_client import FGClient
from ch.hslu.wipro.fg.io.fg_io_handler import FGIOHandler


class FGClientWrite(FGClient):

    lock = threading.Lock()

    def process(self):
        while self.running:
            data = str(FGIOHandler.OUTPUT)
            if data is None or len(data.strip()) == 0:
                continue
            self.lock.acquire()
            self.socket.send(bytes(data, encoding='utf-8'))
            FGIOHandler.OUTPUT = None
            self.lock.release()
