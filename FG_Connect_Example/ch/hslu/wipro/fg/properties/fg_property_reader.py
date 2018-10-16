
class FGPropertyReader:
    VAR_SEPARATOR = ","
    INNER_SEPARATOR = "="

    @staticmethod
    def get_properties(data: str):
        props = dict()
        if data is not None:
            values = data.split(FGPropertyReader.VAR_SEPARATOR)
            for val in values:
                val_split = val.split(FGPropertyReader.INNER_SEPARATOR)
                props[val_split[0]] = float(val_split[1])
        return props
