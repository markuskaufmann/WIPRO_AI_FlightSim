from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState


class PositionPitchReward(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        reward_to_return = 0

        if props["pitch-deg"] < -40:
            return RewardMultipliers.NEGATIVE_REWARD, True

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.COMMON
