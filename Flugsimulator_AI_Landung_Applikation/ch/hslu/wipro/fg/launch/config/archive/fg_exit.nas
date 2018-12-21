
# globals
var initialized = 0;

var initialize_exit_props = func {
    if(initialized == 0) {
        setprop("/wipro/exit", 0)
        setlistener("/wipro/exit", func {
            if(getprop("/wipro/exit") == 1) {
                gui.popupTip("Exit");
                fgcommand("exit");
            }
        });
        initialized = 1;
    }
}

# listeners
setlistener("/sim/signals/fdm-initialized", func {
    initialize_exit_props();
});
