
# constants checkpoint 1
var cp1_aileron = 0;
var cp1_elevator = 0.3;
var cp1_rudder = 0;
var cp1_flaps = 1;
var cp1_throttle = 0.3;
var cp1_mixture = 0.7;
var cp1_latitude_deg = 21.3252466948;
var cp1_longitude_deg = -157.946;
var cp1_altitude_ft = 66;
var cp1_airspeed_kt = 45;
var cp1_pitch_deg = -5;
var cp1_roll_deg = 0;
var cp1_heading_deg = 90;

# constants checkpoint 2
var cp2_aileron = 0;
var cp2_elevator = 0.4;
var cp2_rudder = 0;
var cp2_flaps = 1;
var cp2_throttle = 0.3;
var cp2_mixture = 0.5;
var cp2_latitude_deg = 21.3252466948;
var cp2_longitude_deg = -157.946;
var cp2_altitude_ft = 66;
var cp2_airspeed_kt = 33;
var cp2_pitch_deg = -5;
var cp2_roll_deg = 0;
var cp2_heading_deg = 90;

# constants timeout
var reset_timeout = 1;

# functions
var set_cp1 = func(val) {
    setprop("/wipro/reset_cp1", val);
}

var set_cp2 = func(val) {
    setprop("/wipro/reset_cp2", val);
}

var initialize_reset_props = func {
    set_cp1(0);
    set_cp2(0);
}

var pause_sim = func {
    setprop("/sim/freeze/clock", 1);
}

var continue_sim = func {
    setprop("/sim/freeze/clock", 0);
}

var reset_timer = maketimer(reset_timeout, func {
    continue_sim();
});

var reset_checkpoint = func(aileron, elevator, rudder, flaps, throttle, mixture,
                            latitude_deg, longitude_deg, altitude_ft,
                            airspeed_kt, pitch_deg, roll_deg, heading_deg) {
    pause_sim();

    # set environmental settings
    setprop("/position/latitude-deg", latitude_deg);
    setprop("/position/longitude-deg", longitude_deg);
    setprop("/position/altitude-ft", altitude_ft);

    setprop("/orientation/pitch-deg", pitch_deg);
    setprop("/orientation/roll-deg", roll_deg);
    setprop("/orientation/heading-deg", heading_deg);

    # repair all damage
    c172p.repair_damage();

    # set flight controls
    setprop("/controls/flight/aileron", aileron);
    setprop("/controls/flight/elevator", elevator);
    setprop("/controls/flight/rudder", rudder);
    setprop("/controls/flight/flaps", flaps);
    setprop("/controls/engines/current-engine/throttle", throttle);
    setprop("/controls/engines/current-engine/mixture", mixture);

    # set airspeed
    setprop("/velocities/airspeed-kt", airspeed_kt);

    # start the engine if not already running
    if (!getprop("/engines/active-engine/running")) {
        c172p.autostart();
	}

	reset_timer.restart(reset_timeout);
}

var reset_checkpoint1 = func {
    reset_checkpoint(cp1_aileron, cp1_elevator, cp1_rudder, cp1_flaps, cp1_throttle, cp1_mixture,
                     cp1_latitude_deg, cp1_longitude_deg, cp1_altitude_ft, cp1_airspeed_kt,
                     cp1_pitch_deg, cp1_roll_deg, cp1_heading_deg);
}

var reset_checkpoint2 = func {
    reset_checkpoint(cp2_aileron, cp2_elevator, cp2_rudder, cp2_flaps, cp2_throttle, cp2_mixture,
                     cp2_latitude_deg, cp2_longitude_deg, cp2_altitude_ft, cp2_airspeed_kt,
                     cp2_pitch_deg, cp2_roll_deg, cp2_heading_deg);
}

setlistener("/sim/signals/fdm-initialized", func {
    initialize_reset_props();

    setlistener("/wipro/reset_cp1", func {
        if(getprop("/wipro/reset_cp1") == 1) {
            reset_checkpoint1();
        }
        set_cp1(0);
    });

    setlistener("/wipro/reset_cp2", func {
        if(getprop("/wipro/reset_cp2") == 1) {
            reset_checkpoint2();
        }
        set_cp2(0);
    });
});
