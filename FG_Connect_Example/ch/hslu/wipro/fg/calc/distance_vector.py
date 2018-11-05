
class DistanceVector:

    def __init__(self, bearing_diff_deg: float, dist_m: float, alt_diff_m: float, bound_discrepancy: dict,
                 bound_discrepancy_reset: dict):
        self.bearing_diff_deg = bearing_diff_deg
        self.dist_m = dist_m
        self.alt_diff_m = alt_diff_m
        self.bound_discrepancy = bound_discrepancy
        self.bound_discrepancy_reset = bound_discrepancy_reset

    def copy(self):
        return DistanceVector(self.bearing_diff_deg, self.dist_m, self.alt_diff_m, self.bound_discrepancy,
                              self.bound_discrepancy_reset)

    def print(self):
        print("bearing_diff_deg: {0}, dist_m: {1}, alt_discrepancy_m: {2}, bound_discrepancy: {3}, "
              "bound_discrepancy_reset: {4}"
              .format(self.bearing_diff_deg, self.dist_m, self.alt_diff_m, self.bound_discrepancy,
                      self.bound_discrepancy_reset))
