
var initialized = 0;
var reset_ongoing = 0;
var cp_current = nil;
var cp_current_func = nil;

# constants checkpoint 1
var cp1 = {
    aileron: 0,
    aileron_trim: 0,
    elevator: 0,
    elevator_trim: 0,
    rudder: 0,
    rudder_trim: 0,
    flaps: 1,
    throttle: 0.3,
    mixture: 0.7,
    latitude_deg: 21.3252466948,
    longitude_deg: -157.946,
    altitude_ft: 66,
    airspeed_kt: 45,
    ubody_fps: 75.9514,
    vbody_fps: 0,
    wbody_fps: 0,
    pitch_deg: 0,
    roll_deg: 0,
    heading_deg: 90,
    side_slip_deg: 0
};

# constants checkpoint 2
var cp2 = {
    aileron: 0,
    aileron_trim: 0,
    elevator: 0.1,
    elevator_trim: 0,
    rudder: 0,
    rudder_trim: 0,
    flaps: 1,
    throttle: 0.9,
    mixture: 0.95,
    latitude_deg: 21.3252466948,
    longitude_deg: -157.946,
    altitude_ft: 66,
    airspeed_kt: 85,
    pitch_deg: -3,
    roll_deg: 0,
    heading_deg: 89.9,
    side_slip_deg: 0
};

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
    if(initialized == 0) {
        set_cp1(0);
        set_cp2(0);
        setlistener("/wipro/reset_cp1", func {
            if(getprop("/wipro/reset_cp1") == 1) {
                if(reset_ongoing == 0) {
                    reset_checkpoint(cp1, set_cp1);
                }
            }
        });
        setlistener("/wipro/reset_cp2", func {
            if(getprop("/wipro/reset_cp2") == 1) {
                if(reset_ongoing == 0) {
                    reset_checkpoint(cp2, set_cp2);
                }
            }
        });
        initialized = 1;
    }
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

var reset_checkpoint = func(cp, cp_func) {
    reset_ongoing = 1;
    cp_current = cp;
    cp_current_func = cp_func;

    # set environmental settings
    setprop("/sim/presets/latitude-deg", cp_current.latitude_deg);
    setprop("/sim/presets/longitude-deg", cp_current.longitude_deg);
    setprop("/sim/presets/altitude-ft", cp_current.altitude_ft);

    setprop("/sim/presets/pitch-deg", cp_current.pitch_deg);
    setprop("/sim/presets/roll-deg", cp_current.roll_deg);
    setprop("/sim/presets/heading-deg", cp_current.heading_deg);
    setprop("/sim/presets/side-slip-deg", cp_current.side_slip_deg);

    setprop("/sim/presets/airspeed-kt", cp_current.airspeed_kt);

    # repair damage
    setprop("/fdm/jsbsim/damage/repairing", 1);
    setprop("/engines/active-engine/crash-engine", 0);
    setprop("/engines/active-engine/kill-engine", 0);

    # damage: landing gear
    setprop("/fdm/jsbsim/gear/unit[0]/broken", 0);
    setprop("/fdm/jsbsim/gear/unit[1]/broken", 0);
    setprop("/fdm/jsbsim/gear/unit[2]/broken", 0);

    # damage: wings
    setprop("/fdm/jsbsim/wing-damage/left-wing", 0);
    setprop("/fdm/jsbsim/wing-damage/right-wing", 0);

    # damage: collapsed wings
    setprop("/fdm/jsbsim/crash", 0);

    # damage: pontoons
    setprop("/fdm/jsbsim/pontoon-damage/left-pontoon", 0);
    setprop("/fdm/jsbsim/pontoon-damage/right-pontoon", 0);

    # damage: engine
    setprop("/fdm/jsbsim/engine/damage-level", 0);

    fgcommand("reposition");
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
});

setlistener("/sim/signals/reinit", func {
    if(!getprop("/sim/signals/reinit")) {

        # reset repairing flag
        setprop("/fdm/jsbsim/damage/repairing", 0);

        # start the engine if not already running
        # if (!getprop("/engines/active-engine/running")) {
        #     c172p.autostart();
        # }

        settimer(func {
            # reset orientation
            setprop("/orientation/pitch-deg", cp_current.pitch_deg);
            setprop("/orientation/roll-deg", cp_current.roll_deg);
            setprop("/orientation/heading-deg", cp_current.heading_deg);
            setprop("/orientation/side-slip-deg", cp_current.side_slip_deg);

            # set flight controls
            setprop("/controls/flight/aileron", cp_current.aileron);
            setprop("/controls/flight/aileron-trim", cp_current.aileron_trim);
            setprop("/controls/flight/elevator", cp_current.elevator);
            setprop("/controls/flight/elevator-trim", cp_current.elevator_trim);
            setprop("/controls/flight/rudder", cp_current.rudder);
            setprop("/controls/flight/rudder-trim", cp_current.rudder_trim);
            setprop("/controls/flight/flaps", cp_current.flaps);
            setprop("/controls/engines/current-engine/mixture", cp_current.mixture);
            setprop("/controls/engines/current-engine/throttle", cp_current.throttle);

            # reset completed
            reset_ongoing = 0;
            cp_current_func(0);
        }, 0.5);
    }
});
