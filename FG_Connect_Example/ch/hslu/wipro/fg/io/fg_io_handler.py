import threading


class FGIOHandler:
    OUTPUT = None
    INPUT = None
    LOCK = threading.Lock()

    @staticmethod
    def write(data):
        FGIOHandler.OUTPUT = data

    @staticmethod
    def read():
        FGIOHandler.LOCK.acquire()
        input_data = str(FGIOHandler.INPUT)
        FGIOHandler.INPUT = None
        FGIOHandler.LOCK.release()
        return str(input_data)
