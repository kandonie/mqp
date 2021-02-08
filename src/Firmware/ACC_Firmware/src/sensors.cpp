#include <Arduino.h>

int currentSensor1Pin = 33;
int currentSensor2Pin = 24;
double Sensor1Current = 0;
double Sensor2Current = 0;

double maximumVoltage = 3.3;
double ADCMax = 4095;
double conversionFactor = .0264; //26.4 mV/a from datasheet

void sensorSetup(){
    pinMode(currentSensor1Pin, INPUT);
    pinMode(currentSensor2Pin, INPUT);
    //pinMode(16, OUTPUT);
    //digitalWrite(16, LOW);

}

double calculateVoltage(int adcReading){
    return (adcReading*maximumVoltage)/4095;
}

// this should probably run not in current check, in a timed loop
void measureCurrent(){

    //analogRead
    double adcReading1 = analogRead(currentSensor1Pin);
    delay(10);
    double adcReading2 = analogRead(currentSensor2Pin);
    delay(10);

    //Divide voltage by conversion factor to calculate currrent reading
    Sensor1Current = calculateVoltage(adcReading1)/conversionFactor;
    Sensor2Current = calculateVoltage(adcReading2)/conversionFactor;
    //Sensor1Current = adcReading1;
    //Sensor2Current = adcReading2;
    //currentSensor2Pin = adcReading2;
}

double currentCheck(String sensor){
    //measureCurrent(); //this needs to run in a timed loop, not when this function is called
    if(sensor.equals("sensor1")){
        return Sensor1Current;
    } else if(sensor.equals("sensor2")){
        return Sensor2Current;
    }
    return 999999;
}








