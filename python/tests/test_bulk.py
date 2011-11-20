#!/usr/bin/env python
'''
Test sending bulk data.
'''

from rainbowduino import matrices, comm
from random import randint
import time
import math

commObj = comm.SerialComm()
leds = matrices.LedMatrix(commObj)

# 8 rows by 24 columns
# 8,0 --> 15,7
for addr in range(3):
    leds.add_matrix(addr,(0+addr*8,0),(7+addr*8,7))

# 83 fps to master, 17 fps to master + 3 slaves
# +1 fps after upping TWI_FREQ
def fill_matrix(func):
    for addr in range(3):
        matrix = []
        for irow in range(8):
            row = []
            for icol in range(8):
                row.append(func(addr,irow,icol))
                continue
            matrix.append(row)
            #print row
            continue

        commObj.set_matrix(addr,matrix)
        continue
# 41 fps to master, 9 fps to master+3 slaves
def fill_by_rows(func):
    for addr in range(3):
        for irow in range(8):
            row = []
            for icol in range(8):
                row.append(func(addr,irow,icol))
                continue
            #print addr,irow,row
            commObj.set_row(addr,irow,row)
            continue
        continue
    return

def fill_by_cols(func):
    for addr in range(1):
        for icol in range(8):
            col = []
            for irow in range(8):
                col.append(func(addr,irow,icol))
                continue
            commObj.set_column(addr,icol,col)
            continue
        continue
    return

def fill_rand(addr,irow,icol):
    return (randint(0,15),randint(0,15),randint(0,15))

def fill_rb(addr,irow,icol):
    return (2*irow+1,2*icol+1,0)

def fill_by_col(addr,irow,icol):
    rc = irow*2 + 1
    cc = icol*2 + 1

    if irow > icol:
        return (rc,0,icol+1)
    if icol > irow:
        return (0,cc,irow+1)

    return (cc,cc,cc)


start = time.time()
count = 0;
while True:
    fill_matrix(fill_rand)
    #fill_by_rows(fill_rand)
    count += 1
    if count > 100 and count % 100 == 1:
        fps = float(count)/(time.time() - start)
        print 'fps: %f' % fps
    if count > 1001:
        break
    continue
    
#fill_by_cols(fill_by_col)
#time.sleep(0.5)
#fill_by_rows(fill_by_col)


