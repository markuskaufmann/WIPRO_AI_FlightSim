from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader


class FGReadSample(FGObserver):

    def __init__(self):
        self.t_running = Thread(target=self.read)
        self.running = True

    def read(self):
        while self.running:
            props = FGPropertyReader.get_properties()
            distance_vector = DistCalc.process_distance_vector(props)
            print(props)
            distance_vector.print()
            sleep(0.5)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGReadSample())
    FGMain(fg_observable).start()
