#!/usr/bin/env python
'''
Implement Fade sketch by send data down serial to the Dimmer sketch
'''

import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
fanfile = '/sys/devices/platform/thinkpad_hwmon/fan1_input'
fp = open(fanfile)
maxrpm = 3000

brightness = 0
lastBrightness = 0
fadeAmount = 5
while True:
    fp.seek(0)
    val = int(fp.read().strip())
    print val
    if val == 65535:
        val = 0
    if val > maxrpm:
        val = maxrpm

    brightness = int((255.0 * val) / maxrpm)

    if brightness != lastBrightness:
        lastBrightness = brightness
        ser.write(chr(brightness))
        print val,brightness

    time.sleep(1)
    continue
