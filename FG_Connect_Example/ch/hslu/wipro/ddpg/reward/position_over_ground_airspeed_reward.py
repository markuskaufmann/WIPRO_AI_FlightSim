from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionOverGroundAirspeedReward(RewardInterface):
    def __init__(self):
        self.old_airspeed_kt = None

    def reset(self):
        self.old_airspeed_kt = None

    def calculate_reward(self, props) -> (float, bool):
        reward_to_return = 0
        airspeed_kt = props['airspeed-kt']
        dist_vector = DistCalc.process_distance_vector(props)
        if self.old_airspeed_kt is None:
            self._set_old_values(airspeed_kt)
            return reward_to_return, False

        reward_to_return += self.calculate_speed_reward(airspeed_kt, dist_vector)
        self._set_old_values(airspeed_kt)

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.OVER_GROUND

    def _set_old_values(self, airspeed_kt):
        self.old_airspeed_kt = airspeed_kt

    def calculate_speed_reward(self, airspeed_kt, distvector):
        delta_airspeed_kt = airspeed_kt - self.old_airspeed_kt

        if distvector.alt_diff_m > 6:
            if delta_airspeed_kt < -0.8:
                print("////////////////////// SLOWING DOWN TOO FAST")
                return RewardMultipliers.TO_FAST_OR_SLOW_SLOWDOWN_REWARD
            elif -0.8 <= delta_airspeed_kt <= 0.3:
                print("////////////////////// SLOWING DOWN JUST RIGHT")
                return RewardMultipliers.SLOWDOWN_JUST_RIGHT
            else:
                print("////////////////////// TOO FAST!")
                return RewardMultipliers.TO_FAST_OR_SLOW_SLOWDOWN_REWARD
        else:
            if delta_airspeed_kt < -2:
                print("////////////////////// SLOW DOWN FAST (AS IT SHOULD)")
                return RewardMultipliers.SLOWDOWN_JUST_RIGHT
            if delta_airspeed_kt > -1:
                print("////////////////////// NOT SLOWING DOWN FAST ENOUGH")
                return RewardMultipliers.TO_FAST_OR_SLOW_SLOWDOWN_REWARD

        return 0
