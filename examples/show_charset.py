#!/usr/bin/python3
# -----------------------------------------------------------------------------
# This program prints the available charset to the display in chunks of
# 16 characters. Pass the chunk number (zero-based) to the program. To display
# the complete character-set, run
#
# ./show_charset.py $(seq 0 15)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-hd44780
#
# -----------------------------------------------------------------------------

import sys, time
import hd44780

SLEEP = 5
COLS  = 16
ROWS  = 2

display = hd44780.HD44780()

if COLS == 20:
  header = "    0123456789012345"
else:  
  header = "0123456789012345"

for chunk in sys.argv[1:]:
  chunk = int(chunk)
  if COLS == 20:
    col_header = header[:chunk+4] + "_" + header[chunk+5:]
    line = "%3d:" % (chunk*16)
  else:
    col_header = header[:chunk] + "_" + header[chunk+1:]
    line = ""
  for nr in range(chunk*16,chunk*16+16):
    line += (chr(nr))

  display.write(col_header,1)
  display.write(line,2)

  # and sleep
  time.sleep(SLEEP)

display.clear()
display.backlight(False)
