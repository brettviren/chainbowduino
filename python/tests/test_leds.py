#!/usr/bin/env python

from rainbowduino import matrices, comm
from random import randint
import time


commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

for addr in range(3):
    leds.add_matrix(addr,(0+addr,0),(7+addr,7))

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
        #print letter
        r = randint(0,15)
        g = randint(0,15)
        b = randint(0,15)
        leds.set_ascii(letter, (1,1), (r,g,b))
        continue
    return
    
def do_pattern():
    leds.set_clear()
    for n in range(16):
        leds.set_clear()
        leds.set_color((n,n,n))
    for n in range(16):
        n = 15 - n
        leds.set_clear()
        leds.set_color((n,n,n))

    leds.set_clear()

    for row in range(8):
        for col in range(8):
            
            r = 2*col+1
            g = 2*row+1
            #b = randint(0,15)
            b = 1

            leds.set_pixel((col,row), (r,g,b))

            continue
        continue
    return
        
def do_gradient():
    leds.set_clear()
    #16 12 8 4 0
    red_grad   = [15,11, 7, 3, 0, 0, 0,15]
    green_grad = [ 0, 3, 7,11, 7, 3, 0,15]
    blue_grad  = [ 0, 0, 0, 3, 7,11,15,15]
    for col in range(8):
        for row,(r,g,b) in enumerate(zip(red_grad,green_grad,blue_grad)):
            leds.set_pixel((col,row), (r,g,b))
            continue
        continue

import time
def do_flash():
    while True:
        leds.set_clear()
        time.sleep(.1)
        leds.set_color((15,15,15))
        time.sleep(.1)
        continue
    return

def do_show_addr():
    for addr in leds.addresses():
        print 'Address %d show me your address' % addr
        leds.comm.set_show_addr(addr)
        continue
    return


do_show_addr()


