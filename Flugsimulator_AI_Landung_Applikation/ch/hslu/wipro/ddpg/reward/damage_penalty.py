from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.ddpg.reward.util import Util


class DamagePenalty(RewardInterface):

    def __init__(self):
        self.boolean_damage_keys = ['collapsed-wings']
        self.float_damage_keys = ['left-wing-damage', 'right-wing-damage']

    def calculate_reward(self, props) -> (float, bool):

        for possible_damage_key in self.boolean_damage_keys:
            if props[possible_damage_key] == 'true':
                return RewardMultipliers.NEGATIVE_REWARD, True

        for possible_damage_key in self.float_damage_keys:
            if props[possible_damage_key] > 0:
                return RewardMultipliers.NEGATIVE_REWARD, True

        has_gear_damage = Util.has_gear_damage(props)

        if has_gear_damage:
            return RewardMultipliers.NEGATIVE_REWARD, True

        return 0, False

    def reset(self):
        pass

    def get_state(self) -> int:
        return RewardState.COMMON
