#include <Servo.h>

Servo servo1; // first servo motor
Servo servo2; // second servo motor

void setup()
{
  servo1.attach(3);
  servo2.attach(9); // attaches the second servo motor to pin 9
  Serial.begin(9600);
}

void loop()
{
  // Read data from Python script
  if (Serial.available() > 0) {
    char data = Serial.read();
    
    // Move servos based on data received from Python script
    if (data == '1') {
      if (servo1.read() != 0 || servo2.read() != 180) { // check if either servo is already moving
        servo1.write(0);
        servo2.write(180);
        delay(1000); // added delay to ensure that the servos complete their 180 degree movement before going back to original position
      }
    }
    else {
      if (servo1.read() != 180 || servo2.read() != 0) { // check if either servo is already moving
        servo1.write(180);
        servo2.write(0);
        delay(1000); // added delay to ensure that the servos complete their 180 degree movement before going back to original position
      }
    }
  }
}
