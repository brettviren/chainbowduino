#!/usr/bin/env python

import time
from rainbowduino import comm
talk = comm.SerialComm()

for addr in range(3):
    talk.set_all(addr)
    time.sleep(0.5)
    talk.set_all(addr,(15,15,15))
    time.sleep(0.5)
    talk.set_all(addr)
    time.sleep(0.5)
    talk.set_show_addr(addr)
    time.sleep(0.5)
    print
    continue


