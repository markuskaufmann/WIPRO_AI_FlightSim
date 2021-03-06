
class FGPropertyType:
    READ = 'FG Property Read'
    WRITE_RESET = 'FG Property Reset'
    WRITE_CONTROL = 'FG Property Write Control'
    WRITE_GEAR = 'FG Property Write Gear'

    TYPE_PROP_MAP = {
        WRITE_RESET: ['checkpoint_1', 'checkpoint_2', 'fg_exit'],
        WRITE_CONTROL: ['aileron', 'elevator', 'throttle'],
        WRITE_GEAR: ['brake_left', 'brake_right']
    }

    TYPE_CONNECTION_MAP = {
        READ: [9876],
        WRITE_RESET: [9877],
        WRITE_CONTROL: [9878],
        WRITE_GEAR: [9879]
    }

    @staticmethod
    def add_socket_to_connection_map(fg_property_type, socket):
        values = FGPropertyType.TYPE_CONNECTION_MAP[fg_property_type]
        values.append(socket)

    @staticmethod
    def remove_socket_from_connection_map(fg_property_type, socket):
        values = FGPropertyType.TYPE_CONNECTION_MAP[fg_property_type]
        values.remove(socket)
