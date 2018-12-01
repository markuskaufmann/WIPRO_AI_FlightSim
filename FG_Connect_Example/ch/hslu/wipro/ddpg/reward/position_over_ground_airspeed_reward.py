import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState


class PositionOverGroundAirspeedReward(RewardInterface):
    def __init__(self):
        self.old_airspeed_kt = None

    def reset(self):
        self.old_airspeed_kt = None

    def calculate_reward(self, props) -> (float, bool):
        reward_to_return = 0
        airspeed_kt = props['airspeed-kt']

        if self.old_airspeed_kt is None:
            self._set_old_values(airspeed_kt)
            return reward_to_return, False

        reward_to_return += self.calculate_speed_reward(airspeed_kt)
        self._set_old_values(airspeed_kt)

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.OVER_GROUND

    def _set_old_values(self, airspeed_kt):
        self.old_airspeed_kt = airspeed_kt

    def calculate_speed_reward(self, airspeed_kt):
        delta_airspeed_kt = np.abs(airspeed_kt - self.old_airspeed_kt)

        if delta_airspeed_kt > 3:
            print("////////////////////// SLOWING DOWN TO FAST")
            return RewardMultipliers.TO_FAST_SLOWDOWN_REWARD

        return 0

    def old_calculate_pitch_reward(self, props, dist_vector):
        pitch = props['pitch-deg']
        reward_to_return = 0

        if dist_vector.alt_diff_m < 10:
            if -30 < pitch:
                reward_to_return = 0
            elif 15 > pitch > 0:
                reward_to_return += pitch * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER
            elif pitch <= 0:
                reward_to_return += ((30 + pitch) / 5) * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER

        return reward_to_return
