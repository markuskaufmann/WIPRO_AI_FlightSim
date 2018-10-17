
class DistanceVector:

    def __init__(self, bearing_diff_deg: float, dist_m: float, alt_m: float):
        self.bearing_diff_deg = bearing_diff_deg
        self.dist_m = dist_m
        self.alt_m = alt_m

    def print(self):
        print("bearing_diff_deg: {0}, dist_m: {1}, alt_m: {2}".format(self.bearing_diff_deg, self.dist_m, self.alt_m))
