
class FGPropertyType:
    READ = -2
    WRITE_RESET = -1
    WRITE_CONTROL = 0
    WRITE_ENGINE = 1
    WRITE_GEAR = 2

    TYPE_PROP_MAP = {
        WRITE_RESET: ['aileron', 'aileron_trim', 'elevator', 'elevator_trim', 'rudder', 'rudder_trim', 'flaps',
                      'throttle', 'mixture', 'brake_left', 'brake_right', 'brake_parking',
                      'latitude_deg', 'longitude_deg', 'altitude_ft', 'airspeed_kt'],
        WRITE_CONTROL: ['aileron', 'aileron_trim', 'elevator', 'elevator_trim', 'rudder', 'rudder_trim', 'flaps'],
        WRITE_ENGINE: ['throttle', 'mixture'],
        WRITE_GEAR: ['brake_left', 'brake_right', 'brake_parking']
    }

    TYPE_CONNECTION_MAP = {
        READ: [9876],
        WRITE_RESET: [9877],
        WRITE_CONTROL: [9878],
        WRITE_ENGINE: [9879],
        WRITE_GEAR: [9880]
    }

    @staticmethod
    def add_socket_to_connection_map(fg_property_type, socket):
        values = FGPropertyType.TYPE_CONNECTION_MAP[fg_property_type]
        values.append(socket)
