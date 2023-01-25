/*
This sketch controls a 28BYJ-48 stepper motor via a shift register. 

For details on usage, wiring, etc. see link below.
http://projectsfromtech.blogspot.com/2014/03/arduino-shift-register-stepper-motor.html

Last Edited: 3/1/2014 
by Matthew https://projectsfromtech.blogspot.com

Thanks to DrLuke from http://bildr.org/2011/02/74hc595/
for Shift Register Control code
*/

int SER_Pin = 8;   //pin 14 on the 75HC595
int RCLK_Pin = 9;  //pin 12 on the 75HC595
int SRCLK_Pin = 10; //pin 11 on the 75HC595

//How many of the shift registers - change this
#define number_of_74hc595s 1 

//do not touch
#define numOfRegisterPins number_of_74hc595s * 8

boolean registers[numOfRegisterPins];



           


//set all register pins to LOW
void clearRegisters(){
  for(int i = numOfRegisterPins - 1; i >=  0; i--){
     registers[i] = LOW;
  }
} 


//Set and display registers
//Only call AFTER all values are set how you would like (slow otherwise)
void writeRegisters(){

  digitalWrite(RCLK_Pin, LOW);

  for(int i = numOfRegisterPins - 1; i >=  0; i--){
    digitalWrite(SRCLK_Pin, LOW);

    int val = registers[i];

    digitalWrite(SER_Pin, val);
    digitalWrite(SRCLK_Pin, HIGH);

  }
  digitalWrite(RCLK_Pin, HIGH);

}

//set an individual pin HIGH or LOW
void setRegisterPin(int index, int value){
  registers[index] = value;
}

////////////////////////////////////////////////////////////////////
//declare variables for the motor pins
int motorPin1 = 0;	// Blue   - 28BYJ48 pin 1
int motorPin2 = 1;	// Pink   - 28BYJ48 pin 2
int motorPin3 = 2;	// Yellow - 28BYJ48 pin 3
int motorPin4 = 3;	// Orange - 28BYJ48 pin 4
                        // Red    - 28BYJ48 pin 5 (VCC)

int motorSpeed = 0;     //variable to set stepper speed
const int potPin = 2; 	//potentiometer connected to A2
int potValue = 0; 	//variable to read A0 input


//////////////////////////////////////////////////////////////////////////////
void setup() {

  Serial.begin(9600);
  
  pinMode(SER_Pin, OUTPUT);
  pinMode(RCLK_Pin, OUTPUT);
  pinMode(SRCLK_Pin, OUTPUT);


  //reset all register pins
  clearRegisters();
  writeRegisters();
  
  
}

//////////////////////////////////////////////////////////////////////////////
void loop(){

  potValue = analogRead(potPin);     // read the value of the potentiometer
  Serial.println(potValue);          // View full range from 0 - 1024 in Serial Monitor
  if (potValue < 535){               // if potentiometer reads 0 to 535 do this
    motorSpeed = (potValue/15 + 5);  //scale potValue to be useful for motor
    clockwise();                     //go to the ccw rotation function
  }
  else {                             //value of the potentiometer is 512 - 1024
    motorSpeed = ((1024-potValue)/15 + 5); //scale potValue for motor speed
    counterclockwise(); //go the the cw rotation function
  }
  

}

//////////////////////////////////////////////////////////////////////////////
//set pins to ULN2003 high in sequence from 1 to 4
//delay "motorSpeed" between each pin setting (to determine speed)

void counterclockwise (){
  // 1
  setRegisterPin(motorPin1, HIGH);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin4, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 2
  setRegisterPin(motorPin1, HIGH);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin4, LOW);
  writeRegisters(); 
  delay (motorSpeed);
  // 3
  setRegisterPin(motorPin1, LOW);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin4, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 4
  setRegisterPin(motorPin1, LOW);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin4, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 5
  setRegisterPin(motorPin1, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin4, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 6
  setRegisterPin(motorPin1, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin4, HIGH);
  writeRegisters(); 
  delay (motorSpeed);
  // 7
  setRegisterPin(motorPin1, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin4, HIGH);
  writeRegisters(); 
  delay(motorSpeed);
  // 8
  setRegisterPin(motorPin1, HIGH);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin4, HIGH);
  writeRegisters(); 
  delay(motorSpeed);
}

//////////////////////////////////////////////////////////////////////////////
//set pins to ULN2003 high in sequence from 4 to 1
//delay "motorSpeed" between each pin setting (to determine speed)

void clockwise(){
  // 1
  setRegisterPin(motorPin4, HIGH);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin1, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 2
  setRegisterPin(motorPin4, HIGH);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin1, LOW);
  writeRegisters(); 
  delay (motorSpeed);
  // 3
  setRegisterPin(motorPin4, LOW);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin1, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 4
  setRegisterPin(motorPin4, LOW);
  setRegisterPin(motorPin3, HIGH);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin1, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 5
  setRegisterPin(motorPin4, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin1, LOW);
  writeRegisters(); 
  delay(motorSpeed);
  // 6
  setRegisterPin(motorPin4, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin2, HIGH);
  setRegisterPin(motorPin1, HIGH);
  writeRegisters(); 
  delay (motorSpeed);
  // 7
  setRegisterPin(motorPin4, LOW);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin1, HIGH);
  writeRegisters(); 
  delay(motorSpeed);
  // 8
  setRegisterPin(motorPin4, HIGH);
  setRegisterPin(motorPin3, LOW);
  setRegisterPin(motorPin2, LOW);
  setRegisterPin(motorPin1, HIGH);
  writeRegisters(); 
  delay(motorSpeed);
}
