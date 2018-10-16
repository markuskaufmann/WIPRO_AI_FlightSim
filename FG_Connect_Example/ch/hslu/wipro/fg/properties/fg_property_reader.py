from ch.hslu.wipro.fg.io.fg_io_handler import FGIOHandler


class FGPropertyReader:
    VAR_SEPARATOR = ","
    INNER_SEPARATOR = "="

    @staticmethod
    def get_properties():
        data = FGIOHandler.read()
        while data is None or len(str(data).strip()) == 0 or data == 'None':
            continue
        props = dict()
        if data is not None:
            values = data.split(FGPropertyReader.VAR_SEPARATOR)
            for val in values:
                val_split = val.split(FGPropertyReader.INNER_SEPARATOR)
                props[val_split[0]] = float(val_split[1])
        return props
