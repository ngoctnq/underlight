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
from random import random
from ledctrl import *

# preset management part
valentine = False

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
  global valentine
  while True:
    for line in incoming(host, port):
      if len(line)>6:
        line = line[0:6]
      print 'data incoming to port', port,': ', line
      if len(line)==6:
        if line == 'alloff':
          valentine = False
        elif line == 'moodie':
          valentine = True
        else:
          try:
            red = int(line[0:2],16)
            green = int(line[2:4],16)
            blue = int(line[4:6],16)
            print 'Custom light color detected.'
            setColor(red, green, blue)
            if (red+green+blue == 0):
              print 'Light turned off.'
            valentine = False
          except:
            pass

minh = 190.
maxh = 320.
up_d = 1.
itrv = 0.01
loop = 10.
diff = maxh - minh
last = time()
hue = minh

thread.start_new_thread(portListener, ('', 2112))

while True:
  if valentine:
    now = time()
    if now-last < itrv:
      continue
    if now-last < 2 * itrv:
      hue += up_d * diff / loop * itrv
    last = now
    if hue > maxh:
      up_d = -1.
      hue = 2. * maxh - hue
    if hue < minh:
      up_d = 1.
      hue = 2 * minh - hue
    r,g,b = hsv_to_rgb(hue/360., 0.5, 1)
    r *= 255
    g *= 255
    b *= 255
    print r,g,b
    setColor(r,g,b)
