from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionAltitudeReward(RewardInterface):
    def __init__(self):
        self.old_dist_vector = None

    def reset(self):
        self.old_dist_vector = None

    def calculate_reward(self, props) -> (float, bool):
        # add vector to observation space
        reward_to_return = 0
        dist_vector = DistCalc.process_distance_vector(props)
        print("Height: {0}, Pitch: {1}, Speed: {2}".format(dist_vector.alt_diff_m, props["pitch-deg"],
                                                           props["airspeed-kt"]))
        if self.old_dist_vector is None:
            self._set_old_values(dist_vector)
            return reward_to_return, False

        delta_alt_diff = dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        self._set_old_values(dist_vector)

        if delta_alt_diff > 0.3:
            return RewardMultipliers.NEGATIVE_REWARD / 10, False

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.COMMON

    def _set_old_values(self, dist_vector):
        self.old_dist_vector = dist_vector
