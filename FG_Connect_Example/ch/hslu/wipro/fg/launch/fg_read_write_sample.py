from threading import Thread
from time import sleep

import ch.hslu.wipro.ddpg.ddpg
from ch.hslu.wipro.ddpg import ddpg
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.connect.tcp_socket_client_write import TCPSocketClientWrite
from ch.hslu.wipro.fg.connect.tcp_socket_server_read import TCPSocketServerRead
from ch.hslu.wipro.fg.io.fg_io_handler import FGIOHandler
from ch.hslu.wipro.fg.events.fg_observable import FGObservable
from ch.hslu.wipro.fg.events.fg_ready_observer import FGReadyObserver
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader
from ch.hslu.wipro.fg.properties.fg_property_write_type import FGPropertyWriteType
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGReadWriteSample:

    def __init__(self):
        self.socket_server_read = TCPSocketServerRead(9876)
        self.socket_client_write = TCPSocketClientWrite(9877)
        # self.t_write = Thread(target=self.write)
        self.t_read = Thread(target=self.read)
        self.start_observable = FGObservable()
        self.start_observer = FGReadyObserver()
        self.start_observable.add_observer(self.start_observer)
        self.ready_fired = False

    def start(self):
        self.socket_server_read.start()
        self.t_read.start()
        # self.t_write.start()

    # def write(self):
    #     sleep(80)
    #     print("write start")
    #     self.socket_client_write.start()
    #     sleep(2)
    #     output = FGPropertyWriter.prepare_output(FGPropertyWriteType.WRITE_RESET, aileron=0.78, aileron_trim=0.78,
    #                                              elevator=0.89, elevator_trim=0.89, rudder=0.88, rudder_trim=0.88,
    #                                              flaps=1.0, slats=1.0, speedbrake=1.0, throttle=0.5, mixture=1.0,
    #                                              brake_left=0, brake_right=0, brake_parking=0.0, latitude_deg=52.0,
    #                                              longitude_deg=54.0, altitude_ft=1000, airspeed_kt=20)
    #     print("write {0}".format(output))
    #     FGIOHandler.write(output)

    def read(self):
        while not self.socket_server_read.is_closed():
            props = FGPropertyReader.get_properties()
            if props is None:
                continue
            print(props)
            if self.ready_fired:
                dist_vector = DistCalc.process_distance_vector(props['latitude-deg'],
                                                               props['longitude-deg'],
                                                               props['altitude-ft'])
                dist_vector.print()
            if not self.ready_fired:
                if round(float(props['altitude-ft']), 1) > 0.0:
                    sleep(10)
                    self.start_observable.notify_observers("FlightGear is ready")
                    self.ready_fired = True
            sleep(0.5)


if __name__ == '__main__':
    fgrws = FGReadWriteSample()
    fgrws.start()
    ddpg.start_reinforcement_learning()
