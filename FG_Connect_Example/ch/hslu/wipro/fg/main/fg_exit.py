import os

from ch.hslu.wipro.fg.main.fg_init import FGInit


class FGExit:

    @staticmethod
    def close_fg():
        try:
            FGInit.close_read_client_connection()
            FGInit.close_write_connections()
            os.system("taskkill /f /t /im fgfs.exe")
        except Exception as e:
            print(e)
