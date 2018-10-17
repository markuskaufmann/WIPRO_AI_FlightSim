import os
from threading import Thread


class FGLaunch:

    # FG Location
    # FG_DIR = "C:\\Users\\MK\\Documents\\FlightGear_Root\\FlightGear 2018.2.2"
    FG_DIR = "C:\\Program Files\\FlightGear 2018.2.2"

    # Executable
    FG_EXECUTABLE = FG_DIR + "\\bin\\fgfs.exe"
    FG_DATA = FG_DIR + "\\data"

    # Commands
    FG_CMD_FGROOT = " --fg-root=\"" + FG_DATA + "\""
    FG_CMD_WINDOW = " --geometry=640x480 --disable-splash-screen"
    FG_CMD_AIRCRAFT = " --aircraft=c172p"
    FG_CMD_AIRPORT = " --airport=PHNL --runway=08L"
    FG_CMD_TIME = " --timeofday=noon"
    FG_CMD_FREEZE = " --enable-fuel-freeze"
    FG_CMD_OBJECTS = " --disable-random-objects --disable-ai-models --disable-ai-traffic"
    FG_CMD_SOUND = " --disable-sound"
    FG_CMD_WEATHER = " --turbulence=0.0 --disable-clouds --disable-clouds3d --fog-disable --disable-real-weather-fetch"
    FG_CMD_PROTOCOL_READ = " --generic=socket,out,0.5,127.0.0.1,9876,tcp,fg_read"
    FG_CMD_PROTOCOL_WRITE_RESET = " --generic=socket,in,0.5,127.0.0.1,9877,tcp,fg_write_reset"
    FG_CMD_PROTOCOL_WRITE_CONTROL = " --generic=socket,in,0.5,127.0.0.1,9878,tcp,fg_write_control"
    FG_CMD_PROTOCOL_WRITE_ENGINE = " --generic=socket,in,0.5,127.0.0.1,9879,tcp,fg_write_engine"
    FG_CMD_PROTOCOL_WRITE_GEAR = " --generic=socket,in,0.5,127.0.0.1,9880,tcp,fg_write_gear"

    # Launch string
    FG_LAUNCH_STRING = "\"" + FG_EXECUTABLE + "\"" \
                       + FG_CMD_FGROOT \
                       + FG_CMD_WINDOW \
                       + FG_CMD_AIRCRAFT \
                       + FG_CMD_AIRPORT \
                       + FG_CMD_TIME \
                       + FG_CMD_FREEZE \
                       + FG_CMD_OBJECTS \
                       + FG_CMD_SOUND \
                       + FG_CMD_WEATHER \
                       + FG_CMD_PROTOCOL_READ \
                       + FG_CMD_PROTOCOL_WRITE_RESET \
                       + FG_CMD_PROTOCOL_WRITE_CONTROL \
                       + FG_CMD_PROTOCOL_WRITE_ENGINE \
                       + FG_CMD_PROTOCOL_WRITE_GEAR

    @staticmethod
    def start_process():
        Thread(target=FGLaunch._start).start()

    @staticmethod
    def _start():
        print(FGLaunch.FG_LAUNCH_STRING)
        os.system("start cmd /c {0}".format(FGLaunch.FG_LAUNCH_STRING))


if __name__ == '__main__':
    FGLaunch.start_process()
