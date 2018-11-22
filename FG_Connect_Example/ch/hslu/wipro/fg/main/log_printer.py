import time


class LogPrinter(object):

    def __init__(self, *fd):
        self._fd = fd

    def write(self, obj):
        if obj is None:
            return
        str_obj = str(obj).strip().strip('\n')
        if str_obj == '':
            return
        ts = time.strftime("%d.%m.%Y %H:%M:%S")
        for fd in self._fd:
            fd.write(ts + " - " + str_obj + "\r\n")
            fd.flush()
