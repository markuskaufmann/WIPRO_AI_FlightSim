from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class TouchdownReward(RewardInterface):
    def __init__(self):
        self.plane_touched_ground = False
        self.back_gear_keys = ['left-gear-damage', 'right-gear-damage']
        self.front_gear_key = 'front-gear-damage'

    def calculate_reward(self, props) -> (float, bool):
        if self.plane_touched_ground:
            return 0, False

        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0

        has_back_gear_damage = self.has_back_gear_damage(props)

        if -50 < dist_vector.dist_m < 50 and dist_vector.alt_diff_m < 1:
            self.plane_touched_ground = True

            if has_back_gear_damage:
                reward_to_return = -10 * RewardMultipliers.TOUCHDOWN_MULTIPLIER
            elif props[self.front_gear_key] == 'false':
                reward_to_return = 20 * RewardMultipliers.TOUCHDOWN_MULTIPLIER
            else:
                reward_to_return = 200 * RewardMultipliers.TOUCHDOWN_MULTIPLIER

        elif dist_vector.alt_diff_m < 1:
            self.plane_touched_ground = True
            reward_to_return = 10 * RewardMultipliers.TOUCHDOWN_MULTIPLIER

        return reward_to_return, False

    def reset(self):
        self.plane_touched_ground = False

    def has_back_gear_damage(self, props) -> bool:
        for damage_key in self.back_gear_keys:
            if props[damage_key] == 'true':
                return True

        return False
