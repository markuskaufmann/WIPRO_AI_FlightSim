from ch.hslu.wipro.fg.main.fg_init import FGInit
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGExit:

    @staticmethod
    def close_fg():
        try:
            FGInit.close_read_client_connection()
            FGPropertyWriter.fg_exit()
        except Exception as e:
            print("Error while sending close command: {0}".format(e))
