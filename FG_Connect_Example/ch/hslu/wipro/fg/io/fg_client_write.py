from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.io.fg_client import FGClient
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FGClientWrite(FGClient):

    _instance = None

    @staticmethod
    def create_instance():
        if FGClientWrite._instance is not None:
            return
        FGClientWrite._instance = FGClientWrite(None, None)
        FGClientWrite._instance.start_process()

    def process(self):
        while self.running:
            data = FGDataOutput.get()
            data_val = str(data[1])
            if data_val is None or len(data_val.strip()) == 0 or data_val == 'None':
                continue
            socket = FGPropertyType.TYPE_CONNECTION_MAP[data[0]][1]
            socket.send(bytes(data_val, encoding='utf-8'))
