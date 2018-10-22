from ch.hslu.wipro.ddpg.spaces.Box import Box
import numpy as np

_normal_box = Box(low=-1, high=1, shape=(1,), dtype=np.float32)

DefaultActionSpaces = [
    (True, 'throttle', _normal_box),
    (True, 'mixture', _normal_box),
    (True, 'aileron', _normal_box),
    (True, 'elevator', _normal_box),
    (True, 'rudder', _normal_box),
    (True, 'flaps', _normal_box)
]

DefaultObservationSpaces = [
    (True, 'throttle', _normal_box),
    (True, 'mixture', _normal_box),
    (True, 'aileron', _normal_box),
    (True, 'elevator', _normal_box),
    (True, 'rudder', _normal_box),
    (True, 'flaps', _normal_box)
]

DefaultObservationSpaceKeys = ['throttle', 'mixture', 'aileron', 'elevator', 'rudder', 'flaps']

