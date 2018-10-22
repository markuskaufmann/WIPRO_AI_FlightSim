import inspect

from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.properties.fg_property_converter import FGPropertyConverter
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FGPropertyWriter:
    VAR_SEPARATOR = ","
    LINE_SEPARATOR = "\r\n"

    @staticmethod
    def write_action(actions):
        actions_to_write = FGPropertyConverter.process_actions(actions)
        if len(actions_to_write) == 0:
            return
        FGPropertyWriter._write_control(aileron=actions_to_write['aileron'],
                                        elevator=actions_to_write['elevator'],
                                        rudder=actions_to_write['rudder'],
                                        flaps=actions_to_write['flaps'],
                                        throttle=actions_to_write['throttle'],
                                        mixture=actions_to_write['mixture'])

    @staticmethod
    def reset_checkpoint1():
        pass

    @staticmethod
    def reset_checkpoint2():
        FGPropertyWriter._write_reset(aileron=0, elevator=0, rudder=0, flaps=0, throttle=0.6, mixture=0.95,
                                      latitude_deg=21.3252466948, longitude_deg=-157.95,
                                      altitude_ft=100, airspeed_kt=20, damage='false', pitch_deg=0, roll_deg=0,
                                      heading_deg=90)

    @staticmethod
    def _write_reset(aileron: float, elevator: float, rudder: float, flaps: float, throttle: float, mixture: float,
                     latitude_deg: float, longitude_deg: float, altitude_ft: float, airspeed_kt: float, damage: str,
                     pitch_deg: float, roll_deg: float, heading_deg: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_RESET, aileron, elevator, rudder, flaps, throttle,
                                          mixture, latitude_deg, longitude_deg, altitude_ft, airspeed_kt, damage,
                                          pitch_deg, roll_deg, heading_deg)

    @staticmethod
    def _write_control(aileron: float, elevator: float, rudder: float, flaps: float, throttle: float,
                       mixture: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_CONTROL, aileron, elevator, rudder,
                                          flaps, throttle, mixture)

    # @staticmethod
    # def _write_engine(throttle: float, mixture: float):
    #     FGPropertyWriter._write_to_output(FGPropertyType.WRITE_ENGINE, throttle, mixture)
    #
    # @staticmethod
    # def _write_gear(brake_left: float, brake_right: float, brake_parking: float):
    #     FGPropertyWriter._write_to_output(FGPropertyType.WRITE_GEAR, brake_left, brake_right, brake_parking)

    @staticmethod
    def _write_to_output(fg_property_type: FGPropertyType, aileron=None, elevator=None, rudder=None, flaps=None,
                         throttle=None, mixture=None, latitude_deg=None, longitude_deg=None, altitude_ft=None,
                         airspeed_kt=None, damage=None, pitch_deg=None, roll_deg=None, heading_deg=None):
        prop_type_keys = FGPropertyType.TYPE_PROP_MAP[fg_property_type]
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        values.pop('frame')
        values.pop('fg_property_type')
        output = ""
        for prop_key in prop_type_keys:
            val = values[prop_key]
            s = FGPropertyWriter.VAR_SEPARATOR
            if val is not None:
                s = str(val) + s
            output += s
        FGDataOutput.set((fg_property_type, output[:-1] + FGPropertyWriter.LINE_SEPARATOR))
