#!/usr/bin/env python

from rainbowduino import matrices, comm

commObj = comm.TestComm()
leds = matrices.LedMatrix(commObj)

for count in range(3):
    leds.add_matrix(count, (1+count*8,1),(8+count*8,8))
    continue

test_pixels = [
    [0, (2,2), (2,2)],
    [1, (10,2), (2,2)],
    [2, (18,2), (2,2)],
]

for addr_out, pixel_in, pixel_out in test_pixels:
    addr,pixel = leds.matrix_address(pixel_in)
    assert addr == addr_out
    assert pixel == pixel_out

    leds.set_pixel(pixel_in, (1,2,3))
    continue


