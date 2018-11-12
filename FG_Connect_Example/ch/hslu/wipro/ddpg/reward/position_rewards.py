import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionRewards(RewardInterface):
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

        # reward_to_return += self.calculate_distance_reward(props, dist_vector)
        # reward_to_return += self.calculate_pitch_reward(dist_vector)
        # reward_to_return += self.calculate_alt_reward(props, dist_vector)
        # reward_to_return += self.calculate_bearing_reward(dist_vector)
        # reward_to_return += self.calculate_discrepancy_reward(dist_vector)
        delta_alt_dif = dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        self._set_old_values(dist_vector)

        discrepancy_reset = self.determine_discrepancy_reset(dist_vector)
        if discrepancy_reset != 0:
            return RewardMultipliers.NEGATIVE_REWARD, True

        if delta_alt_dif > 2:
            return RewardMultipliers.NEGATIVE_REWARD, True

        if not DistCalc.check_if_plane_horizontally_is_on_runway(props):
            return RewardMultipliers.NEGATIVE_REWARD, True

        return reward_to_return, False

    def _set_old_values(self, dist_vector):
        self.old_dist_vector = dist_vector

    def calculate_distance_reward(self, props, dist_vector):
        if DistCalc.check_if_plane_is_on_runway(props):
            return 10 * RewardMultipliers.DISTANCE_MULTIPLIER
        return -(dist_vector.dist_m - self.old_dist_vector.dist_m)

    def calculate_alt_reward(self, props, dist_vector):
        delta_alt_dif = dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        if dist_vector.alt_diff_m < 20 and props['pitch-deg'] < -5:
            return -5 * RewardMultipliers.ALTITUDE_MULTIPLIER
        elif delta_alt_dif > 0:
            return -1 * delta_alt_dif * RewardMultipliers.ALTITUDE_MULTIPLIER
        else:
            return 0

    def calculate_bearing_reward(self, dist_vector):
        return RewardMultipliers.BEARING_MULTIPLIER * -(
                    np.abs(dist_vector.bearing_diff_deg) - np.abs(self.old_dist_vector.bearing_diff_deg))

    def calculate_pitch_reward(self, dist_vector):
        pitch_diff_deg = dist_vector.pitch_deg - self.old_dist_vector.pitch_deg
        if -3 < pitch_diff_deg < 0:
            return 10 * RewardMultipliers.PITCH_MULTIPLIER
        else:
            return -1 * np.abs(pitch_diff_deg) * RewardMultipliers.PITCH_MULTIPLIER

    def calculate_discrepancy_reward(self, dist_vector):
        reward = 0
        discrepancies = dist_vector.bound_discrepancy
        for discrepancy_key in discrepancies.keys():
            discrepancy_value = discrepancies[discrepancy_key]
            if discrepancy_value == 0:
                reward += 10 * RewardMultipliers.DISCREPANCY_MULTIPLIER
            else:
                reward -= np.abs(discrepancy_value) * RewardMultipliers.DISCREPANCY_MULTIPLIER

        return reward

    def determine_discrepancy_reset(self, dist_vector) -> float:
        discrepancies_reset = dist_vector.bound_discrepancy_reset
        for discrepancy_key in discrepancies_reset.keys():
            discrepancy_value = discrepancies_reset[discrepancy_key]
            if discrepancy_value != 0:
                return np.abs(discrepancy_value)
        return 0
