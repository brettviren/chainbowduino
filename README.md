= Chainbowduino =

This project provides firmware and host software for driving multiple
[Rainbowduino](http://www.seeedstudio.com/depot/rainbowduino-led-driver-platform-atmega-328-p-371.html)
(RBD) boards chained together.

== Addressing ==

Each RBD board has an address.  Address 0 is the master, the rest are
slaves.  A small, unique firmware is initially flashed to each board.
In the setup() function the 0th byte of EEPROM is written with the
uniqe address.  After this, the full, identical firmware is flashed to
each board.

== Communication ==

Communication between the host computer and the master board is via
UART.  Communication between the master board and any slaves it
through I2C.  Besides driving its own LEDs the master acts as a
UART/I2C converter.  Communication proceeds through several states:

1. A command is written to UART by the host

2. The master reads the command and either:

 * executes it if it is addressed to the master, or

 * forwards it to I2C, and the addressed slave board executes it

3. The master writes a response to UART

4. the host reads the response.

5. The system is idle until it is repeated.

=== Protocol ===

The communication protocol (implemented on the host side by comm.py
and on the RBD side by comm.cpp) consists of command and response
packets terminated with a 0 byte.  Details of the protocol may change
from what is documented below.  The source is always definitive.

The command packet consists of a header and a command character and a
command-specific payload.

* address of board

* a packet number (1-255, rolls over)

* length of command character and any command-specific payload data

* command character

* command-specific payload bytes

* terminating zero byte

To see what commands exist check the chainbowduino.pde file.

The response packet consists of a:

* A two byte status "OK" or "NO"

* The packet number being responded to

* an optional string of non-zero bytes (useful for debugging)

* terminating zero byte


= Hardware =

My initial hardware consists of:

* 3 [Rainbowduino](http://www.seeedstudio.com/depot/rainbowduino-led-driver-platform-atmega-328-p-371.html) boards

* 3 [8x RGB LED common-anode matrices](http://www.seeedstudio.com/depot/60mm-square-88-led-matrix-super-bright-rgb-p-113.html)

* 1 [UartSBee v4](http://www.seeedstudio.com/depot/uartsbee-v4-p-688.html)

* 1 solderless bread board and some jumpers

* mini-usb cable

* laptop running Debian

Yes, seeedstudio got lots of my money.....


Some notes on hardware:

* Make sure to get common-anode LED matrices, common-cathodes exist too and won't work.

* Take note some important differences between the [discontinued](http://www.seeedstudio.com/wiki/UartSBee) [UartSBee v3](http://www.seeedstudio.com/wiki/UartSBee_V3.1) and the current [V4](http://www.seeedstudio.com/wiki/UartSBee_V4).  The v3 boards will [plug right in](http://www.seeedstudio.com/wiki/Rainbowduino_LED_driver_platform_-_Atmega_328#Use_UartSB_to_Upload_firmware) to the header connector on the RBD board, however V4 changes the pin out to make this no longer work.  If you don't notice this you will get errors when trying to upload a sketch.  

== Connecting ==

The RBDs chain end to end.  The I2C connection is made automatically
by mating the pins to the socket.  You need to supply some connection
for forwarding the power.  I used some segments of solid copper core
cut from a TV cable.

Chaining like this hides the reset buttons which in practice is no big
loss.  More importantly it hides the slave's UART connections.  This
is a big problem if you need to reprogram the slaves.  to solve this I
ran some jumper wires from the UART sockets, out under the LED box and
into a breadboard.  There they are lined up so I can move the UartSB
from board to board.  These jumpers also take care of the pin out
mismatch mentioned above.

