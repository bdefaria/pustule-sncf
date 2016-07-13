SUMMARY = "Main application init"
DESCRIPTION = "Autostart files main application"


INIT_FILE = "App-init"
INITSCRIPT_PARAMS = "start 99 5 . stop 99 0 1 6 ."

require init.inc
