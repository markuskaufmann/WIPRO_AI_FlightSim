from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_init import FGInit


class FGWriteConnectionObserver(FGObserver):

    def on_update(self, observable, event):
        FGInit.init_write_connections()
