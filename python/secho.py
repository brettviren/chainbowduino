#!/usr/bin/env python

import serial
import sys

ser = serial.Serial('/dev/ttyUSB0',9600)

def dispatch(addr,word):
    header = ['P',chr(addr),chr(len(word))]    
    for char in header:
        ser.write(char)
        print ord(char)
    for char in word:
        ser.write(char)

for word in sys.argv[1:]:
    dispatch(0,word)
    dispatch(1,word)
    dispatch(2,word)

    
