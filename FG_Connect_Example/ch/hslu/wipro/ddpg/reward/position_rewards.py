import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
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

        delta_alt_dif = dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        self._set_old_values(dist_vector)

        discrepancy_reset = self.determine_discrepancy_reset(dist_vector)
        if discrepancy_reset != 0:
            return RewardMultipliers.NEGATIVE_REWARD, True

        if delta_alt_dif > 0.1:
            return RewardMultipliers.NEGATIVE_REWARD, True

        if not DistCalc.check_if_plane_is_on_runway_width(props):
            return RewardMultipliers.NEGATIVE_REWARD, True

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.COMMON

    def _set_old_values(self, dist_vector):
        self.old_dist_vector = dist_vector

    def determine_discrepancy_reset(self, dist_vector) -> float:
        discrepancies_reset = dist_vector.bound_discrepancy_reset
        for discrepancy_key in discrepancies_reset.keys():
            discrepancy_value = discrepancies_reset[discrepancy_key]
            if discrepancy_value != 0:
                return np.abs(discrepancy_value)
        return 0
