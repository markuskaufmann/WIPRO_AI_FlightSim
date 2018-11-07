from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.const.dist_lookup import DistLookup


class LandingReward(RewardInterface):
    def calculate_reward(self, props) -> (float, bool):
        if props['airspeed-kt'] < 5:
            if DistCalc.check_if_plane_is_on_runway(props):
                return 10 * RewardMultipliers.LANDING_MULTIPLIER, True
        return 0, False

    def reset(self):
        pass
