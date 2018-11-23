from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.ddpg.reward.util import Util


class LandingReward(RewardInterface):
    def calculate_reward(self, props) -> (float, bool):
        divider = 1
        has_gear_damage = Util.has_gear_damage(props)
        if has_gear_damage:
            divider = 25

        if props['airspeed-kt'] < 1:
            print("Landed!")
            return (10 * RewardMultipliers.LANDING_MULTIPLIER) / divider, True

        return 0, False

    def reset(self):
        pass

    def get_state(self) -> int:
        return RewardState.ON_GROUND
