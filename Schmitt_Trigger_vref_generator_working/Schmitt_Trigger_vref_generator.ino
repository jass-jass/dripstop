#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;

// set this value to 9,8,7,6 or 5 to adjust the resolution

#define DAC_RESOLUTION (9)


bool state= true;
float myArray[200];
  int i;
  float maxVal;
  float minVal;
  int sensorValue;
  float voltage;

  const int strobe = 7;

  bool strobeState;

void setup(void) {
  
 //Serial.begin(9600);
 
  pinMode(strobe,INPUT);
  

  // For Adafruit MCP4725A1 the address is 0x62 (default) or 0x63 (ADDR pin tied to VCC)
  // For MCP4725A0 the address is 0x60 (ADDR pin tied to GND) or 0x61
  // For MCP4725A2 the address is 0x64 or 0x65

 
  dac.begin(0x60); // address is 0x60 since ADDR pin is tied to GND
    
 
}

void loop(void) {

  // MCP4275 operating voltage 2.6V to 5.5V
  // Resolution = 12 bit, Ex: 5V/4095 = 1.2mv/step
  // 4095 value may change (reduced) if the arduino voltage output is above 5V

  // while using comapartor, the ouput changes when the offset voltage between in pin and ref pin is 0.08 V
  // Ex: 2.48V set as input then output toggles at dac value 2.40 & 2.56
  
   if(state== true)
  {
  for (i=0;i<200;i++)
  {
    sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
   voltage = sensorValue * (5.06 / 1023.0);
  // print out the value you read:
     myArray[i] = voltage;
   //Serial.println(myArray[i]);
    delay(10);
    
  }

 
  

  
    maxVal = myArray[0];
    minVal = myArray[0];

   

   for ( i = 0; i < 200; i++) {
      maxVal = max(myArray[i],maxVal);
      minVal = min(myArray[i],minVal);

   }

  // Serial.println(maxVal);
 // Serial.println(minVal);

  


// updating DAC
  
    
    
   dac.setVoltage((((maxVal+minVal)/2)*4095)/5, false);

   state= false;

   delay(10);
     
  }
  strobeState = digitalRead(strobe);
   
    



 if(strobeState == HIGH){
dac.setVoltage(((maxVal-0.2)*4095)/5, false);
    
   }

 if(strobeState == LOW){
dac.setVoltage(((minVal+0.25)*4095)/5, false);
    
   }
   


   
}
