#!/usr/bin/env python
'''
Test the color packing routines.
'''

from rainbowduino import matrices, comm
from random import randint
import time
import math

commObj = comm.SerialComm()

def test_pack_color():
    check_color(1,2,3)
    return

def test_pack_colors():
    check_colors(1,2,3, 4,5,6)
    return

def check_color(r,g,b):
    one, two = map(ord,commObj.pack_color((r,g,b)))
    print '(%d,%d,%d) 0x0%x 0x%x%x 0x%x 0x%x' % (r,g,b,b,g,r,one, two)
    assert one == b, 'Got badly packed first byte: 0x%x' % one
    assert two == g<< 4 | r, 'Got badly packed second byte: 0x%x' % two

def check_colors(r,g,b,R,G,B):
    one, two, three = map(ord,commObj.pack_colors( [(r,g,b),(R,G,B)] ) )
    print '(%d,%d,%d),(%d,%d,%d) 0x%x%x 0x%x%x 0x%x%x 0x%x 0x%x 0x%x' % \
        (r,g,b,R,G,B, r,g,b,R,G,B, one, two, three)

test_pack_color()
test_pack_colors()
