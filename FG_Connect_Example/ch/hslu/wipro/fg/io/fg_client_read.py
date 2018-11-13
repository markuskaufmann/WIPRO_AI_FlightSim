from ch.hslu.wipro.fg.data.fg_data_input import FGDataInput
from ch.hslu.wipro.fg.io.fg_client import FGClient


class FGClientRead(FGClient):

    def process(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if data == b'':
                    continue
                FGDataInput.set(str(data, encoding='utf-8'))
            except Exception as e:
                print(e)
                break
