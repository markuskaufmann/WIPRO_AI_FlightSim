
# globals
var initialized = 0;

var initialize_exit_props = func {
    if(initialized == 0) {
        setprop("/wipro/fg_exit", 0);
        setlistener("/wipro/fg_exit", func {
            if(getprop("/wipro/fg_exit") == 1) {
                settimer(fg_exit, 2, 1);
                setprop("/sim/freeze/clock", 1);
            }
        });
        initialized = 1;
    }
}

var fg_exit = func() {
    fgcommand("exit");
}

# listeners
setlistener("/sim/signals/fdm-initialized", func {
    initialize_exit_props();
});
