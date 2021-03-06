from threading import Thread
from time import sleep

from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_main import FGMain
from ch.hslu.wipro.fg.events.fg_ready_observable import FGReadyObservable


class FGWriteEngineSample(FGObserver):

    def __init__(self):
        self.t_running = Thread(target=self.write)
        self.running = True

    def write(self):
        sleep(5)
        while self.running:
            # FGPropertyWriter._write_engine(throttle=np.random.choice([0, 1]),
            #                                mixture=np.random.choice([0, 1]))
            sleep(10)

    def stop(self):
        self.running = False

    def on_update(self, observable, event):
        self.t_running.start()


if __name__ == '__main__':
    fg_observable = FGReadyObservable()
    fg_observable.add_observer(FGWriteEngineSample())
    FGMain(fg_observable).start()
