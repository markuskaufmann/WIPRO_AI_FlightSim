import unittest

from ch.hslu.wipro.ddpg.spaces.Box import Box
from ch.hslu.wipro.ddpg.utility.factories.SpaceFactory import SpaceFactory
import numpy as np

class SpaceFactoryTest(unittest.TestCase):

    testee = SpaceFactory()
    box = Box(low=-5, high=1, shape=(1,), dtype=np.float32)

    def test_returns_box(self):
        result = self.testee.create_space([(True, 'test', self.box)])
        self.assertEqual(list(result.keys())[0], 'test')

    def test_add_multiple(self):
        result = self.testee.create_space([(True, 'test', self.box), (True, 'test2', self.box)])
        self.assertIs(len(result), 2)

    def test_doesnt_add_when_flag_is_false(self):
        result = self.testee.create_space([(True, 'test', self.box), (True, 'test2', self.box), (False, 'test3', self.box)])
        self.assertIs(len(result), 2)

    def test_add_box_form(self):
        result = self.testee.create_space([(True, 'test', self.box)])
        self.assertEqual(result['test'], self.box)

    def test_complete(self):
        result = self.testee.create_space(
            [(True, 'test', self.box), (True, 'test2', self.box), (False, 'test3', self.box)])
        self.assertEqual(str(result), "{'test': Box(1,), 'test2': Box(1,)}")

if __name__ == '__main__':
    unittest.main()