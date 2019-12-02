#!/usr/bin/python3
# -----------------------------------------------------------------------------
# CircuitPython library for the HD44780 with serial interface (PCF8574T)
#
# Sample code
#
# Website: https://github.com/bablokb/circuitpython-hd44780
#
# -----------------------------------------------------------------------------

import hd44780
display = hd44780.HD44780()
display.clear()
display.backlight(False)
