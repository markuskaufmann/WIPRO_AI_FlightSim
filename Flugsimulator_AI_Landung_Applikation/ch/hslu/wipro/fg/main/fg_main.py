import os
import sys
import time

from ch.hslu.wipro.ddpg.ddpg_launcher import DDPGLauncher
from ch.hslu.wipro.fg.main.fg_start_stop import FGStartStop
from ch.hslu.wipro.fg.main.log_printer import LogPrinter


class FGMain:

    _LOG_DIR_PREFIX = 'logs/'

    log_dir = None

    def __init__(self):
        pass

    def start(self):
        try:
            ts = time.strftime("%Y%m%d_%H%M%S")
            file = ts + '_main.log'
            self.log_dir = FGMain._LOG_DIR_PREFIX + 'main_launch_' + ts
            os.mkdir(self.log_dir)
            f = open(self.log_dir + '/' + file, 'w')
            log_printer = LogPrinter(sys.stdout, f)
            sys.stdout = log_printer
            sys.stderr = log_printer
            FGStartStop.start_fg("initial_launch", [DDPGLauncher()], self.log_dir)
        except Exception as e:
            print("Error while launching FGMain: {0}".format(e))


if __name__ == '__main__':
    fg_main = FGMain()
    fg_main.start()
