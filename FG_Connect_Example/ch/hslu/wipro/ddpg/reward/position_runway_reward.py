import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionRunwayReward(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        if not DistCalc.check_if_plane_is_on_runway_width(props):
            return RewardMultipliers.NEGATIVE_REWARD, True
        return 0, False

    def get_state(self) -> int:
        return RewardState.COMMON
