
from tensorflow.python.client import device_lib


def list_local_devices():
    print(device_lib.list_local_devices())


if __name__ == '__main__':
    list_local_devices()
