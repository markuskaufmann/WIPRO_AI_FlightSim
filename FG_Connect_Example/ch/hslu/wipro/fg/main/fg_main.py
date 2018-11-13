from ch.hslu.wipro.ddpg.ddpg_launcher import DDPGLauncher
from ch.hslu.wipro.fg.main.fg_start_stop import FGStartStop


class FGMain:

    def __init__(self):
        pass

    def start(self):
        try:
            FGStartStop.start_fg([DDPGLauncher()])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    fg_main = FGMain()
    fg_main.start()
