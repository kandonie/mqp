#include "ESP32Servo.h"
#include "constants.h"
#include "Arduino.h"

#define FULL_RV 2000
#define FULL_FW 1000
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

//encoder PID values
double kpl = 4;
double kil = .1;
double kdl = 0;

//TEMP PLEASE REMOVE
int print_count = 0;
bool drivingForwards = true;


void brushlessNeutral(){
    Motor1.writeMicroseconds(STOPPED);
    Motor2.writeMicroseconds(STOPPED);
}

void setPIDGains(double proportional, double integral, double derivative) {
    //kp = proportional;
    // ki = integral;
    // kd = derivative;
    //tempory change to set the encoder pid values
    kpl = proportional;
    kil = integral;
    kdl = derivative;

}

void setDirection(bool isForwards) {
    drivingForwards = isForwards;
}

bool getDirection(){
    return drivingForwards;
}

int checkPWM(int pwm){
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
        brushlessNeutral();
        PWMDisabledDrive = true;
    } 
    else if(system.equals("weapon")){
        PWMDisabledWeapon = true;
    } 
    else if(system.equals("all")){
        brushlessNeutral();
        PWMDisabledDrive = true;
        PWMDisabledWeapon = true;
    } 


}


//ESTOP is a non recoverable function,the robot must be power cycled after an ESTOP 
void estopRobot(){

    brushlessNeutral();
    delay(100);
    //disable pwm on motor ports
    Motor1.detach();
    Motor2.detach();
    Motor3.detach();
    Motor4.detach();

    Serial.println("Robot is ESTOPPED, Power Off Robot");
    delay(500);

}


//old code, just used for keeping track of robot enabled states
void enablePWM(String system){

    if(system.equals("drive")){ 
        PWMDisabledDrive = false;
    } 
    else if(system.equals("weapon")){
        PWMDisabledWeapon = false;
    } 
    else if(system.equals("all")){
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
    if(speed > STOPPED)
    {
        setDirection(false);    
    } else {
        setDirection(true);
    }

    speed = checkPWM(speed);
    Motor1.writeMicroseconds(speed);
}

void setLeft(int speed)
{

    if(speed > STOPPED)
    {
        setDirection(false);    
    } else {
        setDirection(true);
    }
    
    speed = checkPWM(speed);
    Motor2.writeMicroseconds(speed);
}

// set the motor speeds so the robot turns
// @param speed a range from 1000-2000
// @param direction a string that is either "CW" or "CCW"
void turnSpeed(int speed, String direction){
    if (direction == "CCW") {
        setLeft(speed);
        setRight(FULL_RV - abs(speed - FULL_FW));
    } else {
        setLeft(FULL_RV - abs(speed - FULL_FW));
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
    // Serial.print("Current Heading  ");
    // Serial.print(currentHeading);
    // Serial.print("Desired Heading ");
    // Serial.println(desiredHeading);

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
    int speed = map(output, 0, 50, STOPPED, FULL_RV);
    // constrain to pwm range 1000-2000 so negative output values can make motors go backwards
    speed = constrain(speed, FULL_FW, FULL_RV);

    //check turn angle
    turnSpeed(speed, direction);

    //reset setpoints when target is hit
    previousError = error;

    //arbitrary error for now
    if(abs(error) < 10){
        disablePWM("drive");
        //Serial.println("Reached Angle");
        return true;
    }

    return false;

}


bool driveDistance(int encoderTicks, double distGoal){
    int n_th_print = 20;
    if(print_count % n_th_print == 0){
        Serial.print("encoderTicks ");
        Serial.print(encoderTicks);
    }
    

    if(distGoal > 50){
        Serial.println("Distance goal too large");
        return true;
    }
    // Convert encoder ticks to wheel revolutions
    // 14 motor poles, 52:855 gearbox reduction
    double wheelPos = (float)encoderTicks*52.0/(855.0*14.0);
    //Convert goals to wheel revolutions
    double wheelGoal = distGoal/(2.75*3.14);
    Serial.print("\twheelGoal ");
    Serial.print(wheelGoal);
    // Set error for PID
    // goal - pos noninverted goes in reverse forever
    error1 = wheelGoal - wheelPos;
    if(print_count % n_th_print == 0){
        Serial.print("\terror: ");
        Serial.print(error1);
    }

    totalError1 += error1;
    double proportional = error1*kpl;
    double integral = totalError1*kil;
    double derivative = (error1 - previousError1)*kdl;

    double output = proportional + integral + derivative;
    //Serial.print("output: ");
    //Serial.println(output);

    // Map output over full PWM range
    int speed = map(output, -50, 50, FULL_RV, FULL_FW);
    //speed = constrain(speed, FULL_FW, FULL_RV);
    if(print_count % n_th_print == 0){
        Serial.print("\tSpeed: ");
        Serial.println(speed);
    }

    // Set drive speeds
    setRight(speed);
    setLeft(speed);

    previousError1 = error1;
    
    //arbitrary error for now in rotations of wheel
    if(abs(error1) < .25){
        Serial.println("Robot has reached desired distance");
        disablePWM("drive");
        totalError1 = 0;
        previousError = 0;
        error1 = 0;
        return true;
    }

    return false;
}


