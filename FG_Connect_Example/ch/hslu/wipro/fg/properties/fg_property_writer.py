import inspect

from ch.hslu.wipro.fg.data.fg_data_output import FGDataOutput
from ch.hslu.wipro.fg.properties.fg_property_type import FGPropertyType


class FGPropertyWriter:
    VAR_SEPARATOR = ","
    LINE_SEPARATOR = "\r\n"

    @staticmethod
    def write_action(actions):
        throttle = (actions[0] + 1) / 2
        mixture = (actions[1] + 1) / 2
        FGPropertyWriter._write_engine(throttle, mixture)

    @staticmethod
    def _write_reset(aileron: float, aileron_trim: float, elevator: float, elevator_trim: float, rudder: float,
                     rudder_trim: float, flaps: float, throttle: float, mixture: float, brake_left: float,
                     brake_right: float, brake_parking: float, latitude_deg: float, longitude_deg: float,
                     altitude_ft: float, airspeed_kt: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_RESET, aileron, aileron_trim, elevator,
                                          elevator_trim, rudder, rudder_trim, flaps, throttle, mixture,
                                          brake_left, brake_right, brake_parking, latitude_deg, longitude_deg,
                                          altitude_ft, airspeed_kt)

    @staticmethod
    def reset_checkpoint2():
        FGPropertyWriter._write_reset(aileron=0, aileron_trim=0, elevator=0, elevator_trim=0, rudder=0,
                                      rudder_trim=0, flaps=0, throttle=0.5, mixture=0, brake_left=0, brake_right=0,
                                      brake_parking=0, latitude_deg=21.3252466948, longitude_deg=-158.1431852166,
                                      altitude_ft=1000, airspeed_kt=30)

    @staticmethod
    def _write_control(aileron: float, aileron_trim: float, elevator: float, elevator_trim: float, rudder: float,
                       rudder_trim: float, flaps: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_CONTROL, aileron, aileron_trim, elevator,
                                          elevator_trim, rudder, rudder_trim, flaps)

    @staticmethod
    def _write_engine(throttle: float, mixture: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_ENGINE, throttle, mixture)

    @staticmethod
    def _write_gear(brake_left: float, brake_right: float, brake_parking: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_GEAR, brake_left, brake_right, brake_parking)

    @staticmethod
    def _write_to_output(fg_property_type: FGPropertyType, aileron=None, aileron_trim=None, elevator=None,
                         elevator_trim=None, rudder=None, rudder_trim=None, flaps=None, throttle=None, mixture=None,
                         brake_left=None, brake_right=None, brake_parking=None, latitude_deg=None, longitude_deg=None,
                         altitude_ft=None, airspeed_kt=None):
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
