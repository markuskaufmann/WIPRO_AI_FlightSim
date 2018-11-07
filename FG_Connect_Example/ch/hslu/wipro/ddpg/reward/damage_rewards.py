from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface


class DamageRewards(RewardInterface):

    def __init__(self):
        self.boolean_damage_keys = ['collapsed-wings']
        self.float_damage_keys = ['left-wing-damage', 'right-wing-damage']

    def calculate_reward(self, props) -> (float, bool):
        for possible_damage_key in self.boolean_damage_keys:
            if props[possible_damage_key] == 'true':
                return -5 * RewardMultipliers.DAMAGE_MULTIPLIER, True

        for possible_damage_key in self.float_damage_keys:
            if props[possible_damage_key] > 0:
                return -10 * RewardMultipliers.DAMAGE_MULTIPLIER, True

        return 0, False

    def reset(self):
        pass
