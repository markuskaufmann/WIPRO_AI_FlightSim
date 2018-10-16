from ch.hslu.wipro.fg.calc.dist_lookup import DistLookup
import math

from ch.hslu.wipro.fg.calc.distance_vector import DistanceVector


class DistCalc:

    @staticmethod
    def process_distance_vector(plane_lat_deg: float, plane_lon_deg: float, plane_alt_ft: float) -> DistanceVector:
        alt_m = DistCalc.feet_to_meters(plane_alt_ft)
        plane_lat_rad = math.radians(plane_lat_deg)
        plane_lon_rad = math.radians(plane_lon_deg)
        runway_lat_rad = DistLookup.RWY_LOC_TD_ZONE_START[0]
        runway_lon_rad = DistLookup.RWY_LOC_TD_ZONE_START[1]
        delta_lat_rad = plane_lat_rad - runway_lat_rad
        delta_lon_rad = plane_lon_rad - runway_lon_rad
        a = math.sin(delta_lat_rad / 2) ** 2 + math.cos(runway_lat_rad) \
                * math.cos(plane_lat_rad) \
                * math.sin(delta_lon_rad / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist_m = DistLookup.EARTH_RADIUS_METER * c
        bearing_y = math.sin(delta_lon_rad) * math.cos(plane_lat_rad)
        bearing_x = math.cos(runway_lat_rad) * math.sin(plane_lat_rad) - math.sin(runway_lat_rad) * math.cos(plane_lat_rad) \
                    * math.cos(delta_lon_rad)
        bearing_deg = math.degrees(math.atan2(bearing_y, bearing_x))
        return DistanceVector(bearing_deg, dist_m, alt_m)

    @staticmethod
    def feet_to_meters(dist_ft: float) -> float:
        return dist_ft * DistLookup.FACT_FOOT_METER

    @staticmethod
    def meters_to_feet(dist_m: float) -> float:
        return dist_m * DistLookup.FACT_METER_FOOT
