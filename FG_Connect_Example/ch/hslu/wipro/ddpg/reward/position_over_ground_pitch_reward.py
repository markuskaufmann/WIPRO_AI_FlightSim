import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionOverGroundPitchReward(RewardInterface):
    def __init__(self):
        self.old_pitch_deg = None

    def reset(self):
        self.old_pitch_deg = None

    def calculate_reward(self, props) -> (float, bool):
        # add vector to observation space
        reward_to_return = 0
        pitch_deg = props['pitch-deg']

        if self.old_pitch_deg is None:
            self._set_old_values(pitch_deg)
            return reward_to_return, False

        reward_to_return += self.calculate_pitch_reward(pitch_deg)
        self._set_old_values(pitch_deg)

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.OVER_GROUND

    def _set_old_values(self, pitch_deg):
        self.old_pitch_deg = pitch_deg

    def calculate_pitch_reward(self, pitch_deg):
        reward_to_return = 0
        delta_pitch_deg = np.abs(pitch_deg) - np.abs(self.old_pitch_deg)

        if -2 < delta_pitch_deg < 1:
            rounded_pitch = np.round(np.abs(delta_pitch_deg), 1)
            reward_to_return += 1000 / (rounded_pitch if rounded_pitch != 0 else 0.01)

        if -2 < pitch_deg < 3:
            reward_to_return += 2000

        return reward_to_return

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
