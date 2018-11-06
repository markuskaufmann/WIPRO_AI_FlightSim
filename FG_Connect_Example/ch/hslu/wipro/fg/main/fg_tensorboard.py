
import os

PATH_PREFIX_MK = "C:\\Users\\MK\\Documents\\Study_Repos\\WIPRO_AI_FlightSim"
PATH_PREFIX_CU = "C:\\Users\\Cyrille\\Documents\\GitHub\\WIPRO_AI_FlightSim"

PATH_PREFIX = PATH_PREFIX_MK

PATH_POSTFIX = "\\FG_Connect_Example\\ch\\hslu\\wipro\\fg\\main\\results\\tf_ddpg"


def show_tensorboard():
    path = PATH_PREFIX + PATH_POSTFIX
    os.system('tensorboard --logdir=' + path)


if __name__ == '__main__':
    show_tensorboard()
