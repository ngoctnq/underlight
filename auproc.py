#!/usr/bin/env python2

'''
Audio processing Python script
(C) Ngoc Tran, 2015

This includes some light management codes for my personal use, it should not
be too hard to deduce what does what.

Takes in audio data from stdin; in my case: shairport-sync.
Then, analyze the data, return corresponding RGB data for the LED to process.
'''

import alsaaudio
import audioop
from time import time
import thread
from colorsys import hsv_to_rgb
import sys
import socket
from ledctrl import *

# preset management part

headlight = False
customlgt = False
auproclgt = False
lasttime = 0.
turnedOn = 0.

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
  global headlight, customlgt, auproclgt, turnedOn
  while True:
    for line in incoming(host, port):
      if len(line)>6:
        line = line[0:6]
      print 'data incoming to port', port,': ', line
      if len(line)==6:
        if line == 'doorlt':
          print 'Doorlight code detected.'
          # if (not(customlgt) and not(auproclgt)):
          if not(customlgt):
            if headlight:
               turnedOn = time()
            else:
               thread.start_new_thread(doorCtrl, ())
        else:
          try:
            red = int(line[0:2],16)
            green = int(line[2:4],16)
            blue = int(line[4:6],16)
            headlight = False
            print 'Custom light color detected.'
            # if not(auproclgt):
            if True:
              customlgt = True
              setColor(red, green, blue)
              if (red+green+blue == 0):
                print 'Light turned off.'
                customlgt = False
          except:
            pass

def doorCtrl():
  global headlight, turnedOn
  print 'Headlight starting.'
  headlight = True
  setColor(255,255,255)
  turnedOn = time()
  notBroken = True
  while (time() - turnedOn < 60):
    if not(headlight):
      notBroken = False
      break
  print 'Headlight turned off,',
  if notBroken:
    setColor(0,0,0)
    print 'naturally.'
  else:
    print 'forced.'

# never used because of RPi's lack of juice
def audiomgmt():
  global lasttime, auproclgt, headlight, customlgt
  while True:
    # turn off after 1s without audio
    if (time() - lasttime < 1):
      auproclgt = True
      headlight = False
      customlgt = False
    elif auproclgt:
      auproclgt = False
      turnOff()

# audio part

BUFFER_RATE = 2**12
# threshold of drop
CHILL_MAX = 0.8

# Set up audio
stream = alsaaudio.PCM()
# this reduces the lag between audio output and LED
stream.setperiodsize(BUFFER_RATE/4)

# cycle through hue, the higher the peak the more changed
def hueIncrement(hue,x):
   hue += x**4
   if (hue>1):
      hue-=1
   return hue

hue = 0.
# last max peak
lastMax = 0.1

thread.start_new_thread(portListener, ('', 2112))
#thread.start_new_thread(audiomgmt, ())

while True:
   # Read data from sysin
   data = sys.stdin.read(BUFFER_RATE)
   # write audio out to speaker
   stream.write(data)
   headlight = False

   # get the max volume of the read data
   maxVol=audioop.max(data,2)
   # max ~ 28000, I think
   # convert to 1.0 scale
   maxUnit = min(1.0* maxVol / 28000 , 1.0)
   # increment the hue according to sound level
   hue = hueIncrement(hue,maxUnit)
   # avoid division by 0
   maxUnit = max(maxUnit, 0.1)
   # weight light adjustment depending on sound level
   if (maxUnit > CHILL_MAX):
      bias = lastMax/maxUnit * 6
   else:
      bias = 3
   # convert HSV to RGB
   # keep LED light up always with the value level always greater than 0.1
   r,g,b = hsv_to_rgb(hue, 1, max(0.1, maxUnit**bias))
   # update the last magnitude to compare with the next
   lastMax = maxUnit

   # update LED color
   setColor(int(r*255),int(g*255),int(b*255))

   # update last time with audio
   lasttime = time()