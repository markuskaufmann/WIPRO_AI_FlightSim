from threading import Thread
from time import sleep

import numpy as np

from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGReadWriteSample(FGObserver):

    def __init__(self):
        self.t_read = Thread(target=self.read)
        self.t_write = Thread(target=self.write)
        self.running = True

    def read(self):
        while self.running:
            props = FGPropertyReader.get_properties()
            distance_vector = DistCalc.process_distance_vector(props)
            print(props)
            distance_vector.print()
            sleep(0.5)

    def write(self):
        sleep(5)
        while self.running:
            FGPropertyWriter._write_control(aileron=np.random.choice([-1, 0, 1]),
                                            elevator=np.random.choice([-1, 0, 1]),
                                            rudder=np.random.choice([-1, 0, 1]),
                                            flaps=np.random.choice([-1, 0, 1]),
                                            throttle=np.random.choice([0, 1]),
                                            mixture=np.random.choice([0, 1]))
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_read.start()
        self.t_write.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGReadWriteSample())
    FGMain(fg_observable).start()
