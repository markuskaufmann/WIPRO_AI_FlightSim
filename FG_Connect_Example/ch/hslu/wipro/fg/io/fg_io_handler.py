from queue import Queue


class FGIOHandler:
    OUTPUT = None
    INPUT = None

    @staticmethod
    def write(data):
        FGIOHandler.OUTPUT = data

    @staticmethod
    def read():
        return FGIOHandler.INPUT
