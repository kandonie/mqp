#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

int currentSensor1Pin = 33;
int currentSensor2Pin = 24;
double Sensor1Current = 0;
double Sensor2Current = 0;

double maximumVoltage = 3.3;
double ADCMax = 4095;
double conversionFactor = .0264; //26.4 mV/a from datasheet

double* gyroData = new double[3];

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

void sensorSetup()
{
    pinMode(currentSensor1Pin, INPUT);
    pinMode(currentSensor2Pin, INPUT);

    if (!bno.begin())
    {
        Serial.print("No BNO055 detected");
        while (1);
    }
    Serial.println("Connected To BNo055");
}

double calculateVoltage(int adcReading)
{
    return (adcReading * maximumVoltage) / 4095;
}

// this should probably run not in current check, in a timed loop
void measureCurrent()
{

    //analogRead
    double adcReading1 = analogRead(currentSensor1Pin);
    //delay(10);
    double adcReading2 = analogRead(currentSensor2Pin);
    //delay(10);

    //Divide voltage by conversion factor to calculate currrent reading
    Sensor1Current = calculateVoltage(adcReading1) / conversionFactor;
    Sensor2Current = calculateVoltage(adcReading2) / conversionFactor;
    //Sensor1Current = adcReading1;
    //Sensor2Current = adcReading2;
    //currentSensor2Pin = adcReading2;
}

double currentCheck(String sensor)
{
    //measureCurrent(); //this needs to run in a timed loop, not when this function is called
    if (sensor.equals("sensor1"))
    {
        return Sensor1Current;
    }
    else if (sensor.equals("sensor2"))
    {
        return Sensor2Current;
    }
    return 999999;
}

void updateGyroData()
{
    sensors_event_t orientationData , linearAccelData, gravityData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    //bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
    gyroData[0] = orientationData.orientation.x; //left to right used for turning
    gyroData[1] = orientationData.orientation.y; //up and down tilt from fw to rear
    gyroData[2] = orientationData.orientation.z; //seems pretty reliable for seeing if the robot is flipped over
}

double getGyroData()
{
    //this needs to 
    return gyroData[0];
}

bool isUpsideDown()
{
    if ( gyroData[2] > 50 || gyroData[2] < -50){
        Serial.println("Robot is flipped over");
        return true;
    }
    return false;
}
