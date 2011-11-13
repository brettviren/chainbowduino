#!/usr/bin/env python

import serial
import time
import random
import math

ser = serial.Serial('/dev/ttyUSB1',9600)

def ShowChar(addr,char,r,g,b,s):
    data = ['R', chr(0x01), chr(s), chr(r), chr(g), chr(b), chr(char)]
    print chr(char)
    for ch in data:
        ser.write(ch)
        time.sleep(0.002)
        continue
    return

def ShowColor(r,g,b,char,s=0):
    data = ['R', chr(0x02), chr(s), chr(r), chr(g), chr(b), chr(char)]
    print chr(char)
    for ch in data:
        ser.write(ch)
        time.sleep(0.002)
        continue
    return



def pics(s=0):
    for n in range(4):
        print n
        data = ['R', chr(0x00), chr(s), chr(0x00), chr(0x00), chr(0x00), chr(n)]
        for ch in data:
            ser.write(ch)
            time.sleep(0.002)
            continue
        time.sleep(0.2)
        continue
    return
        

def count():
    for start,num in [('0',10)]:
        for n in range(num):
            num = ord(start) + n
            ShowChar(0,num,15,0,0,0)
            time.sleep(0.050)
            continue
        continue
    return


def cycle_colors():
    for red in range(10):
        red *= 25
        for green in range(10):    
            green *= 25
            for blue in range(10):
                blue *= 25
                print red,green,blue
                ShowColor(red,green,blue,ord('X'))
                time.sleep(0.005)
                continue
            continue
        continue
    return

def do_random():
    for n in range(1000):
        row = int(random.uniform(0,8))
        col = int(random.uniform(0,8))
        r = int(random.uniform(0,255))
        g = int(random.uniform(0,255))
        b = int(random.uniform(0,255))
        data = ['R',chr(0x3),chr(row),chr(col),chr(r),chr(g),chr(b)]
        for ch in data:
            ser.write(ch)
            #time.sleep(0.002)
            continue
        #time.sleep(0.050)
        continue
    return

def do_scale():
    green=0
    for row in range(8):
        red = row*2+1
        for col in range(8):
            blue = col*2+1
            mag = math.sqrt(float(red**2 + blue**2 + green**2))
            r = int((16.0*red)/mag)
            g = int((16.0*green)/mag)
            b = int((16.0*blue)/mag)
            print mag,r,g,b,red,green,blue
            data = ['R',chr(0x3),chr(row),chr(col),chr(r),chr(g),chr(b)]
            for ch in data:
                ser.write(ch)
                continue
            continue
        continue
    return

do_scale()

