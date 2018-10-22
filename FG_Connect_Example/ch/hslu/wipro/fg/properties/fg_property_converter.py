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
        'aileron': {'fact': 0.1, 'val_range_alg': [-1, 1], 'val_range_fg': [-1, 1]},
        'elevator': {'fact': 0.1, 'val_range_alg': [-1, 1], 'val_range_fg': [-1, 1]},
        'rudder': {'fact': 0.1, 'val_range_alg': [-1, 1], 'val_range_fg': [-1, 1]},
        'flaps': {'fact': 0.1, 'val_range_alg': [-1, 1], 'val_range_fg': [0, 1]},
        'throttle': {'fact': 0.05, 'val_range_alg': [-1, 1], 'val_range_fg': [0, 1]},
        'mixture': {'fact': 0.05, 'val_range_alg': [-1, 1], 'val_range_fg': [0, 1]}
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
            conversion_map = FGPropertyConverter._CONVERSION_MAP[action]
            alg_action = FGPropertyConverter._check_val_in_range(conversion_map['val_range_alg'], actions[i])
            converted_value = properties[action] + (conversion_map['fact'] * alg_action)
            fg_action = FGPropertyConverter._check_val_in_range(conversion_map['val_range_fg'], converted_value)
            result[action] = fg_action
        print(result)
        return result

    @staticmethod
    def _check_val_in_range(arr_range, val):
        if val < arr_range[0]:
            val = arr_range[0]
        elif val > arr_range[1]:
            val = arr_range[1]
        return val
