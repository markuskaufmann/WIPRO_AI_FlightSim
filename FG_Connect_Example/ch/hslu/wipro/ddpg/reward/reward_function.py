from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class RewardFunction(object):
    def __init__(self, reward_functions):
        self.old_dist_vector = None
        self.old_throttle = None
        self.terminal = False
        self.reward_functions = reward_functions
        self.reward_state = RewardState.IN_AIR

    def compute_reward(self, props, dist_vector):
        reward = 0
        self.check_reward_state(props, dist_vector)
        for r_function in self.reward_functions:
            if self.terminal:
                break
            if r_function.get_state() == self.reward_state or r_function.get_state() == RewardState.COMMON:
                r, t = r_function.calculate_reward(props)
                reward += r
                self.terminal = t

        return reward, self.terminal

    def set_old_values(self, achieved_goal, observation):
        pass

    def reset(self):
        self.terminal = False
        self.reward_state = RewardState.IN_AIR
        for r_function in self.reward_functions:
            r_function.reset()

    def check_reward_state(self, props, dist_vector):
        alt_m = dist_vector.alt_diff_m
        if alt_m < 0.2:
            if self.reward_state == RewardState.OVER_GROUND:
                print("\n%%%%%%%%%%%%%%%%% Switched to OnGround %%%%%%%%%%%%%%%%\n")
                self.reward_state = RewardState.ON_GROUND
        elif alt_m < 15:
            if self.reward_state == RewardState.IN_AIR:
                print("\n%%%%%%%%%%%%%%%%% Switched to OverGround %%%%%%%%%%%%%%%%\n")
                self.reward_state = RewardState.OVER_GROUND
