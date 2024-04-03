#!/usr/bin/env python3

from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import socket

class BiDirectionalClient(udp_client.SimpleUDPClient):
  def __init__(self, address: str, port: int, allow_broadcast: bool = False) -> None:
    super().__init__(address, port, allow_broadcast)
    self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._sock.bind(('', 0))
    self.client_port = self._sock.getsockname()[1]
    self.address = address

client = BiDirectionalClient("127.0.0.1", 8000)

# test client
client.send_message("/sw", 1)
client.send_message("/sw", 0)

def h_rgb(_a, index, r, g, b):
  print(f'rgb({index}): ({r}, {g}, {b})')

def h_hsv(_a, index, h, s, v):
  print(f'hsv({index}): ({h}, {s}, {v})')

def h_rot(_a, index, val):
  print(f'rot({index}): {val} / 255')

def h_text(_a, color, x, y, *ta):
  text = " ".join(ta)
  print(f'text ({color}): {x}x{y} {text}')

def h_rect(_a, color, x, y, w, h):
  print(f'rect ({color}): {x}x{y} - {w}x{h}')

def h_graph(_a, color, x, y, w, h, *nums):
  print(f"graph ({color}): {x}x{y} - {w}x{h} - {nums}")

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

ThreadingOSCUDPServer.allow_reuse_address = True
server = ThreadingOSCUDPServer((client.address, client.client_port), dispatcher)
server.serve_forever() 