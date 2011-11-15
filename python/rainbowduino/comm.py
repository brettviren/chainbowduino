#!/usr/bin/env python
'''
Implement communication protocol to a set of addressible LED matrices.

Pixels are (column,row) tuples starting at (0,0) at top of matrix.

Colors are (red,green,blue) triples, each componenet is limited to 4bits.
'''

class TestComm(object):
    def __init__(self):
        return

    def set_pixel(self,addr,pixel,color):
        '''
        Set one pixel of the matrix at the given address to the given color
        '''
        print '%x (%d,%d) (%x,%x,%x)' % (addr, pixel[0], pixel[1], color[0], color[1], color[2])

    def set_column(self,addr,col,colors):
        '''
        Set the given column of the matrix at the given address to the given color.
        '''
        print '%x column %d' % (addr, col)
        for color in colors:
            print '\t(%x,%x,%x)' % color
        return

    def set_row(self,addr,row,colors):
        '''
        Set the given row of the matrix at the given address to the given color.
        '''
        print '%x row %d' % (addr, row)
        for color in colors:
            print '\t(%x,%x,%x)' % color
        return
        
    def set_all(self,addr,color):
        '''
        Set all LEDs to the given color
        '''
        print '%x all (%x,%x,%x)' % (addr, color[0], color[1], color[2])
        return

    def set_matrix(self,addr,matrix):
        '''
        Set a full matrix of colors.  The matrix is a list of rows,
        each row a list of colors.
        '''
        print '%x' % addr
        for row in matrix:
            print '\t'
            for color in row:
                print '(%x,%x,%x) ' % color
            print '\n'
            continue
        return


class SerialComm(object):
    '''
    Match serial communication protocol of comm.cpp
    '''
    def __init__(self, device = '/dev/ttyUSB0', baudrate = 9600):
        import serial
        self.ser = serial.Serial(device,baudrate,timeout=1)
        self.count = 0
        return

    def send(self, addr, data):
        '''
        Packetize and send data to the serial line to the matrix with
        the given address.  Data should be byte characters.  Use
        "chr()" if you need to send a number.
        '''
        import time
        if self.count == 255: 
            self.count = 0
        self.count += 1
        tosend = [chr(addr), chr(self.count), chr(len(data))] + data + [chr(0)]
        print 'Send to %x #%d %d cmd "%s"' % (addr,self.count,len(data),data[0])
        for char in tosend:
            self.ser.write(char)
            continue

        reply = self.ser.read(3)
        if len(reply) != 3:
            print 'Packet %d FAILED: got only %d bytes' % (self.count, len(reply))
            return

        okno = reply[:2]
        count = ord(reply[2])
        if okno == 'NO' or count != self.count:
            print 'Packet %d FAILED: got %s%d' % (self.count, okno, count)
        else:
            print 'Packet %d ok' % self.count

        return

    def pack_pixel(self, pixel):
        '''
        Return pixel packed ready to send as a single character list
        '''
        return [chr( ((pixel[0]&0xf) << 4) | (pixel[1]&0xf) )]

    def pack_color(self, color):
        '''
        Return color packed ready to send as a two element list [0x0b, 0xgr]
        '''
        r,g,b = color
        return [ chr(b&0xf) , chr(((g&0xf)<<4) | (r&0xf)) ]

    def set_pixel(self, addr, pixel, color):
        '''
        Set one pixel of the matrix at the given address to the given color
        '''
        self.send(addr, ['P'] + self.pack_pixel(pixel) + self.pack_color(color))
        return

    def set_column(self, addr, col, colors):
        '''
        Set the given column of the matrix at the given address to the given color.
        '''
        data = ['C', chr(col)]
        for color in colors:
            data += self.pack_color(color)
        self.send(addr, data)
        return

    def set_row(self, addr, row, colors):
        '''
        Set the given row of the matrix at the given address to the given color.
        '''
        data = ['R', chr(row)]
        for color in colors:
            data += self.pack_color(color)
        self.send(addr, data)
        return
        
    def set_all(self,addr,color = None):
        '''
        Set all LEDs to the given color
        '''
        if color is None:
            data = ['D']
            self.send(addr,data)
            return
        data = ['L'] + self.pack_color(color)
        self.send(addr,data)
        return

    def set_matrix(self,addr,matrix):
        '''
        Set a full matrix of colors.  The matrix is a list of rows,
        each row a list of colors.
        '''
        data = ['M']
        for row in matrix:
            for color in row:
                data += self.pack_color(color)
                continue
            continue
        self.send(addr, data)
        return

    def set_ascii(self,addr,ascii,color,offset=0):
        '''
        Write the given ascii character in the given color at given offset
        '''
        data = ['A', ascii] + self.pack_color(color) + [chr(offset)]
        self.send(addr, data)
        return

        
