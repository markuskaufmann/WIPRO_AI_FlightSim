import subprocess
from threading import Thread


class FGLaunch:
    # FG Location
    FG_DIR_MK = "C:\\Users\\MK\\Documents\\FlightGear_Root\\FlightGear 2018.2.2"
    FG_DIR_CU = "C:\\Program Files\\FlightGear 2018.2.2"
    FG_DIR_LB = "C:\\Users\\Student\\Documents\\WIPRO_FlightSim\\FlightGear 2018.2.2"

    FG_DIR = FG_DIR_MK

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

    # Launch string
    # FG_LAUNCH_STRING = "\"" + FG_EXECUTABLE + "\"" \
    #                    + FG_CMD_FGROOT \
    #                    + FG_CMD_WINDOW \
    #                    + FG_CMD_AIRCRAFT \
    #                    + FG_CMD_AIRPORT \
    #                    + FG_CMD_TIME \
    #                    + FG_CMD_FREEZE \
    #                    + FG_CMD_OBJECTS \
    #                    + FG_CMD_SOUND \
    #                    + FG_CMD_WEATHER \
    #                    + FG_CMD_PROTOCOL_READ \
    #                    + FG_CMD_PROTOCOL_WRITE_RESET \
    #                    + FG_CMD_PROTOCOL_WRITE_CONTROL

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
                      FG_ARGS_PROTOCOL_WRITE_CONTROL]

    FG_LAUNCH = [FG_EXECUTABLE, FG_LAUNCH_ARGS]

    @staticmethod
    def start_process():
        Thread(target=FGLaunch._start).start()

    @staticmethod
    def _start():
        print(FGLaunch.FG_LAUNCH)
        subprocess.call(FGLaunch.FG_LAUNCH, stdin=None, stdout=None, stderr=None, shell=False)


if __name__ == '__main__':
    FGLaunch.start_process()
