#!/usr/bin/env python
'''
Implement Fade sketch by send data down serial to the Dimmer sketch
'''

import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)

brightness = 0
fadeAmount = 5
while True:
    #print brightness
    ser.write(chr(brightness))
    brightness += fadeAmount
    if (brightness == 0 or brightness == 255):
        fadeAmount = -fadeAmount
        pass
    time.sleep(0.030)
    continue
