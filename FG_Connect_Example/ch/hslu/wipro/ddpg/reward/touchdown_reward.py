from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class TouchdownReward(RewardInterface):

    def __init__(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0
        terminal = False
        pitch = props["pitch-deg"]
        airspeed = props["airspeed-kt"]

        print("Height: {0}, Pitch: {1}, Speed: {2}".format(dist_vector.alt_diff_m, pitch, airspeed))

        if dist_vector.alt_diff_m < 0.1:
            reward_to_return = (25 * RewardMultipliers.TOUCHDOWN_MULTIPLIER)

        return reward_to_return, terminal

    def reset(self):
        pass

    def get_state(self) -> int:
        return RewardState.OVER_GROUND
