from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class TouchdownReward(RewardInterface):
    def __init__(self):
        self.plane_touched_ground = False
        self.first_step_after_touchdown = False
        self.back_gear_keys = ['left-gear-damage', 'right-gear-damage', 'front-gear-damage']

    def calculate_reward(self, props) -> (float, bool):
        #if self.plane_touched_ground:
        #    return 0, False

        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0
        terminal = False
        has_damage = self.has_damage(props)
        pitch = props["pitch-deg"]

        print("Height: ", dist_vector.alt_diff_m, " --  Pitch: ", pitch)
        if dist_vector.alt_diff_m < 10:
            if 15 > pitch > 0:
                reward_to_return += pitch * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER
            elif pitch <= 0:
                reward_to_return += pitch * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER

        if dist_vector.alt_diff_m < 0.5 and not self.plane_touched_ground:
            self.plane_touched_ground = True
            self.first_step_after_touchdown = True

        if self.first_step_after_touchdown and dist_vector.alt_diff_m < 0.5:
            self.first_step_after_touchdown = False
            if has_damage:
                reward_to_return = (5 * RewardMultipliers.TOUCHDOWN_MULTIPLIER)
                terminal = True
            else:
                reward_to_return = (200 * RewardMultipliers.TOUCHDOWN_MULTIPLIER)
                print("*******CLEAN TOUCHDOWN**********")

        return reward_to_return, terminal

    def reset(self):
        self.plane_touched_ground = False
        self.first_step_after_touchdown = False

    def has_damage(self, props) -> bool:
        for damage_key in self.back_gear_keys:
            if props[damage_key] == 'true':
                return True

        return False
