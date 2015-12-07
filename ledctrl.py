#!/usr/bin/env python2
import pigpio
from time import sleep

RED=17
GREEN=18
BLUE=27

GPIO=pigpio.pi()

def setRed(x):
  GPIO.set_PWM_dutycycle(RED,x)

def setGreen(x):
  GPIO.set_PWM_dutycycle(GREEN,x)

def setBlue(x):
  GPIO.set_PWM_dutycycle(BLUE,x)

def setColor(r,g,b):
  setRed(r)
  setGreen(g)
  setBlue(b)

def setWhite():
  GPIO.write(RED,1)
  GPIO.write(GREEN,1)
  GPIO.write(BLUE,1)

def setBlack():
  GPIO.write(RED,0)
  GPIO.write(GREEN,0)
  GPIO.write(BLUE,0)

def turnOn():
  setWhite()

def turnOff():
  setBlack()

for i in range(0,2):
  turnOn()
  sleep(0.1)
  turnOff()
  sleep(0.1)
print "ledctrl loaded."
