#include "comm.h"
#include <HardwareSerial.h>
#include <Wire.h>


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

#define BAUDRATE 115200

extern HardwareSerial Serial;


Comm::Comm()
    : m_addr(-1)
    , m_handler(0)
{
}

void Comm::init(int addr)
{
    m_addr = addr;

    if (addr) {                 // slave
        Wire.begin(addr);
    }
    else {                      // master
        Wire.begin();
    }

    Serial.begin(BAUDRATE);
}

byte Comm::addr()
{
    return m_addr;
}

// get next byte from serial stream
byte Comm::serial_get(bool block)
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

byte Comm::wire_get(bool block)
{                               // slave
    if (block) {
        while (true) {
            if (Wire.available() > 0) {
                break;
            }
        }
    }

    return Wire.receive();
}

// Drain data from serial up to and including '\0'
void Comm::serial_drain()
{
    while (true) {
        byte val = serial_get();
        if (val == '\0') {
            break;
        }
    }
}

// Drain data from wire up to and including '\0'
void Comm::wire_drain()
{
    while (true) {
        byte val = wire_get();
        if (val == '\0') {
            break;
        }
    }
}

byte Comm::read()
{
    if (m_addr) {               // I'm on I2C
        return wire_get();
    }
    else {                      // I'm on serial
        return serial_get();
    }
}

bool Comm::drain(int nbytes)
{
    while (nbytes) {
        --nbytes;
        byte val = read();
    }
}

bool Comm::transmit(byte addr, byte nbytes)
{                               // master
    Wire.beginTransmission(addr);
    // Wire.send(addr);
    // Wire.send(nbytes);
    while (nbytes) {
        --nbytes;
        byte val = serial_get();
        Wire.send(val);
    }
    Wire.send('\0');
    Wire.endTransmission();
    return true;
}


void Comm::process()
{
    if (m_addr) {               // slave
        process_wire();
    }
    else {                      // master
        process_serial();
    }
}

void Comm::process_wire()
{
    byte val = wire_get();
    if (val != m_addr) {
        wire_drain();
        return;
    }
    byte num = wire_get();
    m_handler(num);
    wire_drain();
}

void Comm::process_serial()
{
    if (! Serial.available()) {
        return;
    }

    byte addr = serial_get();
    byte pkt = serial_get();
    byte num = serial_get();

    bool okay = false;
    if (!addr) {                // handle by master
        if (m_handler) {
            okay = m_handler(num);
            serial_drain();
        }
        else {
            okay = drain(num);
        }
    }
    else {                      // send to slave
        okay = transmit(addr,num);
        serial_drain();
    }

    if (okay) {
        Serial.print("OK");
    }
    else {
        Serial.print("NO");
    }
    Serial.print(pkt);
    Serial.print(addr);
    Serial.print(num);
    Serial.print('\0');
}

void Comm::set_handler(PacketHandler handler)
{
    m_handler = handler;
}


