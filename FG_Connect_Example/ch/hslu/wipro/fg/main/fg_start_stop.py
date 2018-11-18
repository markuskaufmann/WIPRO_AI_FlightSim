from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.events.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.events.fg_write_conn_observer import FGWriteConnectionObserver
from ch.hslu.wipro.fg.launch.fg_launch import FGLaunch
from ch.hslu.wipro.fg.main.fg_closebroker import FGCloseBroker
from ch.hslu.wipro.fg.main.fg_exit import FGExit
from ch.hslu.wipro.fg.main.fg_init import FGInit


class FGStartStop:

    observable = None
    started = False

    @staticmethod
    def start_fg(observers: []):
        if FGStartStop.started:
            return
        print("Start FlightGear")
        FGStartStop.observable = FGReadyObservable()
        FGStartStop.observable.add_observer(FGStartObserver())
        FGStartStop.observable.add_observer(FGWriteConnectionObserver())
        for observer in observers:
            FGStartStop.observable.add_observer(observer)
        try:
            # init read socket server
            FGInit.init_read_connection()
            # init close broker
            FGCloseBroker.get_instance().add_delegate(FGInit.close_write_connections)
            # launch FlightGear
            FGLaunch.start_process()
            # wait until FlightGear is ready
            FGStartStop.observable.start()
        except Exception as e:
            print(e)

    @staticmethod
    def stop_fg():
        if not FGStartStop.started:
            return
        print("Stop FlightGear")
        FGExit.close_fg()
        FGStartStop.started = False


class FGStartObserver(FGObserver):

    def on_update(self, observable, event):
        FGStartStop.started = True
