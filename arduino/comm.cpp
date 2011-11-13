#include "comm.h"
#include <HardwareSerial.h>

/*
 * Communication protocol:
 *
 * Packet: [address][count][payload of count bytes][\0]
 * Payload: [command][command specific options]
 */

#define BAUDRATE 9600

extern HardwareSerial Serial;


Comm::Comm()
    : m_addr(-1)
    , m_handler(0)
    , m_gotSerial(false)
{
}

void Comm::init(int addr)
{
    m_addr = addr;

    m_master.begin();
    m_slave.begin(addr);

    Serial.begin(BAUDRATE);
}

// get next byte from serial stream
byte serial_get(bool block = true);
byte serial_get(bool block)
{
    if (block) {
        while (true) {
            if (Serial.available() > 0) {
                break;
            }
        }
    }

    return Serial.read();
}

void serial_drain()
{
    while (true) {
        byte val = serial_get();
        if (val == '\0') {
            break;
        }
    }
}

byte Comm::read()
{
    if (m_gotSerial) {
        return serial_get();
    }
    else {
        return m_slave.receive();
    }
}

bool Comm::drain(int nbytes)
{
    Serial.print("Draining ");
    Serial.print(nbytes);
    Serial.println(" bytes.");

    while (nbytes) {
        --nbytes;
        byte val = read();
        //Serial.print((int)val);
    }
}

void Comm::transmit(int addr, int nbytes)
{
    Serial.print("transmitting ");
    Serial.print(nbytes);
    Serial.print(" to address ");
    Serial.print(addr);
    Serial.println(".");

    m_master.beginTransmission(addr);
    while (nbytes) {
        --nbytes;
        byte val = serial_get();
        m_master.send(val);
    }
    m_master.endTransmission();
}


void Comm::process()
{
    if (! Serial.available()) {
        return;
    }

    byte addr = serial_get();
    byte num = serial_get();

    Serial.print("Got packet for address ");
    Serial.print((int)addr);        
    Serial.print(" with nbytes=");
    Serial.print((int)num);        
    Serial.println(".");

    if (addr == m_addr) {
        if (m_handler) {
            m_gotSerial = true;
            m_handler(num);
            serial_drain();
            m_gotSerial = false;
        }
        else {
            drain(num);
        }
    }
    else {
        transmit(addr,num);
    }
}

void Comm::set_handler(PacketHandler handler)
{
    m_handler = handler;
}


