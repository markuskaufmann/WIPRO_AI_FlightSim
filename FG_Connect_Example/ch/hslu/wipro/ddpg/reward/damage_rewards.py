from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface


class DamageRewards(RewardInterface):

    def __init__(self):
        self.boolean_damage_keys = ['gear-front-broken', 'gear-left-broken', 'gear-right-broken', 'collapsed-wings']
        self.float_damage_keys = [ 'left-wing-damage', 'right-wing-damage']

    def calculate_reward(self, observation) -> (float, bool):
        for possible_damage_key in self.boolean_damage_keys:
            if observation[possible_damage_key] == 'true':
                return -1000, True

        for possible_damage_key in self.float_damage_keys:
            if observation[possible_damage_key] > 0:
                return -1000, True

        return 0, False

    def reset(self):
        pass
