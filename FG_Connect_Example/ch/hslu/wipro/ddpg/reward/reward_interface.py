class RewardInterface:
    def calculate_reward(self, observation):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
