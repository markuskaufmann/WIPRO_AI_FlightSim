import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionDiscrepancyResetPenalty(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        reward_to_return = 0
        dist_vector = DistCalc.process_distance_vector(props)

        discrepancy_reset = self.determine_discrepancy_reset(dist_vector)
        if discrepancy_reset != 0:
            return RewardMultipliers.NEGATIVE_REWARD, True

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.COMMON

    def determine_discrepancy_reset(self, dist_vector) -> float:
        discrepancies_reset = dist_vector.bound_discrepancy_reset
        for discrepancy_key in discrepancies_reset.keys():
            discrepancy_value = discrepancies_reset[discrepancy_key]
            if discrepancy_value != 0:
                return np.abs(discrepancy_value)
        return 0
