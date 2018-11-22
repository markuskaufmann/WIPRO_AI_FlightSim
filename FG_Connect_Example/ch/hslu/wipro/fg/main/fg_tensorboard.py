
import os

PATH_DIR = "C:\\Users\\[USER]\\Documents\\FG_Logs_Graphs\\[OPEN_AI_DIR]\\tb"

VAR_USER_MK = "MK"
VAR_USER_CU = "Cyrille"
VAR_USER_LB = "Student"

VAR_USER_CURRENT = VAR_USER_MK
VAR_OPEN_AI_DIR_CURRENT = "openai-2018-11-13-20-43-43-405759"

# PATH_PREFIX_MK = "C:\\Users\\MK\\Documents\\Study_Repos\\WIPRO_AI_FlightSim"
# PATH_PREFIX_CU = "C:\\Users\\Cyrille\\Documents\\GitHub\\WIPRO_AI_FlightSim"

# PATH_PREFIX = PATH_PREFIX_MK

# PATH_POSTFIX = "\\FG_Connect_Example\\ch\\hslu\\wipro\\fg\\main\\results\\tf_ddpg"


def show_tensorboard():
    # path = PATH_PREFIX + PATH_POSTFIX
    path = PATH_DIR.replace('[USER]', VAR_USER_CURRENT).replace('[OPEN_AI_DIR]', VAR_OPEN_AI_DIR_CURRENT)
    os.system('tensorboard --logdir=' + path)


if __name__ == '__main__':
    show_tensorboard()
