#!/usr/bin/env python3

DO_8ENCODER=True
DO_4ENCODER=False
DO_OLED=False

from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import socket
from threading import Thread

if DO_8ENCODER or DO_4ENCODER or DO_OLED:
  import board
  import busio
if DO_8ENCODER:
  from M58Encoder import M58Encoder
if DO_OLED:
  import adafruit_ssd1306
  from PIL import Image, ImageDraw, ImageFont

# patch settings for my purposes
socket.setdefaulttimeout(60)
ThreadingOSCUDPServer.allow_reuse_address = True

class BiDirectionalClient(udp_client.SimpleUDPClient):
  def __init__(self, address: str, port: int, allow_broadcast: bool = False) -> None:
    super().__init__(address, port, allow_broadcast)
    self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._sock.bind(('', 0))
    self.client_port = self._sock.getsockname()[1]
    self.address = address


class HardwareUi(Thread):
  def __init__(self, pd):
    Thread.__init__(self)
    self.pd = pd
    if DO_8ENCODER or DO_4ENCODER or DO_OLED:
      bus = busio.I2C(board.SCL, board.SDA)
    if DO_OLED:
      self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, bus, addr=0x3c)
      self.screen = Image.new("1", (self.oled.width, self.oled.height))
      self.draw = ImageDraw.Draw(self.screen)
    if DO_4ENCODER:
      self.rotaries = [0,0,0,0]
      self.buttons = [0,0,0,0,0]
      # TODO: similar stuff to 8encoder
    if DO_8ENCODER:
      self.rotaries = [0,0,0,0,0,0,0,0]
      self.buttons = [0,0,0,0,0,0,0,0]
      self.m5e = M58Encoder(bus)
      print(f"version: {self.m5e.get_firmware_version()} - 0x{self.m5e.get_address():02x}")
      self.switch = self.m5e.get_switch_value()
      self.pd.send_message("/sw", self.switch)
      for i in range(8):
        self.m5e.set_encoder_value(i, 0)
        self.pd.send_message("/rot", [i, self.rotaries[i]])
        self.pd.send_message("/btn", [i, self.buttons[i]])

  def run(self):
    while True:
      if DO_OLED:
        self.oled.image(self.screen)
        self.oled.show()
      if DO_4ENCODER:
        # TODO: similar stuff to 8encoder
        pass
      if DO_8ENCODER:
        old = self.switch
        self.switch =  self.m5e.get_switch_value()
        if self.switch != old:
          self.pd.send_message("/sw", self.switch)
        for i in range(8):
          old = self.rotaries[i]
          self.rotaries[i] = self.m5e.get_encoder_value(i) % 255
          if self.rotaries[i] != old:
            self.pd.send_message("/rot", [i, self.rotaries[i]])
          old = self.buttons[i]
          if self.m5e.is_button_down(i):
            self.buttons[i] = 1
          else:
            self.buttons[i] = 0
          if self.buttons[i] != old:
            self.pd.send_message("/btn", [i, self.buttons[i]])

  def rgb(self, index,  r, g, b):
    if (DO_4ENCODER and index > 3) or (DO_8ENCODER and index > 7):
      print(f'rgb: {index} too high')
    else:
      if DO_8ENCODER:
        self.m5e.set_led_color_rgb(index, r, g, b)
      else:
        print(f'rgb {index}: {r}, {g}, {b}')

  def hsv(self, index, h, s, v):
    if (DO_4ENCODER and index > 3) or (DO_8ENCODER and index > 7):
      print(f'hsv: {index} too high')
    else:
      if DO_8ENCODER:
        self.m5e.set_led_color_hsv(index, h, s, v)
      else:
        print(f'hsv {index}: {h}, {s}, {v}')

  def rot(self, index, value):
    if (DO_4ENCODER and index > 3) or (DO_8ENCODER and index > 7):
      print(f'rot: {index} too high')
    else:
      if DO_8ENCODER:
        self.m5e.set_encoder_value(index, value)
      else:
        print(f'rot {index} ({color}): {value} ')

  def text(self, color, x, y, text):
    if DO_OLED:
      self.draw.text((x,y), text, fill=color)
    else:
      print(f'text ({color}) {x}x{y}: {text}')

  def rect(self, color, x, y, w, h):
    if DO_OLED:
      self.draw.rectangle((x, y, w, f), fill=color)
    else:
      print(f'rect ({color}): {x}x{y} - {w}x{h}')

  def graph(self, color, x, y, w, h, data):
    print(f"graph ({color}): {x}x{y} - {w}x{h} - {nums}")


if __name__ == '__main__':
  client = BiDirectionalClient("127.0.0.1", 8000)
  ui = HardwareUi(client)
  ui.start()

  def h_rgb(_a, index, r, g, b):
    ui.rgb(index, r, g, b)

  def h_hsv(_a, index, h, s, v):
    ui.hsv(index, h, s, v)

  def h_rot(_a, index, val):
    ui.rot(index, val)

  def h_text(_a, color, x, y, *ta):
    ui.text(color, x, y, " ".join(ta))

  def h_rect(_a, color, x, y, w, h):
    ui.rect(color, x, y, w, h)

  def h_graph(_a, color, x, y, w, h, *nums):
    ui.graph(color, x, y, w, h, nums)

  def h_default(*a):
    print("from pd", a)

  dispatcher = Dispatcher()
  dispatcher.map("/rgb", h_rgb)
  dispatcher.map("/hsv", h_hsv)
  dispatcher.map("/rot", h_rot)
  dispatcher.map("/text", h_text)
  dispatcher.map("/rect", h_rect)
  dispatcher.map("/graph", h_graph)
  dispatcher.set_default_handler(h_default)

  server = ThreadingOSCUDPServer((client.address, client.client_port), dispatcher)
  server.serve_forever()
