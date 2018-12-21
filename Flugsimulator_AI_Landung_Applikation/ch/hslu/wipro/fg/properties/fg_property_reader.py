from ch.hslu.wipro.fg.data.fg_data_input import FGDataInput


class FGPropertyReader:
    VAR_SEPARATOR = ","
    INNER_SEPARATOR = "="

    @staticmethod
    def get_properties():
        data = None
        while data is None or len(str(data).strip()) == 0 or data == 'None':
            data = FGDataInput.get()
        props = dict()
        if data is not None:
            values = data.split(FGPropertyReader.VAR_SEPARATOR)
            for val in values:
                val_split = val.split(FGPropertyReader.INNER_SEPARATOR)
                str_value = str(val_split[1])
                value = None
                try:
                    value = float(str_value)
                except ValueError:
                    value = str_value.strip('\r\n')
                props[val_split[0]] = value
        return props
