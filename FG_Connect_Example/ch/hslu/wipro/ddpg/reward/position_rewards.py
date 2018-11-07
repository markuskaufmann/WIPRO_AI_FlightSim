import numpy as np

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

        reward_to_return += self.calculate_distance_reward(props, dist_vector)
        reward_to_return += self.calculate_pitch_reward(dist_vector)
        reward_to_return += self.calculate_alt_reward(props, dist_vector)
        reward_to_return += self.calculate_bearing_reward(dist_vector)
        reward_to_return += self.calculate_discrepancy_reward(dist_vector)

        self._set_old_values(dist_vector)

        discrepancy_reset = self.determine_discrepancy_reset(dist_vector)
        if discrepancy_reset != 0:
            return -10000, True

        return reward_to_return, False

    def _set_old_values(self, dist_vector):
        self.old_dist_vector = dist_vector

    def calculate_distance_reward(self, props, dist_vector):
        if DistCalc.check_if_plane_is_on_runway(props):
            return 500
        return -(dist_vector.dist_m - self.old_dist_vector.dist_m)

    def calculate_alt_reward(self, props, dist_vector):
        delta_alt_dif = dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        if dist_vector.alt_diff_m < 20 and props['pitch-deg'] < -5:
            return -500
        elif delta_alt_dif > 0:
            return -100 * delta_alt_dif
        else:
            return 0

    def calculate_bearing_reward(self, dist_vector):
        return -10 * (np.abs(dist_vector.bearing_diff_deg) - np.abs(self.old_dist_vector.bearing_diff_deg))

    def calculate_pitch_reward(self, dist_vector):
        pitch_diff_deg = dist_vector.pitch_deg - self.old_dist_vector.pitch_deg
        if -3 < pitch_diff_deg < 0:
            return 1000
        else:
            return -100 * np.abs(pitch_diff_deg)

    def calculate_discrepancy_reward(self, dist_vector):
        reward = 0
        discrepancies = dist_vector.bound_discrepancy
        for discrepancy_key in discrepancies.keys():
            discrepancy_value = discrepancies[discrepancy_key]
            if discrepancy_value == 0:
                reward += 100
            else:
                reward -= np.abs(discrepancy_value)
        if reward < 0:
            reward *= 30
        return reward

    def determine_discrepancy_reset(self, dist_vector) -> float:
        discrepancies_reset = dist_vector.bound_discrepancy_reset
        for discrepancy_key in discrepancies_reset.keys():
            discrepancy_value = discrepancies_reset[discrepancy_key]
            if discrepancy_value != 0:
                return np.abs(discrepancy_value)
        return 0
