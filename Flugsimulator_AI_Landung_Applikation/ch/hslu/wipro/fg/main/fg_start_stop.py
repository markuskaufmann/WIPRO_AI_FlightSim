import os
import time

from ch.hslu.wipro.fg.events.fg_observer import FGObserver
from ch.hslu.wipro.fg.events.fg_ready_observable import FGReadyObservable
from ch.hslu.wipro.fg.events.fg_write_conn_observer import FGWriteConnectionObserver
from ch.hslu.wipro.fg.launch.fg_launch import FGLaunch
from ch.hslu.wipro.fg.main.fg_broker_close import FGCloseBroker
from ch.hslu.wipro.fg.main.fg_exit import FGExit
from ch.hslu.wipro.fg.main.fg_init import FGInit


class FGStartStop:

    _observable = None
    _started = False
    _current_log_dir = None
    _current_log_file = None

    @staticmethod
    def start_fg(file_suffix: str, observers: [], log_dir=None):
        if FGStartStop._started:
            return
        print("Start FlightGear")
        FGStartStop._observable = FGReadyObservable(important_observers=[FGStartObserver(),
                                                                         FGWriteConnectionObserver()],
                                                    emergency_restart_start_delegate=FGStartStop.start_fg,
                                                    emergency_restart_stop_delegate=FGStartStop.stop_fg)
        for observer in observers:
            FGStartStop._observable.add_observer(observer)
        try:
            # init read socket server
            FGInit.init_read_connection()
            # init close broker
            FGCloseBroker.get_instance().add_delegates(FGInit.close_write_connections,
                                                       FGStartStop._on_fg_close)
            # launch FlightGear
            if log_dir is not None:
                FGStartStop._current_log_dir = log_dir
            log_file_name = time.strftime("%Y%m%d_%H%M%S") + "_fg_" + file_suffix + ".log"
            FGStartStop._current_log_file = open(FGStartStop._current_log_dir + '/' + log_file_name, 'w')
            FGLaunch.start_process(FGStartStop._current_log_file)
            # wait until FlightGear is ready
            FGStartStop._observable.start()
        except Exception as e:
            print("Error while starting FlightGear: {0}".format(e))

    @staticmethod
    def stop_fg(kill_process: bool = False):
        if not FGStartStop._started:
            return
        print("Stop FlightGear")
        if kill_process:
            os.system("taskkill /f /t /im fgfs.exe")
        else:
            FGExit.close_fg()
        FGStartStop._started = False

    @staticmethod
    def _on_fg_close():
        current_log_file = FGStartStop._current_log_file
        if current_log_file is not None:
            current_log_file.flush()
            current_log_file.close()
            FGStartStop._current_log_file = None


class FGStartObserver(FGObserver):

    def on_update(self, observable, event):
        FGStartStop._started = True
