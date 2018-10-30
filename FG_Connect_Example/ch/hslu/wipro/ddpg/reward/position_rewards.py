from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionRewards(RewardInterface):

    """
                if key == 'alt_m':
                observation.append(dist_vector.alt_m)
            elif key == 'dist_m':
                observation.append(dist_vector.dist_m)
            elif key == 'bearing_deg':
                observation.append(dist_vector.bearing_diff_deg)
            elif key == 'discrepancy':
                observation.append(dist_vector.bound_discrepancy)
    """

    def __init__(self):
        self.old_dist_vector = None

    def reset(self):
        self.old_dist_vector = None

    def calculate_reward(self, props) -> (float, bool):
        # add vector to observation space
        reward_to_return = 0
        dist_vector = DistCalc.process_distance_vector(props)

        if self.old_dist_vector is None:
            self._set_old_values(dist_vector)
            return reward_to_return, False

        reward_to_return += self.calculate_distance_reward(dist_vector)
        reward_to_return += self.calculate_alt_reward(dist_vector)
        reward_to_return += self.calculate_bearing_reward(dist_vector)
        reward_to_return += self.calculate_discrepancy_reward(dist_vector)

        self._set_old_values(dist_vector)

        return reward_to_return, False

    def _set_old_values(self, dist_vector):
        self.old_dist_vector = dist_vector

    def calculate_distance_reward(self, dist_vector):
        return -(dist_vector.dist_m - self.old_dist_vector.dist_m)

    def calculate_alt_reward(self, dist_vector):
        return -(dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m)

    def calculate_bearing_reward(self, dist_vector):
        return 0

    def calculate_discrepancy_reward(self, dist_vector):
        return 0
