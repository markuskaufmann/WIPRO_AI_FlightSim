from ch.hslu.wipro.ddpg.spaces.Box import Box
from ch.hslu.wipro.ddpg.utility import SpaceDefiner
from ch.hslu.wipro.fg.calc.distance_vector import DistanceVector


class FGPropertyNormalizer:

    _NORM_BOUNDARIES = {
        'airspeed-kt': [0, 250],
        'alt_m': [-50, 10000],
        'dist_m': [-10000, 10000],
        'bearing_deg': [-90, 90],
        'discrepancy_pitch_deg': [-90, 90],
        'discrepancy_roll_deg': [-90, 90],
        'discrepancy_heading_deg': [0, 180]
    }

    @staticmethod
    def perform_normalization(props: dict, dist_vector: DistanceVector):
        norm_props = dict()
        norm_dist_vector = dist_vector.copy()
        for observation_space in SpaceDefiner.DefaultObservationSpaces:
            key = observation_space[1]
            box = observation_space[2]
            boundaries = None
            try:
                boundaries = FGPropertyNormalizer._NORM_BOUNDARIES[key]
            except KeyError:
                boundaries = [box.low, box.high]
            if key == 'alt_m':
                norm_dist_vector.alt_diff_m = FGPropertyNormalizer._normalize_float(dist_vector.alt_diff_m,
                                                                                    boundaries, box)
            elif key == 'dist_m':
                norm_dist_vector.dist_m = FGPropertyNormalizer._normalize_float(dist_vector.dist_m,
                                                                                boundaries, box)
            elif key == 'bearing_deg':
                norm_dist_vector.bearing_diff_deg = FGPropertyNormalizer._normalize_float(dist_vector.bearing_diff_deg,
                                                                                          boundaries, box)
            elif key == 'discrepancy_pitch_deg':
                norm_dist_vector.bound_discrepancy['pitch-deg'] = \
                    FGPropertyNormalizer._normalize_float(dist_vector.bound_discrepancy['pitch-deg'], boundaries, box)
            elif key == 'discrepancy_roll_deg':
                norm_dist_vector.bound_discrepancy['roll-deg'] = \
                    FGPropertyNormalizer._normalize_float(dist_vector.bound_discrepancy['roll-deg'], boundaries, box)
            elif key == 'discrepancy_heading_deg':
                norm_dist_vector.bound_discrepancy['heading-deg'] = \
                    FGPropertyNormalizer._normalize_float(dist_vector.bound_discrepancy['heading-deg'], boundaries, box)
            else:
                val = props[key]
                norm_val = None
                try:
                    val = float(val)
                    norm_val = FGPropertyNormalizer._normalize_float(val, boundaries, box)
                except ValueError:
                    norm_val = FGPropertyNormalizer._normalize_str_bool(str(val))
                norm_props[key] = norm_val
        return norm_props, norm_dist_vector

    @staticmethod
    def _normalize_float(prop_val_float: float, min_max: [], box: Box) -> float:
        fact = box.high - box.low
        add = box.low
        return fact * ((prop_val_float - min_max[0]) / (min_max[1] - min_max[0])) + add

    @staticmethod
    def _normalize_str_bool(prop_val_str_bool: str) -> float:
        if prop_val_str_bool == 'true':
            return 1
        else:
            return 0
