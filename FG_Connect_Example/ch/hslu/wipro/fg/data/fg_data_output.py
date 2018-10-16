from queue import Queue
from threading import Lock


class FGDataOutput:
    _data = Queue()
    _lock = Lock()

    @staticmethod
    def set(data: str):
        with FGDataOutput._lock:
            FGDataOutput._data.put(data)

    @staticmethod
    def get() -> str:
        with FGDataOutput._lock:
            return str(FGDataOutput._data.get())
