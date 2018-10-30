import numpy as np

from ch.hslu.wipro.fg.const.dist_lookup import DistLookup


class FGPropertyBoundaries:

    _BOUNDARY_MAP = {
        'pitch-deg': [-60, 60],
        'roll-deg': [-20, 20],
        'heading-deg': [70, 110]
    }

    _HEIGHT_BOUNDARY = [DistLookup.ARC_HEIGHT_METER - 0.001,
                        DistLookup.ARC_HEIGHT_METER + 0.001]

    @staticmethod
    def verify_prop_boundaries(props: dict) -> dict:
        discrepancy_dict = dict()
        for bound_key in FGPropertyBoundaries._BOUNDARY_MAP.keys():
            bound_range = FGPropertyBoundaries._BOUNDARY_MAP[bound_key]
            prop_val = props[bound_key]
            discrepancy_dict[bound_key] = FGPropertyBoundaries._compute_discrepancy(prop_val, bound_range)
        return discrepancy_dict

    @staticmethod
    def verify_height_boundary(alt_meter: float) -> float:
        return FGPropertyBoundaries._compute_discrepancy(alt_meter,
                                                         FGPropertyBoundaries._HEIGHT_BOUNDARY)

    @staticmethod
    def _compute_discrepancy(val: float, boundary: []) -> float:
        if val < boundary[0]:
            return np.abs(boundary[0]) - np.abs(val)
        elif val > boundary[1]:
            return np.abs(val) - np.abs(boundary[1])
        return 0
