# from gym import spaces
# from gym.utils import seeding
from abc import ABC
from time import sleep

import numpy as np

from ch.hslu.wipro.ddpg.Environment import Env
from ch.hslu.wipro.ddpg.reward import reward_function_generator
from ch.hslu.wipro.ddpg.spaces import dict_space
from ch.hslu.wipro.ddpg.spaces.Box import Box
from ch.hslu.wipro.ddpg.utility import Seeding
from ch.hslu.wipro.ddpg.utility import SpaceDefiner
from ch.hslu.wipro.ddpg.utility.factories.SpaceFactory import SpaceFactory
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.properties.fg_property_normalizer import FGPropertyNormalizer
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter


class FlightGearEnv(Env, ABC):

    def __init__(self):
        self.viewer = None
        self.initialize_action_space()
        self.initialize_observation_space()
        self.space_factory = SpaceFactory()
        self.props = None
        self.old_props = None
        self.dist_vector = None
        self.old_dist_vector = None
        self.reward_function = reward_function_generator.generate_checkpoint2_reward_function()

        # Why?
        self.seed()

    def seed(self, seed=None):
        # Probably ok like this
        self.np_random, seed = Seeding.np_random(seed)
        return [seed]

    def step(self, u):
        FGPropertyWriter.write_action(u[0])
        sleep(0.3)
        observation = self._get_obs()
        reward, terminal = self.compute_reward()
        return observation, reward, terminal, {}

    def reset(self):
        # TODO: Put plane in the specific position with the defined speed etc, RETURN OBSERVATION
        FGPropertyWriter.reset_checkpoint2()
        self.reward_function.reset()
        sleep(1)
        observation = self._get_obs(reset=True)
        return observation

    def _get_obs(self, reset=False):
        self.set_old_values()
        self.reset_values()
        reset_wait_after_init = True
        while self.props is None or self.props['reset_cp1'] == 1 or self.props['reset_cp2'] == 1:
            # react to FG bug that resets personal properties on reposition
            if reset and reset_wait_after_init:
                sleep(0.5)
                reset_wait_after_init = False
            self.props = FGPropertyReader.get_properties()
        self.props = FGPropertyReader.get_properties()
        self.dist_vector = DistCalc.process_distance_vector(self.props)
        delta_values = self.get_delta_values()
        # normalization
        norm_props, norm_dist_vector, norm_delta_values = FGPropertyNormalizer.perform_normalization(
            self.props,
            self.dist_vector,
            delta_values)
        observation = []
        # TODO: fix observation
        for key in SpaceDefiner.DefaultObservationSpaceKeys:
            if key == 'alt_m':
                observation.append(norm_dist_vector.alt_diff_m)
            elif key == 'alt_m_delta':
                observation.append(norm_delta_values[key])
            elif key == 'airspeed-kt_delta':
                observation.append(norm_delta_values[key])
            elif key == 'dist_m':
                observation.append(norm_dist_vector.dist_m)
            elif key == 'bearing_deg':
                observation.append(norm_dist_vector.bearing_diff_deg)
            elif key == 'pitch_deg_delta':
                observation.append(norm_delta_values[key])
            elif key == 'roll_deg_delta':
                observation.append(norm_delta_values[key])
            elif key == 'heading_deg_delta':
                observation.append(norm_delta_values[key])
            else:
                observation.append(norm_props[key])
        observation = np.array(observation)
        return observation

    def set_old_values(self):
        self.old_props = self.props
        self.old_dist_vector = self.dist_vector

    def reset_values(self):
        self.props = None
        self.dist_vector = None

    def get_delta_values(self) -> dict:
        delta_values = dict()
        delta_values['alt_m_delta'] = 0
        delta_values['airspeed-kt_delta'] = 0
        delta_values['pitch_deg_delta'] = 0
        delta_values['roll_deg_delta'] = 0
        delta_values['heading_deg_delta'] = 0
        if self.old_dist_vector is None or self.old_props is None:
            return delta_values
        delta_values['alt_m_delta'] = self.dist_vector.alt_diff_m - self.old_dist_vector.alt_diff_m
        delta_values['airspeed-kt_delta'] = self.props['airspeed-kt'] - self.old_props['airspeed-kt']
        delta_values['pitch_deg_delta'] = self.props['pitch-deg'] - self.old_props['pitch-deg']
        delta_values['roll_deg_delta'] = self.props['roll-deg'] - self.old_props['roll-deg']
        delta_values['heading_deg_delta'] = self.props['heading-deg'] - self.old_props['heading-deg']
        return delta_values

    def render(self, mode='human'):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def initialize_action_space(self):
        self.action_space = Box(np.array([-1, -1, -1]), np.array([+1, +1, +1]))

    #   self.action_space = Box(low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32)

    def initialize_observation_space(self):

        self.observation_space = SpaceFactory().create_box_space(SpaceDefiner.DefaultObservationSpaces2)

    # For the first stage no desired goal has to be set yet
    def compute_reward(self):
        return self.reward_function.compute_reward(self.props)
