#!/usr/bin/env python
from rainbowduino import matrices, comm
from random import randint
import time
import sys

commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

leds.add_matrix(0,(1,1),(8,8))

while True:
    letter = sys.stdin.read(1)
    if letter == '\n': continue
    if not letter: break
    print letter,ord(letter)

    r = randint(0,15)
    g = randint(0,15)
    b = randint(0,15)
    leds.set_ascii(letter, (1,1), (r,g,b))
