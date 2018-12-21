import numpy as np

from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class PositionInAirPitchReward(RewardInterface):
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
        return RewardState.IN_AIR

    def _set_old_values(self, pitch_deg):
        self.old_pitch_deg = pitch_deg

    def calculate_pitch_reward(self, pitch_deg):
        reward_to_return = 0
        delta_pitch_deg = np.abs(pitch_deg) - np.abs(self.old_pitch_deg)

        if delta_pitch_deg >= 2:
            reward_to_return -= 200

        if -5 < pitch_deg < -1:
            reward_to_return += 100

        return reward_to_return
