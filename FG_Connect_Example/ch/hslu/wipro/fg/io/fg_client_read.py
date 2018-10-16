import threading

from ch.hslu.wipro.fg.io.fg_client import FGClient
from ch.hslu.wipro.fg.io.fg_io_handler import FGIOHandler


class FGClientRead(FGClient):

    lock = threading.Lock()

    def process(self):
        while self.running:
            data = self.socket.recv(1024)
            if data == b'':
                continue
            self.lock.acquire()
            FGIOHandler.INPUT = str(data, encoding='utf-8')
            self.lock.release()
