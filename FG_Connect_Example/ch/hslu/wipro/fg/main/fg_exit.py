import os
from time import sleep

from ch.hslu.wipro.fg.main.fg_init import FGInit
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGExit:

    @staticmethod
    def close_fg():
        try:
            FGInit.close_read_client_connection()
            # FGInit.close_write_connections()
            # os.system("taskkill /f /t /im fgfs.exe")
            FGPropertyWriter.fg_exit()
            sleep(2)
            FGInit.close_write_connections()
        except Exception as e:
            print(e)
