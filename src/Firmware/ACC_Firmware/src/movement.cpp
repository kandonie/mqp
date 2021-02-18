#include "ESP32Servo.h"
#include "Arduino.h"

#define FULL_CW 2000
#define FULL_CCW 1000

Servo Motor1;
Servo Motor2;
Servo Motor3;
Servo Motor4;

const int motorPin = 15;
const int motor2Pin = 14;
const int motor3Pin = 13;
const int motor4Pin = 19; //must change from pin 10 // should be 25, temporarily chaning to 34 for testing

boolean PWMDisabledDrive = false;
boolean PWMDisabledWeapon = false;

//PID variables
double error;
double totalError;
double previousError = 0;

double kp = 0;
double ki = 0;
double kd = 0;

void setPIDGains(double proportional, double integral, double derivative) {
    kp = proportional;
    ki = integral;
    kd = derivative;

    Serial.print("KP Value: ");
    Serial.println(kp);
}


int checkPWM(int pwm){

    if (pwm > 2000) {
    pwm = 2000;
    }
    if (pwm < 1000) {
        pwm = 1000;
    }
    return pwm;
}

void disablePWM(String system){

    if(system.equals("drive") && PWMDisabledDrive == false){
        Motor1.detach();
        Motor2.detach();
        Motor4.detach();    
        PWMDisabledDrive = true;

    } 
    else if(system.equals("weapon") && PWMDisabledWeapon == false){
        Motor3.detach();
        PWMDisabledWeapon = true;

    } 
    else if(system.equals("all")){
        Motor1.detach();
        Motor2.detach();
        Motor3.detach();
        Motor4.detach();
        PWMDisabledDrive = true;
        PWMDisabledWeapon = true;
    } 


}

void enablePWM(String system){
    Motor1.attach(motorPin, 1000, 2000);   // left motor
    Motor2.attach(motor2Pin, 1000, 2000);  // right motor
    Motor3.attach(motor3Pin, 1000, 2000);   // left motor
    Motor4.attach(motor4Pin, 1000, 2000);  // right motor

    if(system.equals("drive") && PWMDisabledDrive == true){
        Motor1.attach(motorPin, 1000, 2000);   // left motor
        Motor2.attach(motor2Pin, 1000, 2000);  // right motor
        Motor4.attach(motor4Pin, 1000, 2000);  // right motor  
        PWMDisabledDrive = false;

    } 
    else if(system.equals("weapon") && PWMDisabledWeapon == true){
        Motor3.attach(motor3Pin, 1000, 2000);  // right motor
        PWMDisabledWeapon = false;

    } 
    else if(system.equals("all")){
        Motor1.attach(motorPin, 1000, 2000);   // left motor
        Motor2.attach(motor2Pin, 1000, 2000);  // right motor
        Motor3.attach(motor3Pin, 1000, 2000);   // left motor
        Motor4.attach(motor4Pin, 1000, 2000);  // right motor
        PWMDisabledDrive = false;
        PWMDisabledWeapon = false;
    } 
}

void movementSetup()
{
    enablePWM("all");
    Motor1.setPeriodHertz(60);
    Motor2.setPeriodHertz(55);
    Motor3.setPeriodHertz(57);
    Motor4.setPeriodHertz(58);
}

void setRight(int speed)
{   
    speed = checkPWM(speed);
    Motor1.writeMicroseconds(speed);
}

void setLeft(int speed)
{
    speed = checkPWM(speed);
    Motor2.writeMicroseconds(speed);
}

// set the motor speeds so the robot turns
// @param speed a range from 1000-2000
// @param direction a string that is either "CW" or "CCW"
void turnSpeed(int speed, String direction){
    if (direction == "CW") {
        setLeft(speed);
        setRight(FULL_CW - abs(speed - FULL_CCW));
    } else {
        setLeft(FULL_CW - abs(speed - FULL_CCW));
        setRight(speed);
    }
}

void setWeapon(int speed){
    speed = checkPWM(speed);
    Motor3.writeMicroseconds(speed);
}

boolean PWMDriveDisabled(){
    return PWMDisabledDrive;
}

boolean PWMWeaponDisabled() {
    return PWMDisabledWeapon;
}



bool turnToAngle(double currentHeading, double desiredHeading){
    error = currentHeading - desiredHeading;
    String direction;
    //previousError 

    if(abs(currentHeading - desiredHeading) > 180){
        direction = "clockwise";
    } else {
        direction = "counterclockWise";
    }

    totalError += error;
    double proportional = error*kp;
    double integral = totalError*ki;
    double derivative = (error - previousError)*kd;

    int output = proportional + integral + derivative;


    //check turn angle
    turnSpeed(output, direction);

    //mapping from 1000,2000

    //reset setpoints when target is hit 
    
    //take values in msec


    previousError = error;

    //arbitrary error for now
    if(error < 100){
        return true;
    }

    return false;

}


void testPWM(){
    Motor1.writeMicroseconds(1000);
    Motor2.writeMicroseconds(1000);
    Motor3.writeMicroseconds(1000);
    Motor4.writeMicroseconds(1000);
    delay(2000);
    Motor1.writeMicroseconds(1500);
    Motor2.writeMicroseconds(1500);
    Motor3.writeMicroseconds(1500);
    Motor4.writeMicroseconds(1500);
    delay(2000);
    Motor1.writeMicroseconds(2000);
    Motor2.writeMicroseconds(2000);
    Motor3.writeMicroseconds(2000);
    Motor4.writeMicroseconds(2000);
    delay(2000);

}




