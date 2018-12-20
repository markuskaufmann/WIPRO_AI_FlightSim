from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState


class PositionOnGroundPitchReward(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        # add vector to observation space
        # reward_to_return = 0
        # pitch_deg = props['pitch-deg']

        elevator = 1 + props['elevator']

        # Evaluate elevator to change the pitch, not the pitch itself
        reward_to_return = RewardMultipliers.ON_GROUND_ELEVATOR_REWARD * elevator

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.ON_GROUND
