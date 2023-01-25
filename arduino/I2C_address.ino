/* This I2C scanner supports 7 bit addressing and not 8 bit & 10 bit addressing*/

// I2C uses 7 bits (bit 7 (MSB) to bit1) for addressing and bit 0 (LSB) to configure read or write.

// The address format is 7 bits so the address range is 000 0001 (0x01 / 1) to 111 1111 (0x7F / 127). MSB is 6th bit and LSB is 0th bit.

// The I2C specification has reserved addresses: 000 0000 (0x00 / 0) to 000 0111 (0x07 / 7) and 111 1000 (0x78 / 120) to 111 1111 (0x7F / 127).

// I2C valid address range: 000 1000 (0x08 / 8) to 111 0111 (0x77 / 119).


// Each I2C device has a base address above which 8 address can be configured using 3 solder jumpers this gives room to connect 8 same devices with different addresses to the controller. 

  // Example: TI I2C LCD Adapter-PCF8574: Based address: 0x27 (010 0111) (without soldering jumpers A0 to A2). A0 to A2 are pulled high without soldering.

  // Configurable address: 0x26 to 0x20 (through soldering jumpers A0 to A2). A0 to A2 are pulled low after soldering.

  // Format: 0100A2A1A0

  // Base address varies for NXP make LCD Adapter-PCF8574: 0x3F (011 1111) (without soldering jumpers A0 to A2). A0 to A2 are pulled high without soldering.

  // Configurable address: 0x3F to 0x38 (through soldering jumpers A0 to A2). A0 to A2 are pulled low after soldering.
  
  // Format: 0111A2A1A0

  

// Some vendors incorrectly provide 8-bit addresses which include the read/write bit. One address for writing to the slave device and another to reading from the slave.

  // Example 8 bit address: If the read address is 0x9B (1001 1011) and the write address is 0x9A (1001 1010) then use only the top seven bits (1001 101) and you get an address of 0x4D.

  // If your slave address is outside the valid address range 000 1000 (0x08 / 8) to 111 0111 (0x77 / 119) then probably your vendor has specified an 8-bit address.
  

// Refer Adafruit_i2c-addresses.pdf for address range for adafruit i2c devices.

// Wire library allows you to communicate with I2C (Inter-Integrated Circuit) / TWI (Two-Wire Interface) devices. 

// Wire.endTransmission() returns 0 if success & 4 for error.
  

#include <Wire.h>

void setup() {
 Serial.begin (9600);
 // Leonardo: wait for serial port to connect
 while (!Serial) 
 {
 }
 Serial.println ();
 Serial.println ("I2C scanner. Scanning ...");
 byte count = 0;
 
 Wire.begin();
 for (byte i = 8; i <= 119; i++)     // scans valid address range: 000 1000 (0x08 / 8) to 111 0111 (0x77 / 119).
 {
 Wire.beginTransmission (i);
 if (Wire.endTransmission () == 0)   // Wire.endTransmission() returns 0 if success & 4 for error.
 {
 Serial.print ("Found address: ");
 Serial.print (i, DEC);
 Serial.print (" (0x");
 Serial.print (i, HEX);
 Serial.println (")");
 count++;
 delay (1); // maybe not be needed?
 } // end of good response
 } // end of for loop
 Serial.println ("Done.");
 Serial.print ("Found ");
 Serial.print (count, DEC);
 Serial.println (" device(s).");
} // end of setup
void loop() {}
