#!/usr/bin/env python
'''
Test the individual matrices.
'''


from rainbowduino import matrices, comm
from random import randint
import time
import math

commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

# 8,0 --> 15,7
for addr in range(3):
    leds.add_matrix(addr,(0+addr*8,0),(7+addr*8,7))

leds.set_clear()

def do_rainbow(bright):
    for col in range(24):
        leds.set_pixel((col,0+col/4),(bright,0,0))
        leds.set_pixel((col,1+col/4),(0,bright,0))
        leds.set_pixel((col,2+col/4),(0,0,bright))


RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
VIOLET = (1,0,1)
YELLOW = (0,1,1)
AQUA = (1,1,0)
BLACK = (0,0,0)
WHITE = (1,1,1)

colors = [RED,GREEN,BLUE,VIOLET,YELLOW,AQUA,WHITE,BLACK]

def color_alpha(index, brightness):
    return map(lambda x: x*brightness, colors[index])


def do_sine(extra_offset = 0):
    for col in range(24):
        brightness = int(16.0*col/24.0)
        for off in range(8):
            angle = 3.14159*col/24.0
            row = (int(math.sin(angle)*8)+off+extra_offset)%8
            leds.set_pixel((col,row),color_alpha(off,brightness))

def do_scroll_string(string,delay,color):
    '''
    Scroll through the given string 
    '''
    nchars = 3
    string = string.strip()
    length = len(string)
    string += " "*nchars
    leds.set_clear()
    for ind in range(length+1):
        for ichar in range(nchars):
            ichar = nchars-ichar-1
            leds.set_ascii(string[ind+ichar],(ichar*8,0),color)
            continue
        time.sleep(delay)
        continue
    return
        

leds.set_clear()
for bright in range(15):
    do_rainbow(bright)
# r = range(15)
# r.reverse()
# for bright in r:
#     do_rainbow(bright)

while True:
    for off in range(8):
        do_sine(off)

#for color in colors[:-1]:
#    do_scroll_string(__doc__,0.1,color)
