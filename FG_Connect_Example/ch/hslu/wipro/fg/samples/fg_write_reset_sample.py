from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGWriteResetSample(FGObserver):

    def __init__(self):
        self.t_running = Thread(target=self.write)
        self.running = True

    def write(self):
        sleep(5)
        while self.running:
            FGPropertyWriter._write_reset(aileron=0, aileron_trim=0, elevator=0, elevator_trim=0, rudder=0,
                                          rudder_trim=0, flaps=1, throttle=0, mixture=0, brake_left=0, brake_right=0,
                                          brake_parking=0, latitude_deg=21.3252466948, longitude_deg=-158.1431852166,
                                          altitude_ft=100, airspeed_kt=20, damage='false', pitch_deg=0, roll_deg=0,
                                          heading_deg=90)
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGWriteResetSample())
    FGMain(fg_observable).start()
