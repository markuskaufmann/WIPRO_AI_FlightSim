
class FGPropertyType:
    READ = 'FG Property Read'
    WRITE_RESET = 'FG Property Reset'
    WRITE_CONTROL = 'FG Property Write'
    # WRITE_ENGINE = 1
    # WRITE_GEAR = 2

    TYPE_PROP_MAP = {
        # WRITE_RESET: ['aileron', 'elevator', 'rudder', 'flaps', 'throttle', 'mixture',
        #               'latitude_deg', 'longitude_deg', 'altitude_ft', 'airspeed_kt', 'damage',
        #               'pitch_deg', 'roll_deg', 'heading_deg'],
        WRITE_RESET: ['checkpoint_1', 'checkpoint_2'],
        WRITE_CONTROL: ['aileron', 'elevator', 'rudder', 'flaps', 'throttle', 'mixture']
        # WRITE_ENGINE: ['throttle', 'mixture'],
        # WRITE_GEAR: ['brake_left', 'brake_right', 'brake_parking']
    }

    TYPE_CONNECTION_MAP = {
        READ: [9876],
        WRITE_RESET: [9877],
        WRITE_CONTROL: [9878]
        # WRITE_ENGINE: [9879],
        # WRITE_GEAR: [9880]
    }

    @staticmethod
    def add_socket_to_connection_map(fg_property_type, socket):
        values = FGPropertyType.TYPE_CONNECTION_MAP[fg_property_type]
        values.append(socket)
