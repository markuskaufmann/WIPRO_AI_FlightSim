
class FGPropertyWriteType:
    WRITE_RESET = -1
    WRITE_CONTROL = 0
    WRITE_ENGINE = 1
    WRITE_GEAR = 2

    TYPE_PROP_MAP = {
        WRITE_RESET: ['aileron', 'aileron_trim', 'elevator', 'elevator_trim', 'rudder', 'rudder_trim', 'flaps',
                      'slats', 'speedbrake', 'throttle', 'mixture', 'brake_left', 'brake_right', 'brake_parking',
                      'latitude_deg', 'longitude_deg', 'altitude_ft', 'airspeed_kt'],
        WRITE_CONTROL: ['aileron', 'aileron_trim', 'elevator', 'elevator_trim', 'rudder', 'rudder_trim', 'flaps',
                        'slats', 'speedbrake'],
        WRITE_ENGINE: ['throttle', 'mixture'],
        WRITE_GEAR: ['brake_left', 'brake_right', 'brake_parking']
    }

    TYPE_PORT_MAP = {
        WRITE_RESET: 9877,
        WRITE_CONTROL: 9878,
        WRITE_ENGINE: 9879,
        WRITE_GEAR: 9880
    }
