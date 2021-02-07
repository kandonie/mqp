#include "ESP32Servo.h"
#include "Arduino.h"

Servo Motor1;
Servo Motor2;
Servo Motor3;
Servo Motor4;

const int motorPin = 15;
const int motor2Pin = 14;
const int motor3Pin = 13;
const int motor4Pin = 25; //must change from pin 10

boolean PWMDisabledDrive = false;
boolean PWMDisabledWeapon = false;

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




