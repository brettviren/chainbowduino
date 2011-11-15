#include "comm.h"
#include <HardwareSerial.h>

/*
 * Communication protocol:
 *
 * Send to me:
 *
 * Packet: [address][return][count][payload of count bytes][\0]
 * Payload: [command][command specific options]
 *
 * If okay, I send to you:
 *
 * OK[return]
 *
 * If not, I send to you
 *
 * NO[return]
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
    while (nbytes) {
        --nbytes;
        byte val = read();
    }
}

bool Comm::transmit(int addr, int nbytes)
{
    m_master.beginTransmission(addr);
    while (nbytes) {
        --nbytes;
        byte val = serial_get();
        m_master.send(val);
    }
    m_master.endTransmission();
    return true;
}


void Comm::process()
{
    if (! Serial.available()) {
        return;
    }

    byte addr = serial_get();
    byte ret = serial_get();
    byte num = serial_get();

    bool okay = false;
    if (addr == m_addr) {
        if (m_handler) {
            m_gotSerial = true;
            okay = m_handler(num);
            serial_drain();
            m_gotSerial = false;
        }
        else {
            okay = drain(num);
        }
    }
    else {
        okay = transmit(addr,num);
    }

    if (okay) {
        Serial.print("OK");
    }
    else {
        Serial.print("NO");
    }
    Serial.print(ret);

}

void Comm::set_handler(PacketHandler handler)
{
    m_handler = handler;
}


