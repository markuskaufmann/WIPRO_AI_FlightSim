from time import sleep

from ch.hslu.wipro.fg.connect.tcp_socket_client_write import TCPSocketClientWrite
from ch.hslu.wipro.fg.io.fg_io_handler import FGIOHandler
from ch.hslu.wipro.fg.properties.fg_property_write_type import FGPropertyWriteType
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGWriteDirect:

    def __init__(self, prop_write_type: FGPropertyWriteType):
        self.prop_write_type = prop_write_type
        self.socket_client_write = TCPSocketClientWrite(FGPropertyWriteType.TYPE_PORT_MAP[self.prop_write_type])

    def write(self):
        self.socket_client_write.start()
        sleep(2)
        output = FGPropertyWriter.prepare_output(self.prop_write_type, aileron=0.78, aileron_trim=0.78,
                                                 elevator=0.89, elevator_trim=0.89, rudder=0.88, rudder_trim=0.88,
                                                 flaps=1.0, slats=1.0, speedbrake=1.0, throttle=0.65, mixture=1.0,
                                                 brake_left=0, brake_right=0, brake_parking=0, latitude_deg=52.0,
                                                 longitude_deg=54.0, altitude_ft=1000, airspeed_kt=20)
        print("write {0}".format(output))
        FGIOHandler.write(output)
        sleep(2)
        self.socket_client_write.close()


if __name__ == '__main__':
    FGWriteDirect(FGPropertyWriteType.WRITE_RESET).write()
