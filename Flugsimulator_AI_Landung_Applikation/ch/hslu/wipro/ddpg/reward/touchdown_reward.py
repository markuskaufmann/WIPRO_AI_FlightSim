from ch.hslu.wipro.ddpg.reward import RewardMultipliers
from ch.hslu.wipro.ddpg.reward.reward_interface import RewardInterface
from ch.hslu.wipro.ddpg.reward.reward_state import RewardState
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class TouchdownReward(RewardInterface):

    def __init__(self):
        self.counter = 0
        self.brake_count = 0
        self.brake_interval = 0

    def calculate_reward(self, props) -> (float, bool):
        dist_vector = DistCalc.process_distance_vector(props)
        reward_to_return = 0
        terminal = False
        pitch = props["pitch-deg"]
        airspeed = props["airspeed-kt"]

        print("Height: {0}, Pitch: {1}, Speed: {2}".format(dist_vector.alt_diff_m, pitch, airspeed))

        if dist_vector.alt_diff_m < 0.1:
            self.counter += 1
            if 2 < self.counter < 6:
                reward_to_return = RewardMultipliers.TOUCHDOWN_MULTIPLIER
            elif self.counter > 6:
                if self.brake_count < 10:
                    if self.brake_interval == 0:
                        print("-------------------- TOUCHDOWN: BRAKE --------------------")
                        FGPropertyWriter.write_brake(force=0.2 * (self.brake_count + 1))
                        self.brake_count += 1
                        self.brake_interval = 2
                    else:
                        self.brake_interval -= 1
        else:
            self.counter = 0

        return reward_to_return, terminal

    def reset(self):
        self.counter = 0
        self.brake_count = 0
        self.brake_interval = 0

    def get_state(self) -> int:
        return RewardState.ON_GROUND
