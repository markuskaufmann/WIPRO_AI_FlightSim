# from gym import spaces
# from gym.utils import seeding
from abc import ABC
from time import sleep

import numpy as np
from ch.hslu.wipro.ddpg.Environment import GoalEnv
from ch.hslu.wipro.ddpg.FlightGearUtility import FlightGearUtility
from ch.hslu.wipro.ddpg.spaces import dict_space
from ch.hslu.wipro.ddpg.spaces.Box import Box
from ch.hslu.wipro.ddpg.utility import Seeding
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc
from ch.hslu.wipro.fg.properties.fg_property_reader import FGPropertyReader
from ch.hslu.wipro.fg.properties.fg_property_writer import FGPropertyWriter

from ch.hslu.wipro.fg.fakeproperties.fake_fg_property_reader import FakeFGPropertyReader
from ch.hslu.wipro.fg.fakeproperties.fake_fg_property_writer import FakeFGPropertyWriter


class FlightGearEnv(GoalEnv, ABC):

    def __init__(self):
        self.viewer = None
        self.utility = FlightGearUtility()
        self.initialize_action_space()
        self.initialize_observation_space()

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

        reward = self.compute_reward(dist_vector, None)
        print("Step done")
        return observation, reward, False, {}


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

        # TODO: fix observation
        observation = np.array([props['aileron'], props['rudder'], props['elevator']])

        return dist_vector, observation

    def render(self, mode='human'):
        raise NotImplementedError

    def close(self):
        self.utility.close_flight_gear()

    def initialize_action_space(self):
        self.action_space = dict_space.Dict({
            'throttle': Box(low=-1, high=1, shape=(1,), dtype=np.float32),
            'mixture': Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        })

    #   self.action_space = Box(low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32)

    def initialize_observation_space(self):
        self.observation_space = dict_space.Dict({
            'observation': Box(low=-1, high=1, shape=(1,), dtype=np.float32),
            'desired_goal': Box(low=-1, high=1, shape=(1,), dtype=np.float32),
            'achieved_goal': Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        })

        """
        Example usage [nested]:
    self.nested_observation_space = spaces.Dict({
        'sensors':  spaces.Dict({
            'position': spaces.Box(low=-100, high=100, shape=(3,)),
            'velocity': spaces.Box(low=-1, high=1, shape=(3,)),
            'front_cam': spaces.Tuple((
                spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                spaces.Box(low=0, high=1, shape=(10, 10, 3))
            )),
            'rear_cam': spaces.Box(low=0, high=1, shape=(10, 10, 3)),
        }),
        'ext_controller': spaces.MultiDiscrete([ [0,4], [0,1], [0,1] ]),
        'inner_state':spaces.Dict({
            'charge': spaces.Discrete(100),
            'system_checks': spaces.MultiBinary(10),
            'job_status': spaces.Dict({
                'task': spaces.Discrete(5),
                'progress': spaces.Box(low=0, high=100, shape=()),
            })
        })
    })

        """

    # For the first stage no desired goal has to be set yet
    def compute_reward(self, achieved_goal, desired_goal, info=None):
        return -achieved_goal.dist_m
