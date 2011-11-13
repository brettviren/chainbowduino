#include <Wire.h>

/*
 * Packet communications through serial and I2C.
 *
 * Any packets from serial that a different address is forwarded to
 * I2C
 *
 * Packet structure is:
 * 
 * 'P'          - the packet marker
 * address      - the address that the packet is for
 * count        - the number of bytes in the payload
 * [payload]    - count number of bytes
 *
 */

#ifndef COMM_H
#define COMM_H

typedef unsigned char byte;

class Comm
{
public:
    // Create a communications
    Comm();

    // call in setup()
    void init(int addr);

    // call in loop()
    void process();

    // Prototype for a packet handler function.  Return true if handled
    typedef bool (*PacketHandler)(int nbytes);

    // Set handler for when a packet is available
    void set_handler(PacketHandler handler);

    // Read next byte, expected to be called from handler to get payload
    byte read();

    // Drain nbytes from the stream
    bool drain(int nbytes);     // default handler

private:
    int m_addr;
    bool m_gotSerial;

    PacketHandler m_handler;
    void transmit(int addr, int nbytes);

    TwoWire m_master, m_slave;
};

#endif  // COMM_H
