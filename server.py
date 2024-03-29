#!/usr/bin/env python

"""
This is the OSC UDP service that proxies hardware access for puredata.
"""

import board
import digitalio
import busio

ENCODER_ADDR         = 0x41
ENCODER_REG          = 0x00
INCREMENT_REG        = 0x20
BUTTON_REG           = 0x50
SWITCH_REG           = 0x60
RGB_LED_REG          = 0x70
RESET_COUNTER_REG    = 0x40
FIRMWARE_VERSION_REG = 0xFE
I2C_ADDRESS_REG      = 0xFF

# this is a port of https://github.com/m5stack/M5Unit-8Encoder/blob/main/src/UNIT_8ENCODER.cpp

class M58Encoder:
  def __init__(self, i2c):
    self.i2c = i2c

  def read_bytes(self, reg, result=bytearray(1)):
    i2c.writeto(ENCODER_ADDR, bytes([reg]))
    self.i2c.readfrom_into(ENCODER_ADDR, result)
    return result

  def is_button_down(self, index):
    """
    Check to see if a rotary pushbutton (0-7) is pressed
    """
    result = self.read_bytes(BUTTON_REG + index)
    if result[0] == 1:
      return False
    else:
      return True


# test

m5e = M58Encoder(busio.I2C(board.SCL, board.SDA))

while True:
  print([
    m5e.is_button_down(0),
    m5e.is_button_down(1),
    m5e.is_button_down(2),
    m5e.is_button_down(3),
    m5e.is_button_down(4),
    m5e.is_button_down(5),
    m5e.is_button_down(6),
    m5e.is_button_down(7)
  ])