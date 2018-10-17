import unittest
import numpy as np
from ch.hslu.wipro.fg.calc.calc_distance import DistCalc

class FlightGearEnvTest(unittest.TestCase):

    def test_reward_fuction(self):
        dictionary = {
            "latitude-deg" : 21.3,
            "longitude-deg" : -157.9,
            "heading-deg" : 1,
            "altitude-ft" : 1000
        }

        vector = DistCalc.process_distance_vector(dictionary)

        vector.dist_m




if __name__ == '__main__':
     unittest.main()
