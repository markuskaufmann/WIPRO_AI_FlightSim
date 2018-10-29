# from gym import spaces
# from gym.utils import seeding
from abc import ABC
from time import sleep

import numpy as np

from ch.hslu.wipro.ddpg.Environment import Env
from ch.hslu.wipro.ddpg.reward import reward_function_generator
from ch.hslu.wipro.ddpg.spaces import dict_space
from ch.hslu.wipro.ddpg.utility import Seeding
from ch.hslu.wipro.ddpg.utility import SpaceDefiner
from ch.hslu.wipro.ddpg.utility.factories.SpaceFactory import SpaceFactory
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FlightGearEnv(Env, ABC):

    def __init__(self):
        self.viewer = None
        self.initialize_action_space()
        self.initialize_observation_space()
        self.old_dist_vector = None
        self.old_throttle = None
        self.space_factory = SpaceFactory()
        self.props = None
        self.reward_function = reward_function_generator.generate_checkpoint2_reward_function()

        # Why?
        self.seed()

    def seed(self, seed=None):
        # Probably ok like this
        self.np_random, seed = Seeding.np_random(seed)
        return [seed]

    def step(self, u):
        FGPropertyWriter.write_action(u)
        sleep(0.5)
        observation = self._get_obs()
        reward, terminal = self.compute_reward()
        print("Step done")
        return observation, reward, terminal, {}

    def reset(self):
        # TODO: Put plane in the specific position with the defined speed etc, RETURN OBSERVATION
        FGPropertyWriter.reset_checkpoint2()
        self.old_dist_vector = None
        self.old_throttle = None
        sleep(1)
        observation = self._get_obs(reset=True)
        return observation

    def _get_obs(self, reset=False):
        self.props = None
        reset_first = True
        while self.props is None or self.props['reset_cp1'] == 1 or self.props['reset_cp2'] == 1:
            # react to FG bug that resets personal properties on reposition
            if reset and reset_first:
                sleep(0.5)
                reset_first = False
            self.props = FGPropertyReader.get_properties()
        self.props = FGPropertyReader.get_properties()
        dist_vector = DistCalc.process_distance_vector(self.props)
        observation = []
        # TODO: fix observation
        for key in SpaceDefiner.DefaultObservationSpaceKeys:
            if key == 'alt_m':
                observation.append(dist_vector.alt_m)
            elif key == 'dist_m':
                observation.append(dist_vector.dist_m)
            elif key == 'bearing_deg':
                observation.append(dist_vector.bearing_diff_deg)
            elif key == 'discrepancy':
                observation.append(dist_vector.bound_discrepancy)
            else:
                observation.append(self.props[key])

        observation = np.array(observation)
        return observation

    def render(self, mode='human'):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def initialize_action_space(self):
        self.action_space = dict_space.Dict(SpaceFactory().create_space(SpaceDefiner.DefaultActionSpaces))

    #   self.action_space = Box(low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32)

    def initialize_observation_space(self):
        self.observation_space = dict_space.Dict(SpaceFactory().create_space(SpaceDefiner.DefaultObservationSpaces))

    # For the first stage no desired goal has to be set yet
    def compute_reward(self):
        return self.reward_function.compute_reward(self.props)
