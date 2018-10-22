from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader


class FGPropertyConverter:

    _ACTION_MAP = {
        0: 'throttle',
        1: 'mixture',
        2: 'aileron',
        3: 'elevator',
        4: 'rudder',
        5: 'flaps'
    }

    _CONVERSION_MAP = {
        'aileron': (0.1, -1, 1),
        'elevator': (0.1, -1, 1),
        'rudder': (0.1, -1, 1),
        'flaps': (0.1, -1, 1),
        'throttle': (0.05, 0, 1),
        'mixture': (0.05, 0, 1)
    }

    @staticmethod
    def process_actions(actions) -> dict:
        print(actions)
        result = dict()
        if actions is None or len(actions) == 0:
            return result
        properties = FGPropertyReader.get_properties()
        for i in range(0, len(actions)):
            action = FGPropertyConverter._ACTION_MAP[i]
            conversion = FGPropertyConverter._CONVERSION_MAP[action]
            converted_value = properties[action] + (conversion[0] * actions[i])
            if converted_value < conversion[1]:
                converted_value = conversion[1]
            elif converted_value > conversion[2]:
                converted_value = conversion[2]
            result[action] = converted_value
        print(result)
        return result
