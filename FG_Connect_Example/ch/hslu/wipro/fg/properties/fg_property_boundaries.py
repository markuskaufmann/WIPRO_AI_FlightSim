import numpy as np


class FGPropertyBoundaries:

    _BOUNDARY_MAP = {
        'pitch-deg': [-60, 60],
        'roll-deg': [-20, 20],
        'heading-deg': [70, 110]
    }

    @staticmethod
    def verify_prop_boundaries(props: dict) -> float:
        total_discrepancy = 0
        for bound_key in FGPropertyBoundaries._BOUNDARY_MAP.keys():
            bound_range = FGPropertyBoundaries._BOUNDARY_MAP[bound_key]
            prop_val = props[bound_key]
            discrepancy = 0
            if prop_val < bound_range[0]:
                discrepancy = np.abs(bound_range[0] - prop_val)
            elif prop_val > bound_range[1]:
                discrepancy = np.abs(prop_val - bound_range[1])
            total_discrepancy += discrepancy
        return total_discrepancy
