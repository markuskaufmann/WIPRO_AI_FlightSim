import math


class DistLookup:
    EARTH_RADIUS_METER = 6371*10**3

    FACT_FOOT_METER = 0.3048
    FACT_METER_FOOT = FACT_FOOT_METER**-1

    ARC_HEIGHT_METER = 1.339

    RWY_BEARING_DEG = 89.9
    RWY_LOC_TD_ZONE_START = (math.radians(21.325269), math.radians(-157.941620))
    RWY_LOC_TD_ZONE_END = (math.radians(21.325269), math.radians(-157.934269))
    RWY_LOC_AIMING_ZONE = (math.radians(21.325269), math.radians(-157.940038))
