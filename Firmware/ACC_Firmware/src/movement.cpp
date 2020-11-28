
#include "ESP32Servo.h"
#include "Arduino.h"


Servo DriveMotor1;
Servo DriveMotor2;
Servo WeaponMotor;

const int motor2pin = 14;
const int motorPin = 15;

void movementSetup()
{
    DriveMotor1.attach(motorPin, 1000, 2000);   // left motor
    DriveMotor2.attach(motor2pin, 1000, 2000);  // right motor
    DriveMotor1.setPeriodHertz(50);
    DriveMotor2.setPeriodHertz(55);
    //DriveMotor1.write(90);
    //DriveMotor2.write(90);

}

void setRight(int speed)
{   
    /*
    if (speed > 2000) {
    speed = 2000;
    }
    if (speed < 1000) {
        speed = 1000;
    }
    */
    
    DriveMotor1.writeMicroseconds(speed);
}

void setLeft(int speed)
{
    /*
    if (speed > 2000) {
    speed = 2000;
    }
    if (speed < 1000) {
        speed = 1000;
    }
    */
    
    DriveMotor2.writeMicroseconds(speed);
}




