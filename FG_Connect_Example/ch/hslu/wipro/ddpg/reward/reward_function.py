class RewardFunction(object):
    def __init__(self, reward_functions):
        self.old_dist_vector = None
        self.old_throttle = None
        self.terminal = False
        self.reward_functions = reward_functions

    def compute_reward(self, props):

        reward = 0

        for r_function in self.reward_functions:
            if self.terminal:
                return reward, self.terminal

            r, t = r_function.calculate_reward(props)
            reward += r
            self.terminal = t

        #if achieved_goal.dist_m < 20 and achieved_goal.alt_m < 1.4:
        #    print("******************** GOAL REACHED ********************")
        #    return 3000, True

        # TODO: change constant zero to action map

        return reward, self.terminal

    def set_old_values(self, achieved_goal, observation):
        pass

    def reset(self):
        self.terminal = False
        for r_function in self.reward_functions:
            r_function.reset()
