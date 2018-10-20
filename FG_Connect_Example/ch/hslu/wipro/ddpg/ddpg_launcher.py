from threading import Thread

from ch.hslu.wipro.ddpg import ddpg
from ch.hslu.wipro.fg.events.fg_observer import FGObserver


class DDPGLauncher(FGObserver):

    def on_update(self, observable, event):
        print("Event: {0} -> Start learning algorithm".format(event))
        Thread(target=ddpg.start_reinforcement_learning).start()
