from ch.hslu.wipro.fg.events.fg_observer import FGObserver

class DDPGLauncher(FGObserver):

    def on_update(self, observable, event):
        print("Event: {0} -> Start learning algorithm".format(event))

        # TODO Thread(target=ddpg.start_reinforcement_learning).start()

