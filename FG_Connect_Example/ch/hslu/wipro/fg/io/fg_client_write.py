from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.io.fg_client import FGClient


class FGClientWrite(FGClient):

    def process(self):
        while self.running:
            data = FGDataOutput.get()
            if data is None or len(data.strip()) == 0 or data == 'None':
                continue
            self.socket.send(bytes(data, encoding='utf-8'))
