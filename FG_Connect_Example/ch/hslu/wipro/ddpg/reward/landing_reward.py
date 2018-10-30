from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.const.dist_lookup import DistLookup


class LandingReward(RewardInterface):
    def calculate_reward(self, props) -> (float, bool):
        if props['airspeed-kt'] < 2:
            if self.check_if_plane_is_on_runway(props):
                return 5000, True

        return 0, False

    def reset(self):
        pass

    def check_if_plane_is_on_runway(self, props) -> bool:
        lat_deg = props['latitude-deg']
        lon_deg = props['longitude-deg']
        if lat_deg < DistLookup.RWY_WIDTH_BOUNDARY['left'] or lat_deg > DistLookup.RWY_WIDTH_BOUNDARY['right']:
            return False
        elif lon_deg < DistLookup.RWY_LOC_TD_ZONE_START['lon'] or lon_deg > DistLookup.RWY_LOC_TD_ZONE_END['lon']:
            return False
        return True
