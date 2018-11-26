import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.const.dist_lookup import DistLookup


class PositionOvergroundBearingReward(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        reward_to_return = 0

        reward_to_return += self.calculate_bearing_reward(props['heading-deg'])

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.OVER_GROUND

    def calculate_bearing_reward(self, heading_deg):
        return RewardMultipliers.BEARING_MULTIPLIER * (DistLookup.RWY_BEARING_DEG -
                                                       (np.abs(DistLookup.RWY_BEARING_DEG - np.abs(heading_deg))))
