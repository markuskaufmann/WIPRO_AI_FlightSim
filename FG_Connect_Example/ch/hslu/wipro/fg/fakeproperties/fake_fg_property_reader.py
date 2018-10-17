from ch.hslu.wipro.fg.data.fg_data_input import FGDataInput


class FakeFGPropertyReader:

    @staticmethod
    def get_properties():

        dict = {
            "aileron": 0.4,
            "rudder": 0.4,
            "elevator": 0.4,
            "latitude-deg": 21,
            "longitude-deg": -151,
            "heading-deg": 2,
            "altitude-ft": 700,
        }

        return dict
