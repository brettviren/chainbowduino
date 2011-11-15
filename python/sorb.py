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

def getline():
    ret = []
    while True:
        val = ser.read()
        if val == '\r':
            return ret
        ret.append(ord(val) & 0177)
    return None

def unpack_motion(line):
    key = "SpaceWare"
    c = []
    for ind,code in enumerate(key):
        val = line[ind]& 0177
        val ^= ord(code)
        c.append(val)
        continue
    t = []
    r = []
    t.append( ((c[0] & 0177)<<3)|((c[1] & 0160)>>4))
    t.append( ((c[1] & 0017)<<6)|((c[2] & 0176)>>1) )
    t.append( ((c[2] & 0001)<<9)|((c[3] & 0177)<<2)|((c[4] & 0140)>>5) )
    r.append( ((c[4] & 0037)<<5)|((c[5] & 0174)>>2) )
    r.append( ((c[5] & 0003)<<8)|((c[6] & 0177)<<1)|((c[7] & 0100)>>6) )
    r.append( ((c[7] & 0077)<<4)|((c[8] & 0170)>>3) )

    tt = []
    for x in t:
        if x > 511: x -= 1024
        tt.append(x)
    rr = []
    for x in r:
        if x > 511: x -= 1024
        rr.append(x)

    return tt,rr

while True:
    line = getline()
    if chr(line[0]) == 'D':
        t,r = unpack_motion(line[-9:])
        print "%4d,%4d,%4d --> %4d %4d %4d" % (t[0],t[1],t[2],r[0],r[1],r[2])
    else:
        print '%d: %s' % (len(line), str(line))


    
