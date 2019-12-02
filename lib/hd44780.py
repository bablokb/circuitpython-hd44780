# -----------------------------------------------------------------------------
# CircuitPython library for the HD44780 with serial interface (PCF8574T)
#
# This code is from https://github.com/CaptainStouf/raspberry_lcd4x20_I2C
# released under the GPL 2
#
# Adapted to CircuitPython with minor modifications by Bernhard Bablok
#
# Website: https://github.com/bablokb/circuitpython-hd44780
#
# -----------------------------------------------------------------------------

import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

class HD44780(object):
  # LCD Address
  ADDRESS = 0x27

  # commands
  CLEARDISPLAY = 0x01
  RETURNHOME = 0x02
  ENTRYMODESET = 0x04
  DISPLAYCONTROL = 0x08
  CURSORSHIFT = 0x10
  FUNCTIONSET = 0x20
  SETCGRAMADDR = 0x40
  SETDDRAMADDR = 0x80

  # flags for display entry mode
  ENTRYRIGHT = 0x00
  ENTRYLEFT = 0x02
  ENTRYSHIFTINCREMENT = 0x01
  ENTRYSHIFTDECREMENT = 0x00

  # flags for display on/off control
  DISPLAYON = 0x04
  DISPLAYOFF = 0x00
  CURSORON = 0x02
  CURSOROFF = 0x00
  BLINKON = 0x01
  BLINKOFF = 0x00

  # flags for display/cursor shift
  DISPLAYMOVE = 0x08
  CURSORMOVE = 0x00
  MOVERIGHT = 0x04
  MOVELEFT = 0x00

  # flags for function set
  F_4BITMODE = 0x00
  F_2LINE = 0x08
  F_5x8DOTS = 0x00

  # flags for backlight control
  BACKLIGHT = 0x08
  NOBACKLIGHT = 0x00

  EN = 0b00000100 # Enable bit
  RS = 0b00000001 # Register select bit

  # line address
  LINE = [0x80,0xC0,0x94,0xD4]

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,i2c=None,address=ADDRESS,trans_map={}):
    if i2c is None:
      i2c = busio.I2C(board.SCL,board.SDA)
    self._device = I2CDevice(i2c,address)
    self.trans_map = trans_map

    self._write(0x03)
    self._write(0x03)
    self._write(0x03)
    self._write(0x02)

    self._write(HD44780.FUNCTIONSET |
                HD44780.F_2LINE | HD44780.F_5x8DOTS | HD44780.F_4BITMODE)
    self._write(HD44780.DISPLAYCONTROL | HD44780.DISPLAYON)
    self._write(HD44780.CLEARDISPLAY)
    self._write(HD44780.ENTRYMODESET | HD44780.ENTRYLEFT)
    time.sleep(0.2)

  # --- set backlight status   -----------------------------------------------
  
  def backlight(self,on):
    if on:
      self._write_to_i2c(HD44780.BACKLIGHT)
    else:
      self._write_to_i2c(HD44780.NOBACKLIGHT)

  # --- display a string on the given line   ---------------------------------

  def write(self,string,line):
    self._write(HD44780.LINE[line-1])
    for char in string:
      if char in self.trans_map:
        self._write(self.trans_map[char],HD44780.RS)
      else:
        self._write(ord(char),HD44780.RS)

  # --- clear the LCD and move cursor to home   -------------------------------

  def clear(self):
    self._write(HD44780.CLEARDISPLAY)
    self._write(HD44780.RETURNHOME)

  # --- write a command to lcd   --------------------------------------------
  
  def _write(self, cmd, mode=0):
    self._write_four_bits(mode | (cmd & 0xF0))
    self._write_four_bits(mode | ((cmd << 4) & 0xF0))

  # --- write four bits   ---------------------------------------------------
  
  def _write_four_bits(self, data):
    self._write_to_i2c(data | HD44780.BACKLIGHT)
    self._strobe(data)

  # --- clocks EN to latch command   -----------------------------------------
  
  def _strobe(self, data):
    self._write_to_i2c(data | HD44780.EN | HD44780.BACKLIGHT)
    time.sleep(.0005)
    self._write_to_i2c(((data & ~HD44780.EN) | HD44780.BACKLIGHT))
    time.sleep(.0001)

  # --- write data to the bus   ----------------------------------------------

  def _write_to_i2c(self,data):
    with self._device:
      self._device.write(bytes([data]))
    time.sleep(0.0001)
