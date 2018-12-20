from datetime import datetime


class LogPrinter(object):

    def __init__(self, *fd):
        self._fd = fd

    def write(self, obj):
        if obj is None:
            return
        str_obj = str(obj)
        prefix = "\n" if str_obj.startswith("\n") else ""
        str_obj = str_obj.strip()
        if str_obj == '':
            return
        ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")
        suffix = "\n" if not str_obj.endswith("\n") else ""
        for fd in self._fd:
            fd.write(ts + " - " + prefix + str_obj + suffix)
            fd.flush()
