#!/usr/bin/env python

import sys, serial, string
try:
    device = sys.argv[1]
except IndexError:
    device = '/dev/ttyUSB1'
try:
    baudrate = int(sys.argv[2])
except IndexError:
    baudrate = 9600

ser = serial.Serial(device,baudrate)
while True:
    val = ser.read()
    sys.stderr.write(val)


    
