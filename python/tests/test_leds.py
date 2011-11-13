#!/usr/bin/env python

from rainbowduino import matrices, comm
from random import randint
import time


commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

leds.add_matrix(0,(0,0),(7,7))

def do_random():
    for nothing in range(1000):
        r = randint(0,15)
        g = randint(0,15)
        b = randint(0,15)
        col = randint(0,7)
        row = randint(0,7)
        leds.set_pixel((col,row), (r,g,b))

def do_alphabet():
    for letter in range(26):
        letter = chr(ord('A') + letter)
        print letter
        r = randint(0,15)
        g = randint(0,15)
        b = randint(0,15)
        leds.set_ascii(letter, (1,1), (r,g,b))
        time.sleep(0.05)
        continue
    return
    
def do_pattern():
    leds.set_clear();
    for n in range(16):
        leds.set_clear();
        leds.set_color((n,n,n));
    for n in range(16):
        n = 15 - n
        leds.set_clear();
        leds.set_color((n,n,n));

    leds.set_clear();
    time.sleep(0.1)

    for row in range(8):
        for col in range(8):
            
            r = 2*col+1
            g = 2*row+1
            b = randint(0,15)

            leds.set_pixel((col,row), (r,g,b))

            continue
        continue
    return
        
#do_alphabet()
do_pattern()

