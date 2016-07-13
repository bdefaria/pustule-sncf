SUMMARY = "Main application init"
DESCRIPTION = "Autostart files main application"


INIT_FILE = "app-init"
INITSCRIPT_PARAMS = "start 80 5 . stop 80 0 1 6 ."

require init.inc
