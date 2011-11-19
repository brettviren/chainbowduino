#!usr/bin/env python 

import serial

class LedMatrix(object):
    '''
    Light up LEDs organized in a 2D matrix.

    Coordinates of LEDs are specified by (column,row) tuples.
    Coordinates start with (0,0) at upper-left.

    Colors are specified with triple of (red, green, blue).  

    The full matrix is composed of a number of sub-matrices, each
    identified by an address number.  

    Addressing the hardware is done through the comm object.
    
    '''
    def __init__(self, comm):
        self.comm = comm
        self.matrices = []
        return

    def add_matrix(self,addr,ul,lr):
        '''
        Add a matrix of given address that extends from upper-left to
        lower-right, inclusive.
        '''
        self.matrices.append((addr,ul,lr))
        return

    def addresses(self):
        '''
        return a list of known addresses
        '''
        ret = []
        for addr, ul, lr in self.matrices:
            ret.append(addr)
            continue
        return ret

    def matrix_address(self,pixel):
        '''
        Return a tuple holding (addr,trans) where addr is the address
        of the matrix that contains the given pixel and trans holds
        the pixel value transformed into the local matrix coordinates.
        Return None if the sub-matrix can not be found.
        '''
        for addr, ul, lr in self.matrices:
            if ul[0] <= pixel[0] <= lr[0] and ul[1] <= pixel[1] <= lr[1]:
                trans = (pixel[0] - ul[0] , pixel[1] - ul[1] )
                return (addr,trans)
            continue
        return None

    def set_pixel(self,pixel,color):
        addr, pixel = self.matrix_address(pixel)
        self.comm.set_pixel(addr,pixel,color)
        return

    def set_ascii(self,ascii,pixel,color):
        '''
        Write an ascii character at pixel with given color
        '''
        addr, pixel = self.matrix_address(pixel)
        self.comm.set_ascii(addr,ascii,color,pixel[0])
        return

    def set_clear(self):
        '''
        Darken the entrie matrix
        '''
        for addr,ul,lr in self.matrices:
            self.comm.set_all(addr)
            continue
        return

    def set_color(self,color):
        '''
        Set entire matrix to given color
        '''
        for addr,ul,lr in self.matrices:
            self.comm.set_all(addr,color)
            continue
        return
