from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class TouchdownReward(RewardInterface):
    def __init__(self):
        self.plane_touched_ground = False

    def calculate_reward(self, observation) -> (float, bool):
        if self.plane_touched_ground:
            return 0, False

        dist_vector = DistCalc.process_distance_vector(observation)
        reward_to_return = 0

        if 20 > dist_vector.dist_m > -20 and dist_vector.alt_m < 5:
            self.plane_touched_ground = True
            reward_to_return = 1000

        elif dist_vector.alt_m < 5:
            self.plane_touched_ground = True
            reward_to_return = -150

        return reward_to_return, False

    def reset(self):
        self.plane_touched_ground = False