#!usr/bin/env python 

import serial

class LedMatrix(object):
    def __init__(self, addr = 0, device = '/dev/ttyUSB0', baudrate = 9600):
        self.addr = 0
        return

    def pack_color(self,color):
        'Color is made by packing 3 4-bit components: red, green, blue into 2 bytes'
        r,g,b = color
        return ( b&0xf , ((g&0xf) << 4) | (r&0xf) )
    
    def set_pixel(self,col,row,color = (0xf,0xf,0xf)):
        pixel = ((col&0xf)<<4) | (row&0xf)
        color = self.pack_color(color)
        self.send( [ 'P', chr(pixel), chr(color[0]), chr(color[1]) ] )
        return

    def send(self,data):
        'Send a packet with the given data (list of chars)'
        tosend = ['P',chr(self.addr),chr(len(data))] + data
        for char in tosend:
            ser.write(char)
            continue
        return
