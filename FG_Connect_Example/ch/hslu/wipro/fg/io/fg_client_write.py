from time import sleep

from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.io.fg_client import FGClient
from ch.hslu.wipro.fg.main.fg_closebroker import FGCloseBroker
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
            try:
                data = FGDataOutput.get()
                fg_type = data[0]
                data_val = str(data[1])
                if data_val is None or len(data_val.strip()) == 0 or data_val == 'None':
                    continue
                socket = FGPropertyType.TYPE_CONNECTION_MAP[fg_type][1]
                socket.send(bytes(data_val, encoding='utf-8'))
                # close / reinit on fg_exit
                if fg_type == FGPropertyType.WRITE_RESET and data_val.strip('\r\n').endswith('1'):
                    print("FGExit sent")
                    FGCloseBroker.get_instance().request_fg_close()
                    FGDataOutput.reinit()
            except Exception as e:
                print(e)
                break
