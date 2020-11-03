
#include "ESP32Servo.h"
#include "Arduino.h"


Servo DriveMotor1;
Servo DriveMotor2;
Servo WeaponMotor;

const int motor2pin = 19;
const int motorPin = 18;

void movementSetup()
{
    DriveMotor1.attach(motorPin, 1000, 2000);   // left motor
    DriveMotor2.attach(motor2pin, 1000, 2000);  // right motor
    DriveMotor1.setPeriodHertz(330);
    DriveMotor2.setPeriodHertz(330);

    DriveMotor1.write(90);
    DriveMotor2.write(90);

}

void setRight(int speed)
{
    if (speed > 255) {
    speed = 255;
    }
    if (speed < 90) {
        speed = 90;
    }
    DriveMotor1.write(speed);
}

void setLeft(int speed)
{
    if (speed > 255) {
    speed = 255;
    }
    if (speed < 90) {
        speed = 90;
    }
    DriveMotor2.write(speed);
}




