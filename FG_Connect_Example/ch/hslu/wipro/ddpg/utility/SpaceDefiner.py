from ch.hslu.wipro.ddpg.spaces.Box import Box
import numpy as np

_normal_box = Box(low=-1, high=1, shape=(1,), dtype=np.float32)
_positive_box = Box(low=0, high=1, shape=(1,), dtype=np.float32)

DefaultActionSpaces = [
    (True, 'throttle', _normal_box),
    (True, 'aileron', _normal_box),
    (True, 'elevator', _normal_box)
]

DefaultObservationSpaces = [
    (True, 'throttle', _positive_box),
    (True, 'mixture', _positive_box),
    (True, 'aileron', _normal_box),
    (True, 'elevator', _normal_box),
    (True, 'rudder', _normal_box),
    (True, 'flaps', _positive_box),
    (True, 'airspeed-kt', _positive_box),
    (True, 'alt_m', _normal_box),
    (True, 'dist_m', _normal_box),
    (True, 'discrepancy', _positive_box),
    (True, 'bearing_deg', _normal_box)
]

DefaultObservationSpaceKeys = [observation_space[1] for observation_space in DefaultObservationSpaces]

