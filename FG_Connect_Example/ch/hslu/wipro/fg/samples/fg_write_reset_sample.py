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
            FGPropertyWriter.reset_checkpoint2()
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGWriteResetSample())
    FGMain(fg_observable).start()
