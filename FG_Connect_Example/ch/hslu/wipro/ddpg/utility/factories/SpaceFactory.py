class SpaceFactory(object):
    def create_space(self, actionTupels):
        space = {}

        for tupels in actionTupels:
            if tupels[0]:
                space.update({tupels[1]: tupels[2]})

        return space
