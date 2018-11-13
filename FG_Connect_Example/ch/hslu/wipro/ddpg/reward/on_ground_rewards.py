from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
import numpy as np

class OnGroundRewards(RewardInterface):

    def calculate_reward(self, props) -> (float, bool):
        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0

        if dist_vector.alt_diff_m < 1:
            # Round on zero decimals, so it won't return insane high reward (for example divided by 0.002)
            reward_to_return = RewardMultipliers.ON_GROUND_MULTIPLIER / np.round((props['airspeed-kt'] + 1), 1)

        return reward_to_return, False

    def reset(self):
        pass
