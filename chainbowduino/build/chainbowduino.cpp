#include <WProgram.h>

int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

void loop ();
void setup ();
void handle_i2c(int num);
#line 1 "build/chainbowduino.pde"
/* -*- c++ -*-

   This is firmware for rainbowduinos that are chained together.

*/

#include "comm.h"
#include "Rainbow.h"
#include <Wire.h>
#include <EEPROM.h>


Comm comm = Comm();
Rainbow rainbow = Rainbow();

// color is packed into a 2byte short: 0x0bgr
unsigned short get_short()
{
    byte b1 = comm.read();
    byte b2 = comm.read();
    return (b1 << 8) | b2;
}

// read and unpack three bytes assuming [0xrg, 0xbR, 0xGB] 
// and repack them into two shorts like [0x0bgr, 0x0BGR]
void get_two(unsigned short *two)
{
    byte b1 = comm.read();
    byte b2 = comm.read();
    byte b3 = comm.read();
    
    byte r = 0xf&(b1 >> 4);
    byte g = 0xf&(b1);
    byte b = 0xf&(b2 >> 4);
    byte R = 0xf&(b2);
    byte G = 0xf&(b3 >> 4);
    byte B = 0xf&(b3);

    two[0] = (b<<8) | (g<<4) | r;
    two[1] = (B<<8) | (G<<4) | R;
}

void get_eight(unsigned short *eight)
{
    for (int count = 0; count < 8; ++count) {
        eight[count] = 0;
    }
    for (int count = 0; count < 4; ++count) {
        get_two(eight+count*2);
    }
}



bool handle_packet(int nbytes)
{
    unsigned char cmd = comm.read();
    
    unsigned short color;
    unsigned short eight[8];
    unsigned short matrix[8][8];

    unsigned char row, col, pixel, ascii;

    switch (cmd) {

    case 'S':                   // Draw serial number
        rainbow.closeAll();
        ascii = (unsigned char)(comm.addr() + '0');
        rainbow.dispChar(ascii, WHITE, 0);
        break;

    case 'D':                   // Darken (clear) all LEDs
        rainbow.closeAll();
        break;

    case 'L':                    // Light all LEDs given color
        color = get_short();
        rainbow.lightAll(color);
        break;

    case 'P':                   // set one pixel to a color
        // format: 0xCR (4 bits for column and 4 bits for row)
        pixel = comm.read();
        col = pixel >> 4;
        row = pixel & 0x0F;

        // format: 0x0bgr
        color = get_short();
        rainbow.lightOneDot(row,col,color,OTHERS_ON);
        break;

    case 'R':                   // Set one row
        // format: 0x0R (row number) 0xrg 0xbR 0xGB * 4
        row = comm.read();
        get_eight(eight);
        rainbow.lightOneLine(row,eight,OTHERS_ON);
        break;

    case 'C':                   // Set one column
        // format: 0x0C (column number) 0x0bgr * 8 (8 shorts of colors)
        col = comm.read();
        get_eight(eight);
        rainbow.lightOneColumn(col,eight,OTHERS_ON);
        break;

    case 'M':                   // Set whole matrix
        // format: 64 shorts of color, row1's 8 columns first, row8's last
        for (int irow = 0; irow < 8; ++irow) {
            get_eight(eight);
            for (int icol = 0; icol < 8; ++icol) {
                matrix[irow][icol] = eight[icol];
            }
        }
        rainbow.lightAll(matrix);
        break;

    case 'A':                   // Set an ASCII letter
        // format: Letter(byte), color(short), offest(byte)
        ascii = comm.read();
        color = get_short();
        col = comm.read();
        rainbow.dispChar(ascii, color, col);
        break;

    default:
        return false;
        break;
    }
    return true;
}

void handle_i2c(int num)
{
    // byte addr = comm.read();
    // byte count = comm.read();

    unsigned char ascii = 0;

    /*
    rainbow.lightAll(WHITE);
    rainbow.closeAll();

    ascii = (unsigned char)(count + '0');
    rainbow.dispChar(ascii, WHITE, 0);
    delay(500);

    rainbow.lightAll(WHITE);
    rainbow.closeAll();
    ascii = (unsigned char)(addr + '0');
    rainbow.dispChar(ascii, WHITE, 0);
    delay(500);
    */

    /*
    if (addr != comm.addr() || count != num) {
        comm.wire_drain();
        return;
    }
    */

    handle_packet(num);

    /*
    delay(500);
    rainbow.lightAll(WHITE);
    rainbow.closeAll();
    ascii = (unsigned char)(addr + '0');
    rainbow.dispChar(ascii, WHITE, 0);
    */
}

void setup ()
{
    int addr = EEPROM.read(0);
    comm.init(addr);
    comm.set_handler(handle_packet);
    Wire.onReceive(handle_i2c);

    rainbow.init();
    rainbow.lightAll(WHITE);
    rainbow.closeAll();

    unsigned char ascii = (unsigned char)(comm.addr() + '0');
    rainbow.dispChar(ascii, WHITE, 0);
    
}

void loop ()
{
    comm.process();
}

//= //Timer1 interuption service routine=========================================
ISR(TIMER1_OVF_vect)         
{
    //sweep 8 lines to make led matrix looks stable
    static unsigned char line=0,level=0;

    flash_line(line,level);

    line++;
    if (line>7) {
        line=0;
        level++;
        if(level>15) {
            level=0;
        }
    }  
 
}
