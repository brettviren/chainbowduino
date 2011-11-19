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
    typedef void (*PacketHandler)(int nbytes);

    // Set handler for when a packet is available
    void set_handler(PacketHandler handler);

    // Read next byte, expected to be called from handler to get payload
    byte read();

    // Drain nbytes from the stream
    bool drain(int nbytes);     // default handler

    // return the address
    byte addr();

private:
    int m_addr;

    PacketHandler m_handler;
    bool transmit(int addr, int nbytes);
};

#endif  // COMM_H
