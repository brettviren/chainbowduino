#!/usr/bin/env python
from rainbowduino import matrices, comm
from random import randint
import time


commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

# 8,0 --> 15,7
for addr in range(3):
    leds.add_matrix(addr,(0+addr*8,0),(7+addr*8,7))

leds.set_clear()

def do_rainbow(bright):
    for col in range(24):
        leds.set_pixel((col,1+col/8),(bright,0,0))
        leds.set_pixel((col,2+col/8),(0,bright,0))
        leds.set_pixel((col,3+col/8),(0,0,bright))

leds.set_clear()
for bright in range(15):
    do_rainbow(bright)
r = range(15)
r.reverse()
for bright in r:
    do_rainbow(bright)

