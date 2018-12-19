from queue import Queue


class FGDataOutput:

    _data = Queue()

    @staticmethod
    def set(data):
        FGDataOutput._data.put(data)

    @staticmethod
    def get():
        return FGDataOutput._data.get()

    @staticmethod
    def reinit():
        FGDataOutput._data = Queue()
