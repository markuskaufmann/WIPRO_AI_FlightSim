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
        dist_vector = DistCalc.process_distance_vector(props)

        if self.old_pitch_deg is None:
            self._set_old_values(pitch_deg)
            return reward_to_return, False

        if dist_vector.alt_diff_m < 6:
            reward_to_return += self.calc_almost_ground_pitch_reward(pitch_deg)

        self._set_old_values(pitch_deg)

        return reward_to_return, False

    def get_state(self) -> int:
        return RewardState.OVER_GROUND

    def _set_old_values(self, pitch_deg):
        self.old_pitch_deg = pitch_deg

    def calc_almost_ground_pitch_reward(self, pitch_deg):
        if pitch_deg > 0:
            return RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER * pitch_deg
        return 0
