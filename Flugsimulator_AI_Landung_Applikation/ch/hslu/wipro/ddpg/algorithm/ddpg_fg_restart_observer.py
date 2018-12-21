from time import sleep

from ch.hslu.wipro.fg.events.fg_observer import FGObserver


class DDPGFGRestartObserver(FGObserver):

    def __init__(self):
        self.ready = False

    def on_update(self, observable, event):
        sleep(2)
        self.ready = True
