#!/usr/bin/env python2

'''
Light management Python script
(C) Ngoc Tran, 2016

This includes some light management codes for my personal use, it should not
be too hard to deduce what does what.
'''

from time import time
import thread
from colorsys import hsv_to_rgb
import sys
import socket
from ledctrl import *

# preset management part

# copied somewhere online, thank you very much and sorry I could not credit you
def incoming(host, port):
  '''Open specified port and return file-like object'''
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # set SOL_SOCKET.SO_REUSEADDR=1 to reuse the socket if
  # needed later without waiting for timeout (after it is
  # closed, for example)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(0)   # do not queue connections
  request, addr = sock.accept()
  return request.makefile('r', 0)

def portListener(host, port):
  while True:
    for line in incoming(host, port):
      if len(line)>6:
        line = line[0:6]
      print 'data incoming to port', port,': ', line
      if len(line)==6:
      	try:
          red = int(line[0:2],16)
          green = int(line[2:4],16)
          blue = int(line[4:6],16)
          print 'Custom light color detected.'
          setColor(red, green, blue)
          if (red+green+blue == 0):
            print 'Light turned off.'
        except:
          pass

# cycle through hue, the higher the peak the more changed
def hueIncrement(hue,x):
  hue += x**4
  if (hue>1):
    hue-=1
  return hue

hue = 0.

thread.start_new_thread(portListener, ('', 2112))
r,g,b = hsv_to_rgb(hue, 1, 1)
setColor(r,g,b)

while True:
  pass

