from ch.hslu.wipro.fg.const.dist_lookup import DistLookup
import math

from ch.hslu.wipro.fg.calc.distance_vector import DistanceVector
from ch.hslu.wipro.fg.properties.fg_property_boundaries import FGPropertyBoundaries


class DistCalc:

    @staticmethod
    def process_distance_vector(properties: dict) -> DistanceVector:
        plane_lat_deg = float(properties['latitude-deg'])
        plane_lon_deg = float(properties['longitude-deg'])
        plane_heading_deg = float(properties['heading-deg'])
        plane_alt_ft = float(properties['altitude-ft'])
        alt_m = DistCalc.feet_to_meters(plane_alt_ft)
        plane_lat_rad = math.radians(plane_lat_deg)
        plane_lon_rad = math.radians(plane_lon_deg)
        runway_lat_rad = math.radians(DistLookup.RWY_LOC_TD_ZONE_START['lat'])
        runway_lon_rad = math.radians(DistLookup.RWY_LOC_TD_ZONE_START['lon'])
        delta_lat_rad = plane_lat_rad - runway_lat_rad
        delta_lon_rad = plane_lon_rad - runway_lon_rad
        a = math.sin(delta_lat_rad / 2) ** 2 + math.cos(runway_lat_rad) \
            * math.cos(plane_lat_rad) \
            * math.sin(delta_lon_rad / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_m = DistLookup.EARTH_RADIUS_METER * c
        bearing_diff_deg = DistLookup.RWY_BEARING_DEG - plane_heading_deg
        discrepancy_dict, discrepancy_dict_reset = FGPropertyBoundaries.verify_prop_boundaries(properties)
        alt_diff_m = FGPropertyBoundaries.verify_height_boundary(alt_m)
        return DistanceVector(bearing_diff_deg, dist_m, alt_diff_m, discrepancy_dict, discrepancy_dict_reset)

    @staticmethod
    def feet_to_meters(dist_ft: float) -> float:
        return dist_ft * DistLookup.FACT_FOOT_METER

    @staticmethod
    def meters_to_feet(dist_m: float) -> float:
        return dist_m * DistLookup.FACT_METER_FOOT
