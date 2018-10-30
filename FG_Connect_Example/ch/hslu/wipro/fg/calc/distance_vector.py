
class DistanceVector:

    def __init__(self, bearing_diff_deg: float, dist_m: float, alt_diff_m: float, bound_discrepancy: dict):
        self.bearing_diff_deg = bearing_diff_deg
        self.dist_m = dist_m
        self.alt_diff_m = alt_diff_m
        self.bound_discrepancy = bound_discrepancy

    def copy(self):
        return DistanceVector(self.bearing_diff_deg, self.dist_m, self.alt_diff_m, self.bound_discrepancy)

    def print(self):
        print("bearing_diff_deg: {0}, dist_m: {1}, alt_discrepancy_m: {2}, bound_discrepancy: {3}"
              .format(self.bearing_diff_deg, self.dist_m, self.alt_diff_m, self.bound_discrepancy))
