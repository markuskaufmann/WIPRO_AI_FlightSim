from ch.hslu.wipro.ddpg.spaces.Box import Box
import numpy as np

class SpaceFactory(object):
    def create_space(self, actionTupels):
        space = {}
        for tupels in actionTupels:
            if tupels[0]:
                space.update({tupels[1]: tupels[2]})

        return space

    def create_box_space(self, actionTupels):
        space = {}
        array1 = []
        array2 = []
        for tupels in actionTupels:
            array1.append(tupels[0])
            array2.append(tupels[1])

        return Box(np.array(array1), np.array(array2))
