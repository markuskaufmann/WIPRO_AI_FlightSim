from ch.hslu.wipro.fg.events.fg_observable import FGObservable
from ch.hslu.wipro.fg.events.fg_observer import FGObserver


class FGReadyObserver(FGObserver):

    def on_update(self, observable: FGObservable, event):
        print("Start from {0}: {1}".format(observable, event))
