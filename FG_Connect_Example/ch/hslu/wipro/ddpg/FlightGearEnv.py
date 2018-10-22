# from gym import spaces
# from gym.utils import seeding
from abc import ABC
from time import sleep

import numpy as np

from ch.hslu.wipro.ddpg.Environment import Env
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

        # Why?
        self.seed()

    def seed(self, seed=None):
        # Probably ok like this
        self.np_random, seed = Seeding.np_random(seed)
        return [seed]

    def step(self, u):
        FGPropertyWriter.write_action(u)
        sleep(0.7)
        dist_vector, observation = self._get_obs()

        reward, terminal = self.compute_reward(dist_vector, observation)
        print("Step done")
        return observation, reward, terminal, {}


    def reset(self):
        # TODO: Put plane in the specific position with the defined speed etc, RETURN OBSERVATION
        FGPropertyWriter.reset_checkpoint2()
        sleep(3)
        dist_vector, observation = self._get_obs()
        return observation

    def _get_obs(self):
        # TODO: remove fakes
        props = FGPropertyReader.get_properties()
        dist_vector = DistCalc.process_distance_vector(props)
        observation = []
        # TODO: fix observation
        for key in SpaceDefiner.DefaultObservationSpaceKeys:
            observation.append(props[key])

        observation = np.array(observation)
        return dist_vector, observation

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
    def compute_reward(self, achieved_goal, observation):
        if self.old_dist_vector is None or self.old_throttle is None:
            self.set_old_values(achieved_goal, observation)
            return 0, False

        if achieved_goal.dist_m < 20:
            print("******************** GOAL REACHED *****************")
            return 3000, True

        delta_distance = self.old_dist_vector - achieved_goal.dist_m
        # TODO: change constant zero to action map
        delta_throttle = self.old_throttle - observation[0]

        self.set_old_values(achieved_goal, observation)

        return delta_distance - delta_throttle*100, delta_distance == 0

    def set_old_values(self, achieved_goal, observation):
        self.old_dist_vector = achieved_goal.dist_m
        # TODO: change constant zero to action map
        self.old_throttle = observation[0]
