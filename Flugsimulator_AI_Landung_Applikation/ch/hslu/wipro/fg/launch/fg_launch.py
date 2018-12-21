import os
import subprocess
import time
from threading import Thread


class FGLaunch:
    # FG Location
    FG_DIR_MK = "C:\\Users\\MK\\Documents\\FlightGear_Root\\FlightGear 2018.2.2"
    FG_DIR_CU = "C:\\Program Files\\FlightGear 2018.2.2"
    FG_DIR_LB = "C:\\Users\\Student\\Documents\\WIPRO_FlightSim\\FlightGear 2018.2.2"

    FG_DIR = FG_DIR_CU

    # Executable
    FG_EXECUTABLE = FG_DIR + "\\bin\\fgfs.exe"
    FG_DATA = FG_DIR + "\\data"

    # Commands
    FG_ARGS_FGROOT = " --fg-root=\"" + FG_DATA + "\""
    FG_ARGS_WINDOW = " --geometry=640x480"
    FG_ARGS_SPLASH = " --disable-splash-screen"
    FG_ARGS_AIRCRAFT = " --aircraft=c172p"
    FG_ARGS_AIRPORT_ID = " --airport=PHNL"
    FG_ARGS_AIRPORT_RW = " --runway=08L"
    FG_ARGS_TIME = " --timeofday=noon"
    FG_ARGS_FUEL_FREEZE = " --enable-fuel-freeze"
    FG_ARGS_AUTOCD = " --enable-auto-coordination"
    FG_ARGS_OBJECTS = " --disable-random-objects"
    FG_ARGS_AI_MODELS = " --disable-ai-models"
    FG_ARGS_AI_TRAFFIC = " --disable-ai-traffic"
    FG_ARGS_SOUND = " --disable-sound"
    FG_ARGS_WEATHER_TURB = " --turbulence=0.0"
    FG_ARGS_WEATHER_CL = " --disable-clouds"
    FG_ARGS_WEATHER_CL3D = " --disable-clouds3d"
    FG_ARGS_WEATHER_FOG = " --fog-disable"
    FG_ARGS_WEATHER_FETCH = " --disable-real-weather-fetch"
    FG_ARGS_PROTOCOL_READ = " --generic=socket,out,5,127.0.0.1,9876,tcp,fg_read"
    FG_ARGS_PROTOCOL_WRITE_RESET = " --generic=socket,in,5,127.0.0.1,9877,tcp,fg_write_reset"
    FG_ARGS_PROTOCOL_WRITE_CONTROL = " --generic=socket,in,5,127.0.0.1,9878,tcp,fg_write_control"
    FG_ARGS_PROTOCOL_WRITE_GEAR = " --generic=socket,in,5,127.0.0.1,9879,tcp,fg_write_gear"

    # Parameters
    FG_LAUNCH_ARGS = [FG_ARGS_FGROOT,
                      FG_ARGS_WINDOW,
                      FG_ARGS_SPLASH,
                      FG_ARGS_AIRCRAFT,
                      FG_ARGS_AIRPORT_ID,
                      FG_ARGS_AIRPORT_RW,
                      FG_ARGS_TIME,
                      FG_ARGS_FUEL_FREEZE,
                      FG_ARGS_AUTOCD,
                      FG_ARGS_OBJECTS,
                      FG_ARGS_AI_MODELS,
                      FG_ARGS_AI_TRAFFIC,
                      FG_ARGS_SOUND,
                      FG_ARGS_WEATHER_TURB,
                      FG_ARGS_WEATHER_CL,
                      FG_ARGS_WEATHER_CL3D,
                      FG_ARGS_WEATHER_FOG,
                      FG_ARGS_WEATHER_FETCH,
                      FG_ARGS_PROTOCOL_READ,
                      FG_ARGS_PROTOCOL_WRITE_RESET,
                      FG_ARGS_PROTOCOL_WRITE_CONTROL,
                      FG_ARGS_PROTOCOL_WRITE_GEAR]

    FG_LAUNCH = [FG_EXECUTABLE, FG_LAUNCH_ARGS]

    _LOG_FILE = None

    @staticmethod
    def start_process(fg_log_file):
        FGLaunch._LOG_FILE = fg_log_file
        Thread(target=FGLaunch._start).start()

    @staticmethod
    def _start():
        print("FG Launch params: {0}".format(FGLaunch.FG_LAUNCH))
        print("FG Logfile: {0}".format(os.path.basename(FGLaunch._LOG_FILE.name)))
        subprocess.call(FGLaunch.FG_LAUNCH,
                        stdin=None,
                        stdout=FGLaunch._LOG_FILE,
                        stderr=subprocess.STDOUT,
                        shell=False)


if __name__ == '__main__':
    log_file_name = time.strftime("%Y%m%d_%H%M%S") + "_fg_manual_launch.log"
    log_file = open("../main/logs/" + log_file_name, 'w')
    FGLaunch.start_process(log_file)
