from threading import Thread
from time import sleep

import numpy as np

from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGWriteControlSample(FGObserver):

    def __init__(self):
        self.t_running = Thread(target=self.write)
        self.running = True

    def write(self):
        sleep(5)
        while self.running:
            FGPropertyWriter._write_control(aileron=np.random.choice([-1, 0, 1]),
                                            aileron_trim=np.random.choice([-1, 0, 1]),
                                            elevator=np.random.choice([-1, 0, 1]),
                                            elevator_trim=np.random.choice([-1, 0, 1]),
                                            rudder=np.random.choice([-1, 0, 1]),
                                            rudder_trim=np.random.choice([-1, 0, 1]),
                                            flaps=np.random.choice([-1, 0, 1]))
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGWriteControlSample())
    FGMain(fg_observable).start()
