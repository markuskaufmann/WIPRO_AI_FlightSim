from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface


class DamageRewards(RewardInterface):

    def __init__(self):
        self.possible_damage_keys = ['gear-front-broken', 'gear-left-broken', 'gear-right-broken', 'left-wing-damage',
                                     'right-wing-damage', 'collapsed-wings']

    def calculate_reward(self, observation) -> (float, bool):
        for possible_damage_key in self.possible_damage_keys:
            if observation[possible_damage_key] == 'true':
                return -1000, True

        return 0, False

    def reset(self):
        pass
