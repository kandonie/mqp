#include "ESP32Servo.h"
#include "Arduino.h"

#define FULL_CW 2000
#define FULL_CCW 1000
#define STOPPED 1500

Servo Motor1;
Servo Motor2;
Servo Motor3;
Servo Motor4;

//motor 1 is right side
//motor 2 is left side
//2000 is full reverse 
//1000 if full forwards

//from robot prespective motor 2 is left
//and motor 1 is right

const int motorPin = 13;
const int motor2Pin = 14;
const int motor3Pin = 15;
const int motor4Pin = 19; 

boolean PWMDisabledDrive = false;
boolean PWMDisabledWeapon = false;

//PID variables
double error;
double totalError;
double previousError = 0;

//PID Variables for driveDistance
double error1;
double totalError1;
double previousError1 = 0;
double error2;
double totalError2;
double previousError2 = 0;

double kp = 0;
double ki = 0;
double kd = 0;


void brushlessNeutral(){
    Motor1.writeMicroseconds(1500);
    Motor2.writeMicroseconds(1500);
}

void setPIDGains(double proportional, double integral, double derivative) {
    kp = proportional;
    ki = integral;
    kd = derivative;

    Serial.print("KP Value: ");
    Serial.println(kp);
}


int checkPWM(int pwm){


    //return pwm = pwm > 2000? 2000: pwm < 1000? 1000:pwm;
    if (pwm > 1600) {
    pwm = 1600;
    }
    if (pwm < 1400) {
        pwm = 1400;
    }
    return pwm;
}

void disablePWM(String system){

    if(system.equals("drive")){
        //Motor1.detach();
        //Motor2.detach();
        brushlessNeutral();
        //Motor4.detach();    
        PWMDisabledDrive = true;

    } 
    else if(system.equals("weapon")){
        //Motor3.detach();
        PWMDisabledWeapon = true;

    } 
    else if(system.equals("all")){
        //Motor1.detach();
        //Motor2.detach();
        brushlessNeutral();
        //Motor3.detach();
        //Motor4.detach();
        PWMDisabledDrive = true;
        PWMDisabledWeapon = true;
    } 


}



void enablePWM(String system){
    // Motor1.attach(motorPin, 1000, 2000);   // left motor
    // Motor2.attach(motor2Pin, 1000, 2000);  // right motor
    // Motor3.attach(motor3Pin, 1000, 2000);   // left motor
    // Motor4.attach(motor4Pin, 1000, 2000);  // right motor

    if(system.equals("drive")){
        // Motor1.attach(motorPin, 1000, 2000);   // left motor
        // Motor2.attach(motor2Pin, 1000, 2000);  // right motor
        //Motor4.attach(motor4Pin, 1000, 2000);  // right motor
        //brushlessNeutral();  
        PWMDisabledDrive = false;

    } 
    else if(system.equals("weapon")){
        //Motor3.attach(motor3Pin, 1000, 2000);  // right motor
        PWMDisabledWeapon = false;

    } 
    else if(system.equals("all")){
        // Motor1.attach(motorPin, 1000, 2000);   // left motor
        // Motor2.attach(motor2Pin, 1000, 2000);  // right motor
        //Motor3.attach(motor3Pin, 1000, 2000);   // left motor
        //Motor4.attach(motor4Pin, 1000, 2000);  // right motor
        //brushlessNeutral();
        PWMDisabledDrive = false;
        PWMDisabledWeapon = false;
    } 
}

void movementSetup()
{
    //enablePWM("all");
    Motor1.attach(motorPin, 1000, 2000);   // left motor
    Motor2.attach(motor2Pin, 1000, 2000);  // right motor
    Motor3.attach(motor3Pin, 1000, 2000);   // left motor
    Motor4.attach(motor4Pin, 1000, 2000);

    Motor1.setPeriodHertz(60);
    Motor2.setPeriodHertz(57);
    Motor3.setPeriodHertz(56);
    Motor4.setPeriodHertz(55);
    Motor1.writeMicroseconds(1500);
    Motor2.writeMicroseconds(1500);
    delay(2000);
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
    if (direction == "CCW") {
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



bool turnToAngle(double currentHeading, double desiredHeading) {
    //Serial.println("Turning to angle");
    if (desiredHeading > 360){
        disablePWM("drive");
        Serial.println("Desired Heading Out Of Range");
        return true;
    }
    error = ((int)currentHeading - (int)desiredHeading)%360;
    Serial.print("Current Heading  ");
    Serial.print(currentHeading);
    Serial.print("Desired Heading ");
    Serial.println(desiredHeading);

    if (error > 180){
        error = 360 - error;
    } else if (error < -180){
        error = 360 + error;
    }
    //Serial.print("Error  : ");
    //Serial.print(error);
    //Serial.print("   Heading  : ");
    //Serial.println(currentHeading);
    String direction;

    if(abs(currentHeading - desiredHeading) > 180){
        direction = "CW";
    } else {
        direction = "CCW";
    }

    totalError += error;
    double proportional = error*kp;
    double integral = totalError*ki;
    double derivative = (error - previousError)*kd;

    int output = proportional + integral + derivative;

    // an output of range 0-1000 will be mapped to pwm range 1500-2000
    int speed = map(output, 0, 50, STOPPED, FULL_CW);
    // constrain to pwm range 1000-2000 so negative output values can make motors go backwards
    speed = constrain(speed, FULL_CCW, FULL_CW);

    //check turn angle
    turnSpeed(speed, direction);

    //reset setpoints when target is hit
    previousError = error;

    //arbitrary error for now
    if(abs(error) < 10){
        disablePWM("drive");
        Serial.println("Reached Angle");
        return true;
    }

    return false;

}


bool driveDistance(int encoderTicks, double distGoal){
    if(distGoal > 50){
        Serial.println("Distance goal too large");
        return true;
    }
    // Convert encoder ticks to wheel revolutions
    // 14 motor poles, 52:855 gearbox reduction
    double wheelPos = encoderTicks*14*52/855;
    //Convert goals to wheel revolutions
    double wheelGoal = distGoal/(2.75*3.14);

    // Set error for PID
    error1 = wheelGoal - wheelPos;

    totalError1 += error1;
    double proportional = error1*kp;
    double integral = totalError1*ki;
    double derivative = (error1 - previousError1)*kd;

    int output = proportional + integral + derivative;

    // Map output over full PWM range
    int speed = map(output, -50, 50, FULL_CCW, FULL_CW);
    
    // Set drive speeds
    setRight(speed);
    setLeft(speed);

    previousError1 = error1;
    
    //arbitrary error for now in rotations of wheel
    if(error < .125){
        return true;
    }

    return false;
}


