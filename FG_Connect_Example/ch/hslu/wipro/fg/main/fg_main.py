from ch.hslu.wipro.ddpg.ddpg_launcher import DDPGLauncher
from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.main.fg_init import FGInit
from ch.hslu.wipro.fg.main.fg_ready_observable import FGReadyObservable


class FGMain(FGObserver):

    def __init__(self, observable: FGReadyObservable):
        self.fg_init = FGInit()
        self.fg_observable = observable
        self.fg_observable.add_observer(self)
        self.fg_observable.add_observer(DDPGLauncher())

    def on_update(self, observable, event):
        # init write socket clients
        self.fg_init.init_write_connections()

    def start(self):
        try:
            # init read socket server
            self.fg_init.init_read_connection()
            # launch FlightGear
            # TODO FGLaunch.start_process()
            # wait until FlightGear is ready
            self.fg_observable.start()
        except Exception as e:
            print(e)


def show_tensorboard():
    import os
    path = "C:\\Users\\Cyrille\\Documents\\GitHub\\WIPRO_AI_FlightSim\\FG_Connect_Example\\ch\\hslu\\wipro\\fg\\main\\results\\tf_ddpg"
    os.system('tensorboard --logdir=' + path)


if __name__ == '__main__':
    fg_main = FGMain(FGReadyObservable())
    fg_main.start()
