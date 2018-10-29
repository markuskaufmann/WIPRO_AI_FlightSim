class RewardInterface:
    def calculate_reward(self, observation) -> (float, bool):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
