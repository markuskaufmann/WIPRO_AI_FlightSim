# from gym import spaces
# from gym.utils import seeding
from abc import ABC

from ch.hslu.wipro.ddpg.Environment import GoalEnv
from ch.hslu.wipro.ddpg.FlightGearUtility import FlightGearUtility
from ch.hslu.wipro.ddpg.utility import Seeding


class FlightGearEnv(GoalEnv, ABC):
    # Metadata necessary?
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 30
    }

    def __init__(self):
        self.viewer = None
        self.utility = FlightGearUtility()
        self.initialize_action_space()
        self.initialize_observation_space()

        # Why?
        self.seed()

    def seed(self, seed=None):
        # Probably ok like this
        self.np_random, seed = Seeding.seeding.np_random(seed)
        return [seed]

    def step(self, u):
        # TODO: Make Action
        # TODO: Evaluate Cost
        # TODO: Get Observation
        # TODO: Return observation, cost, if the episode is done and maybe an info

        """
        th, thdot = self.state  # th := theta
        

        g = 10.
        m = 1.
        l = 1.
        dt = self.dt

        u = np.clip(u, -self.max_torque, self.max_torque)[0]
        self.last_u = u # for rendering
        costs = angle_normalize(th)**2 + .1*thdot**2 + .001*(u**2)

        newthdot = thdot + (-3*g/(2*l) * np.sin(th + np.pi) + 3./(m*l**2)*u) * dt
        newth = th + newthdot*dt
        newthdot = np.clip(newthdot, -self.max_speed, self.max_speed) #pylint: disable=E1111

        self.state = np.array([newth, newthdot])
        return self._get_obs(), -costs, False, {}
        """
        raise NotImplementedError

    def reset(self):
        # TODO: Put plane in the specific position with the defined speed etc, RETURN OBSERVATION
        return self.utility.reset_plane()

    def _get_obs(self):
        # TODO: Return current state of the plane... shoudn't be that difficult
        return None

    def render(self, mode='human'):
        # TODO: Check how to start. Rename Render. Change Environment signature (abstract class)
        self.utility.start_flight_gear()
        return None

    def close(self):
        self.utility.close_flight_gear()

    def initialize_action_space(self):
        # TODO: Initialize Action Space
        pass

    #   self.action_space = Box(low=-self.max_torque, high=self.max_torque, shape=(1,), dtype=np.float32)

    def initialize_observation_space(self):
        # TODO: Initialize Observation Space
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
        # self.observation_space = Box(low=-high, high=high, dtype=np.float32)
        pass

    def compute_reward(self, achieved_goal, desired_goal, info):
        # TODO: compute reward
        pass

