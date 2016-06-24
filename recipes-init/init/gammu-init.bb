SUMMARY = "NW Kalea CAN configuration autostart"
DESCRIPTION = "Autostart files for NW Kalea CAN config"


INIT_FILE = "gammu-init"
INITSCRIPT_PARAMS = "start 80 5 . stop 80 0 1 6 ."

require init.inc
