
# globals
var initialized = 0;
var reset_ongoing = 0;
var cp_current = nil;
var cp_current_pitch = nil;
var cp_current_roll = nil;
var cp_current_heading = nil;
var cp_current_func = nil;

# random number generator
var random = func(min, max) {
    return min + (max - min) * rand();
}

# parameters checkpoint 1

var cp1 = {
    aileron: func { return random(-0.2, 0.2); },
    aileron_trim: 0,
    elevator: func { return random(-0.2, 0.2); },
    elevator_trim: 0,
    rudder: 0,
    rudder_trim: 0,
    flaps: 1,
    throttle: func { return random(0.7, 1); },
    mixture: func { return random(0.7, 1); },
    latitude_deg: func { return random(21.32522, 21.32526); },
    longitude_deg: func { return random(-157.948, -157.944); },
    altitude_ft: func { return random(66, 132); },
    airspeed_kt: func { return random(55, 100); },
    pitch_deg: func { return random(-5, 0); },
    roll_deg: func { return random(-5, 5); },
    heading_deg: func { return random(85, 95); },
    side_slip_deg: 0
};

# parameters checkpoint 2

var cp2 = {
    aileron: func { return 0.3; },
    aileron_trim: 0,
    elevator: func { return random(-0.18, -0.22); },
    elevator_trim: 0,
    rudder: 0,
    rudder_trim: 0,
    flaps: 1,
    throttle: func { return 0; },
    mixture: func { return 0.9; },
    latitude_deg: func { return random(21.32515, 21.32535); },
    longitude_deg: func { return -157.942; },
    altitude_ft: func { return random(49, 51); },
    airspeed_kt: func { return 42; },
    pitch_deg: func { return 0; },
    roll_deg: func { return 0; },
    heading_deg: func { return 89.9; },
    side_slip_deg: 0
};

# var cp2 = {
#     aileron: func { return 0; },
#     aileron_trim: 0,
#     elevator: func { return random(0, 0.3); },
#     elevator_trim: 0,
#     rudder: 0,
#     rudder_trim: 0,
#     flaps: 1,
#     throttle: func { return random(0.7, 1); },
#     mixture: func { return random(0.8, 1); },
#     latitude_deg: func { return 21.325247; },
#     longitude_deg: func { return -157.9435; },
#     altitude_ft: func { return 95; },
#     airspeed_kt: func { return 65; },
#     pitch_deg: func { return -3; },
#     roll_deg: func { return 0; },
#     heading_deg: func { return 89.9; },
#     side_slip_deg: 0
# };

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

var reset_checkpoint = func(cp, cp_func) {
    reset_ongoing = 1;
    cp_current = cp;
    cp_current_func = cp_func;

    # set environmental settings
    setprop("/sim/presets/latitude-deg", cp_current.latitude_deg());
    setprop("/sim/presets/longitude-deg", cp_current.longitude_deg());
    setprop("/sim/presets/altitude-ft", cp_current.altitude_ft());

    cp_current_pitch = cp_current.pitch_deg();
    cp_current_roll = cp_current.roll_deg();
    cp_current_heading = cp_current.heading_deg();

    setprop("/sim/presets/pitch-deg", cp_current_pitch);
    setprop("/sim/presets/roll-deg", cp_current_roll);
    setprop("/sim/presets/heading-deg", cp_current_heading);
    setprop("/sim/presets/side-slip-deg", cp_current.side_slip_deg);

    setprop("/sim/presets/airspeed-kt", cp_current.airspeed_kt());

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

# listeners
setlistener("/sim/signals/fdm-initialized", func {
    initialize_reset_props();
});

setlistener("/sim/signals/reinit", func {
    if(!getprop("/sim/signals/reinit")) {
        # reset repairing flag
        setprop("/fdm/jsbsim/damage/repairing", 0);

        # reset date / time
        setprop("/sim/time/gmt", "2018-11-11T23:00:00");

        # reset fuel freeze
        setprop("/sim/freeze/fuel", 1);

        # reset engine properties
        setprop("/engines/active-engine/oil_consumption_allowed", 0);
        setprop("/engines/active-engine/carb_icing_allowed", 0);
        setprop("/engines/active-engine/coughing", 0);
        setprop("/engines/active-engine/cranking", 0);
        setprop("/engines/active-engine/crash-engine", 0);
        setprop("/engines/active-engine/crashed", 0);
        setprop("/engines/active-engine/damage_allowed", 0);
        setprop("/engines/active-engine/kill-engine", 0);
        setprop("/engines/active-engine/killed", 0);
        setprop("/engines/active-engine/oil-level", 7);
        setprop("/engines/active-engine/oil-lacking", 0);
        setprop("/engines/active-engine/running", 1);

        # reset fuel properties
        setprop("/consumables/fuel/contamination_allowed", 0);
        setprop("/consumables/fuel/tank[0]/empty", 0);
        setprop("/consumables/fuel/tank[0]/level-gal_us", 19.8);
        setprop("/consumables/fuel/tank[0]/water-contamination", 0);
        setprop("/consumables/fuel/tank[1]/empty", 0);
        setprop("/consumables/fuel/tank[1]/level-gal_us", 19.8);
        setprop("/consumables/fuel/tank[1]/water-contamination", 0);

        settimer(func {
            # reset orientation
            setprop("/orientation/pitch-deg", cp_current_pitch);
            setprop("/orientation/roll-deg", cp_current_roll);
            setprop("/orientation/heading-deg", cp_current_heading);
            setprop("/orientation/side-slip-deg", cp_current.side_slip_deg);

            # set flight controls
            setprop("/controls/flight/aileron", cp_current.aileron());
            setprop("/controls/flight/aileron-trim", cp_current.aileron_trim);
            setprop("/controls/flight/elevator", cp_current.elevator());
            setprop("/controls/flight/elevator-trim", cp_current.elevator_trim);
            setprop("/controls/flight/rudder", cp_current.rudder);
            setprop("/controls/flight/rudder-trim", cp_current.rudder_trim);
            setprop("/controls/flight/flaps", cp_current.flaps);
            setprop("/controls/engines/current-engine/mixture", cp_current.mixture());
            setprop("/controls/engines/current-engine/throttle", cp_current.throttle());
            setprop("/controls/gear/brake-left", 0);
            setprop("/controls/gear/brake-right", 0);

            # reset completed
            reset_ongoing = 0;
            cp_current_func(0);
            setprop("/sim/freeze/clock", 0);
        }, 1, 1);
        setprop("/sim/freeze/clock", 1);
    }
});
