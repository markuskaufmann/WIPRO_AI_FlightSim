from ch.hslu.wipro.fg.const.dist_lookup import DistLookup
import math

from ch.hslu.wipro.fg.calc.distance_vector import DistanceVector
from ch.hslu.wipro.fg.properties.fg_property_boundaries import FGPropertyBoundaries


class DistCalc:

    @staticmethod
    def process_distance_vector(properties: dict) -> DistanceVector:
        plane_heading_deg = float(properties['heading-deg'])
        plane_alt_ft = float(properties['altitude-ft'])
        alt_m = DistCalc._feet_to_meters(plane_alt_ft)
        dist_m = DistCalc._dist_to_runway_pos(properties, DistLookup.RWY_LOC_TD_ZONE_START)
        bearing_diff_deg = DistLookup.RWY_BEARING_DEG - plane_heading_deg
        discrepancy_dict, discrepancy_dict_reset = FGPropertyBoundaries.verify_prop_boundaries(properties)
        alt_diff_m = FGPropertyBoundaries.verify_height_boundary(alt_m)
        dist_m_calc = dist_m if dist_m != 0 else 1e-10
        pitch_deg = math.degrees(math.atan(alt_diff_m / dist_m_calc))
        return DistanceVector(bearing_diff_deg, pitch_deg, dist_m, alt_diff_m, discrepancy_dict,
                              discrepancy_dict_reset)

    @staticmethod
    def check_if_plane_is_on_runway(props: dict) -> bool:
        return DistCalc._check_plane_on_runway_width(props) and DistCalc._check_plane_on_runway_length(props)

    @staticmethod
    def check_if_plane_is_on_runway_width(props: dict) -> bool:
        return DistCalc._check_plane_on_runway_width(props)

    @staticmethod
    def check_if_plane_is_on_runway_length(props: dict) -> bool:
        return DistCalc._check_plane_on_runway_length(props)

    @staticmethod
    def _check_plane_on_runway_width(props: dict) -> bool:
        lat_deg = props['latitude-deg']
        return DistLookup.RWY_WIDTH_BOUNDARY['right'] <= lat_deg <= DistLookup.RWY_WIDTH_BOUNDARY['left']

    @staticmethod
    def _check_plane_on_runway_length(props: dict) -> bool:
        lon_deg = props['longitude-deg']
        return DistLookup.RWY_LOC_TD_ZONE_START['lon'] <= lon_deg <= DistLookup.RWY_LOC_TD_ZONE_END['lon']

    @staticmethod
    def _dist_to_runway_pos(props: dict, runway_pos: dict) -> float:
        plane_lat_deg = float(props['latitude-deg'])
        plane_lon_deg = float(props['longitude-deg'])
        plane_lat_rad = math.radians(plane_lat_deg)
        plane_lon_rad = math.radians(plane_lon_deg)
        runway_lat_rad = math.radians(runway_pos['lat'])
        runway_lon_rad = math.radians(runway_pos['lon'])
        delta_lat_rad = plane_lat_rad - runway_lat_rad
        delta_lon_rad = plane_lon_rad - runway_lon_rad
        a = math.sin(delta_lat_rad / 2) ** 2 + math.cos(runway_lat_rad) \
            * math.cos(plane_lat_rad) \
            * math.sin(delta_lon_rad / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return DistLookup.EARTH_RADIUS_METER * c

    @staticmethod
    def _feet_to_meters(dist_ft: float) -> float:
        return dist_ft * DistLookup.FACT_FOOT_METER

    @staticmethod
    def _meters_to_feet(dist_m: float) -> float:
        return dist_m * DistLookup.FACT_METER_FOOT
