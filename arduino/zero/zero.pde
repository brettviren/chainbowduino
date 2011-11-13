/* set the first byte of EPROM to 1 */
#include <EEPROM.h>
void setup () 
{
    EEPROM.write(0,0);
}

void loop()
{
}
