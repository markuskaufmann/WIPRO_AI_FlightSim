import inspect

from ch.hslu.wipro.fg.properties.fg_property_write_type import FGPropertyWriteType


class FGPropertyWriter:
    VAR_SEPARATOR = ","
    LINE_SEPARATOR = "\r\n"

    @staticmethod
    def prepare_output(property_write_type: FGPropertyWriteType, aileron=None, aileron_trim=None, elevator=None,
                       elevator_trim=None, rudder=None, rudder_trim=None, flaps=None, slats=None, speedbrake=None,
                       throttle=None, mixture=None, brake_left=None, brake_right=None, brake_parking=None,
                       latitude_deg=None, longitude_deg=None, altitude_ft=None, airspeed_kt=None):
        prop_type_keys = FGPropertyWriteType.TYPE_PROP_MAP[property_write_type]
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        values.pop('frame')
        values.pop('property_write_type')
        output = ""
        for prop_key in prop_type_keys:
            val = values[prop_key]
            s = FGPropertyWriter.VAR_SEPARATOR
            if val is not None:
                s = str(val) + s
            output += s
        return output[:-1] + FGPropertyWriter.LINE_SEPARATOR
