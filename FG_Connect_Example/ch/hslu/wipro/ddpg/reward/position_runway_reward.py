import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.RewardMultipliers import NOT_ON_CENTER_RUNWAY_MULTIPLIER
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.const.dist_lookup import DistLookup


class PositionRunwayReward(RewardInterface):
    def __init__(self):
        pass

    def reset(self):
        pass

    def calculate_reward(self, props) -> (float, bool):
        dist_vector = DistCalc.process_distance_vector(props)

        if not DistCalc.check_if_plane_is_on_runway_width(props):
            if not DistCalc.check_if_plane_is_on_runway_width(props):
                if dist_vector.alt_diff_m < 0.1:
                    return 0, True
                else:
                    return RewardMultipliers.NEGATIVE_REWARD, True

        current_lat_deg = props['latitude-deg']
        lat_runway_deg = DistLookup.RWY_LOC_TD_ZONE_START['lat']
        lat_diff_deg = -np.abs(lat_runway_deg - current_lat_deg) * 10000
        lat_diff_deg += 0.3
        print("------------!!!!!!!!!!!!!------------dist to center: {0} deg, reward: {1}".format(
            (lat_runway_deg - current_lat_deg), lat_diff_deg))
        return NOT_ON_CENTER_RUNWAY_MULTIPLIER * lat_diff_deg, False

    def get_state(self) -> int:
        return RewardState.COMMON
