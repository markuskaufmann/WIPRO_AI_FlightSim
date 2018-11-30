import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.ddpg.reward.util import Util


class OnGroundRewards(RewardInterface):

    def calculate_reward(self, props) -> (float, bool):

        # Round on one decimal, so it won't return insane high reward (for example divided by 0.0002)
        reward_to_return = -np.abs(RewardMultipliers.ON_GROUND_MULTIPLIER * (props['airspeed-kt'] + 1))

        return reward_to_return, False

    def reset(self):
        pass

    def get_state(self) -> int:
        return RewardState.ON_GROUND
