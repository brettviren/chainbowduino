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
    def __init__(self, device = '/dev/ttyUSB0', baudrate = 115200):
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
        #print len(data)
        data_length = len(data)
        assert 4 + data_length <= 128, "Data must be limited to 124 bytes."
        tosend = [chr(addr), chr(self.count), chr(data_length)] + data + [chr(0)]
        #print 'Send to 0x%x packet:%d len:%d cmd:"%s"' % (addr,self.count,data_length,data[0])
        #print ['0x%x' % ord(x) for x in data[1:]]
        for char in tosend:
            self.ser.write(char)
            continue

        reply = self.ser.read(5)
        if len(reply) != 5:
            print 'Packet %d FAILED: got only %d bytes' % (self.count, len(reply))
            return

        okno = reply[:2]
        pkt = ord(reply[2])
        addr = ord(reply[3])
        nbytes = ord(reply[4])
        if okno == 'NO' or pkt != self.count:
            print 'Packet %d FAILED: got %s%d (%d,%d)' % (self.count, okno, pkt, addr, nbytes)
        else:
            #print 'Packet %d %s%d (%d,%d)' % (self.count, okno, pkt, addr, nbytes)
            pass
        rest = []
        while True:
            char = self.ser.read(1)
            num = ord(char)
            if not num:
                break
            rest.append(num)
            continue
        if rest:
            #print rest
            pass

        #time.sleep(0.001)         # give the human a chance to see something, neh?
        return

    def pack_pixel(self, pixel):
        '''
        Return pixel packed ready to send as a single character list
        '''
        return [chr( ((pixel[0]&0xf) << 4) | (pixel[1]&0xf) )]

    def pack_color(self, color):
        '''
        Return single color packed ready to send as a two element list [0x0b, 0xgr]
        '''
        r,g,b = color
        return [ chr(b&0xf) , chr(((g&0xf)<<4) | (r&0xf)) ]

    def pack_colors(self, colors):
        '''
        Return a succession of colors packed ready to send.  This
        packs two colors into three bytes. Note the RGB order is
        preserved and not bgr.

        [(r,g,b),(R,G,B)]-> [0xrg, 0xbR, 0xGB]

        An odd number of colors results in the last nibble to be zero:

        [(r,g,b)]-> [0xrg, 0xb0]
        '''
        ret = []
        colors = list(colors)   # make a copy
        odd = len(colors) % 2
        if odd: colors.append((0,0,0))

        while len(colors):
            r,g,b = colors.pop(0)
            R,G,B = colors.pop(0)
            ret.append(chr( ((0xf&r) << 4) | (0xf&g) ) )
            ret.append(chr( ((0xf&b) << 4) | (0xf&R) ) )
            ret.append(chr( ((0xf&G) << 4) | (0xf&B) ) )
            continue
        if odd:
            ret.pop()
        return ret

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
        data += self.pack_colors(colors)
        self.send(addr, data)
        return

    def set_row(self, addr, row, colors):
        '''
        Set the given row of the matrix at the given address to the given color.
        '''
        data = ['R', chr(row)]
        data += self.pack_colors(colors)
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
            data += self.pack_colors(row)
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

    def set_show_addr(self,addr):
        '''
        Tell the matrix to display its address
        '''
        data = ['S']
        self.send(addr,data)
        return

