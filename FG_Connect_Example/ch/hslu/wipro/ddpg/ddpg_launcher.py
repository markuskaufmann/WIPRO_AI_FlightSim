from threading import Thread

from ch.hslu.wipro.ddpg.new import run
from ch.hslu.wipro.fg.events.fg_observer import FGObserver


class DDPGLauncher(FGObserver):

    def on_update(self, observable, event):
        print("Event: {0} -> Start learning algorithm".format(event))
        # Thread(target=run.start_reinforcement_learning()).start()
        Thread(target=run.play_result).start()
