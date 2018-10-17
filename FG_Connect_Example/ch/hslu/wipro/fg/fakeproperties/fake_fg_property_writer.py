import inspect

from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FakeFGPropertyWriter:
    VAR_SEPARATOR = ","
    LINE_SEPARATOR = "\r\n"

    @staticmethod
    def write_action(action_dictionary):
        print(action_dictionary)

    @staticmethod
    def write_reset(aileron: float, aileron_trim: float, elevator: float, elevator_trim: float, rudder: float,
                    rudder_trim: float, flaps: float, throttle: float, mixture: float, brake_left: float,
                    brake_right: float, brake_parking: float, latitude_deg: float, longitude_deg: float,
                    altitude_ft: float, airspeed_kt: float):
        print("write reset")

    @staticmethod
    def write_control(aileron: float, aileron_trim: float, elevator: float, elevator_trim: float, rudder: float,
                      rudder_trim: float, flaps: float):
        print("write_control")

    @staticmethod
    def write_engine(throttle: float, mixture: float):
        print("write_engine")

    @staticmethod
    def write_gear(brake_left: float, brake_right: float, brake_parking: float):
        print("write_gear")

    @staticmethod
    def _write_to_output(fg_property_type: FGPropertyType, aileron=None, aileron_trim=None, elevator=None,
                         elevator_trim=None, rudder=None, rudder_trim=None, flaps=None, throttle=None, mixture=None,
                         brake_left=None, brake_right=None, brake_parking=None, latitude_deg=None, longitude_deg=None,
                         altitude_ft=None, airspeed_kt=None):
        print("write_control")
