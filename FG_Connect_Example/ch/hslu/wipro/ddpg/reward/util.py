class Util:
    _GEAR_KEYS = ['left-gear-damage', 'right-gear-damage', 'front-gear-damage']

    @staticmethod
    def has_gear_damage(props) -> bool:
        for damage_key in Util._GEAR_KEYS:
            if props[damage_key] == 'true':
                return True
        return False
