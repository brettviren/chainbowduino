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
void handle_packet(int nbytes);
void setup ();
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
    byte one = comm.read();
    byte two = comm.read();
    return (one << 8) | two;
}

void handle_packet(int nbytes)
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
        rainbow.lightOneDot(col,row,color,OTHERS_ON);
        break;

    case 'R':                   // Set one row
        // format: 0x0R (row number) 0x0bgr * 8 (8 shorts of colors)
        row = comm.read();
        for (int ind=0; ind<8; ++ind) {
            eight[ind] = get_short();
        }
        rainbow.lightOneLine(row,eight,OTHERS_ON);
        break;

    case 'C':                   // Set one column
        // format: 0x0C (column number) 0x0bgr * 8 (8 shorts of colors)
        col = comm.read();
        for (int ind=0; ind<8; ++ind) {
            eight[ind] = get_short();
        }
        rainbow.lightOneColumn(col,eight,OTHERS_ON);
        break;

    case 'M':                   // Set whole matrix
        // format: 64 shorts of color, row1's 8 columns first, row8's last
        for (int irow = 0; irow < 8; ++irow) {
            for (int icol = 0; icol < 8; ++icol) {
                matrix[irow][icol] = get_short();
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
        break;
    }
}

void setup ()
{
    int addr = EEPROM.read(0);
    comm.init(addr);
    comm.set_handler(handle_packet);

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
