from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState


class LandingReward(RewardInterface):
    def calculate_reward(self, props) -> (float, bool):

        if props['airspeed-kt'] < 3:
            print("Landed!")
            return RewardMultipliers.LANDING_MULTIPLIER, True

        return RewardMultipliers.ON_GROUND_REWARD, False

    def reset(self):
        pass

    def get_state(self) -> int:
        return RewardState.ON_GROUND
