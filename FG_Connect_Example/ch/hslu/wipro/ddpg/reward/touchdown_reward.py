from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc


class TouchdownReward(RewardInterface):
    def __init__(self):
        self.plane_touched_ground = False
        self.give_touchdown_rewards = False
        self.gear_keys = ['left-gear-damage', 'right-gear-damage', 'front-gear-damage']
        self.touchdown_counter = 0

    def calculate_reward(self, props) -> (float, bool):
        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0
        terminal = False
        has_damage = self.has_damage(props)
        pitch = props["pitch-deg"]
        airspeed = props["airspeed-kt"]

        print("Height: {0}, Pitch: {1}".format(dist_vector.alt_diff_m, pitch))
        if dist_vector.alt_diff_m < 10:
            if 15 > pitch > 0:
                reward_to_return += pitch * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER
            elif pitch <= 0:
                reward_to_return += pitch * RewardMultipliers.PITCH_BEFORE_LANDING_MULTIPLIER

            reward_to_return += -(airspeed - 50) * RewardMultipliers.SPEED_BEFORE_LANDING_MULTIPLIER

        if dist_vector.alt_diff_m < 0.2 and not self.plane_touched_ground:
            self.plane_touched_ground = True
            self.give_touchdown_rewards = True

        if self.give_touchdown_rewards and dist_vector.alt_diff_m < 0.2:
            if self.touchdown_counter < 4:
                self.touchdown_counter += 1
            else:
                self.give_touchdown_rewards = False

            if has_damage:
                reward_to_return = (3 * RewardMultipliers.TOUCHDOWN_MULTIPLIER)
                terminal = True
            else:
                reward_to_return = (50 * RewardMultipliers.TOUCHDOWN_MULTIPLIER)
                print("*******CLEAN TOUCHDOWN**********")



        return reward_to_return, terminal

    def reset(self):
        self.plane_touched_ground = False
        self.give_touchdown_rewards = False
        self.touchdown_counter = 0

    def has_damage(self, props) -> bool:
        for damage_key in self.gear_keys:
            if props[damage_key] == 'true':
                return True

        return False
