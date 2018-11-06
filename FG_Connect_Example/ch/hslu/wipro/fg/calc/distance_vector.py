
class DistanceVector:

    def __init__(self, bearing_diff_deg: float, pitch_deg: float, dist_m: float, alt_diff_m: float,
                 bound_discrepancy: dict, bound_discrepancy_reset: dict):
        self.bearing_diff_deg = bearing_diff_deg
        self.pitch_deg = pitch_deg
        self.dist_m = dist_m
        self.alt_diff_m = alt_diff_m
        self.bound_discrepancy = bound_discrepancy
        self.bound_discrepancy_reset = bound_discrepancy_reset

    def copy(self):
        return DistanceVector(self.bearing_diff_deg, self.pitch_deg, self.dist_m, self.alt_diff_m,
                              self.bound_discrepancy, self.bound_discrepancy_reset)

    def print(self):
        print("bearing_diff_deg: {0}, pitch_deg: {1}, dist_m: {2}, alt_discrepancy_m: {3}, "
              "bound_discrepancy: {4}, bound_discrepancy_reset: {5}"
              .format(self.bearing_diff_deg, self.pitch_deg, self.dist_m, self.alt_diff_m,
                      self.bound_discrepancy, self.bound_discrepancy_reset))
