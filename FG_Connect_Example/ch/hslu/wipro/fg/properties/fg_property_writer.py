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
                                        throttle=actions_to_write['throttle'])

    @staticmethod
    def write_brake(force: float = 1):
        if force > 1:
            force = 1
        elif force < 0.1:
            force = 0.1
        FGPropertyWriter._write_brake(force)

    @staticmethod
    def reset_checkpoint1():
        FGPropertyWriter._write_reset(checkpoint_1=1, checkpoint_2=0)

    @staticmethod
    def reset_checkpoint2():
        FGPropertyWriter._write_reset(checkpoint_1=0, checkpoint_2=1)

    @staticmethod
    def fg_exit():
        FGPropertyWriter._write_reset(checkpoint_1=0, checkpoint_2=0, fg_exit=1)

    @staticmethod
    def _write_reset(checkpoint_1: float, checkpoint_2: float, fg_exit: float=0):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_RESET,
                                          checkpoint_1=checkpoint_1,
                                          checkpoint_2=checkpoint_2,
                                          fg_exit=fg_exit)

    @staticmethod
    def _write_control(aileron: float, elevator: float, throttle: float):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_CONTROL, aileron=aileron,
                                          elevator=elevator, throttle=throttle)

    @staticmethod
    def _write_brake(force: float = 1):
        FGPropertyWriter._write_to_output(FGPropertyType.WRITE_GEAR, brake_left=force, brake_right=force)

    @staticmethod
    def _write_to_output(fg_property_type: FGPropertyType, aileron=None, elevator=None,
                         throttle=None, brake_left=None, brake_right=None,
                         checkpoint_1=None, checkpoint_2=None, fg_exit=None):
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
