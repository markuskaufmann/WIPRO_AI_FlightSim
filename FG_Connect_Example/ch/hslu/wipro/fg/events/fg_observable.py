from ch.hslu.wipro.fg.events.fg_observer import FGObserver


class FGObservable:

    def __init__(self):
        self.observers = set()

    def add_observer(self, observer: FGObserver):
        self.observers.add(observer)

    def remove_observer(self, observer: FGObserver):
        self.observers.remove(observer)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.on_update(self, event)
