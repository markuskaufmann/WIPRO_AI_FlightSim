import numpy as np

from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FGWriteGearSample(FGObserver):

    def __init__(self):
        self.t_running = Thread(target=self.write)
        self.running = True

    def write(self):
        sleep(5)
        while self.running:
            FGPropertyWriter.write_gear(brake_left=np.random.choice([-1, 0, 1]),
                                        brake_right=np.random.choice([-1, 0, 1]),
                                        brake_parking=np.random.choice([0, 1]))
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGWriteGearSample())
    FGMain(fg_observable).start()
