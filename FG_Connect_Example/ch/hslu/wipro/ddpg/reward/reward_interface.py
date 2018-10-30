class RewardInterface:
    def calculate_reward(self, props) -> (float, bool):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
