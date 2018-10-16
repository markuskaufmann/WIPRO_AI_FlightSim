from threading import Lock


class FGDataInput:
    _data: str = None
    _lock = Lock()

    @staticmethod
    def set(data: str):
        with FGDataInput._lock:
            FGDataInput._data = data

    @staticmethod
    def get() -> str:
        with FGDataInput._lock:
            data = str(FGDataInput._data)
            FGDataInput._data = None
            return data
