#include <Arduino.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "iostream"
#include "string.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include "movement.h"
#include "sensors.h"

using namespace std;

const char *ssid = "#wewantseason";
const char *password = "ap1@Lancast";
// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

char general[] = "/general";
char ESTOP[] = "/ESTOP";
char APOS[] = "/readAPOS";
char robotDataJson[] = "/getRobotData";

//mutex - varible names
int motor1PWM = 1500;
int motor2PWM = 1500;
int weaponPWM = 0;
boolean weaponArmed = false;
boolean driveArmed = false;
// double kp = 0;
// double ki = 0;
// double kd = 0;


String robotMovementType;

//Robot State variable triggers
boolean robotDisabled = true;

double desiredHeading = 180;
double currHeading = 0;

double weaponCurrent;
double driveCurrent;
int startTime = 0;

// Encoder setup
volatile int encoder1Ticks = 0;
volatile int encoder2Ticks = 0;
double desiredDist = 0;
const byte encoder1Pin = 25;
const byte encoder2Pin = 26;
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;

//Interrupt Booleans
boolean checkGyro;
boolean checkCurrent;

//JSON Library declarations
StaticJsonDocument<300> doc;
StaticJsonDocument<200> robotDataDoc;


unsigned long SensorPrevTime = 0; //prevtime is the previous time that the bno055 was polled
unsigned long mainTime;

//Robot States
static enum stateChoices {
  disabled,
  teleop,
  autonomous,
  configureRobot,
  updateSensors
} state,
    previousState;

String readAPOS()
{
  //This should check a global variable with the last heading reading
  Serial.println("Read APOS");
  return "North";
}

String readCurrHeading()
{
  //This should check a global variable with the last heading reading
  // char currHeading_str[10];
  // int heading = (int) currHeading;
  // sprintf(currHeading_str, "%d", heading);
  // Serial.print("Read current heading: ");
  // Serial.println(currHeading_str);
  // return currHeading_str;
  robotDataDoc["getHeading"] = (int) currHeading;
  robotDataDoc["getDriveCurrent"] = 0.25;
  robotDataDoc["getWeaponCurrent"] = 0.5;
  // robotDataDoc["getOrientation"] = 0;
  // robotDataDoc["getSignalStrength"] = 0;

  char buffer[200];
  serializeJson(robotDataDoc, buffer);
  return buffer;
}

String generalHandler()
{

  return "0";
}


// Encoder ISRs
void IRAM_ATTR encoder1ISR() {
  // Check motor direction then increment/decrement accordingly
  portENTER_CRITICAL_ISR(&mux);
  if(motor1PWM>1500){
    encoder1Ticks++;
  } else{
    encoder1Ticks--;
  }
  portEXIT_CRITICAL_ISR(&mux);
}

void IRAM_ATTR encoder2ISR() {
  // Check motor direction then increment/decrement accordingly
  portENTER_CRITICAL_ISR(&mux);
  if(motor2PWM>1500){
    encoder2Ticks++;
  } else{
    encoder2Ticks--;
  }
  portEXIT_CRITICAL_ISR(&mux);

}

void encoderSetup(){
      //encoder pin interrupt configuration
    pinMode(encoder1Pin, INPUT);
    pinMode(encoder2Pin, INPUT);
    attachInterrupt(digitalPinToInterrupt(encoder1Pin), encoder1ISR, RISING);
    attachInterrupt(digitalPinToInterrupt(encoder2Pin), encoder2ISR, RISING);
}

//testing 

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(2000);
  Serial.println("I am Alive");

  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open

  //Uncomment to host esp access point

  
  // WiFi.softAP(ssid, password);
  // IPAddress IP = WiFi.softAPIP();
  // Serial.print("AP IP address: ");
  // Serial.println(IP);
  
  // Uncomment to connect to wifi

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println(WiFi.localIP());

  //Get Requests (Test Request)
  //todo change APOS get request to robot data json
  //todo serilize to a json
  server.on(APOS, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

  //ESTOP Request
  server.on(ESTOP, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

  // gyro data Request
  server.on(robotDataJson, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readCurrHeading().c_str());
  });

  server.on(
      "/generaltest",
      HTTP_POST,
      [](AsyncWebServerRequest *request) {},
      NULL,
      [](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total) {
        char json[] = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
        // TODO actual memory safety
        int jsonIndex = 0;
        for (size_t i = 0; i < len; i++)
        {

          //Serial.write(data[i]);
          if (data[i] == ' ')
          {
            continue;
          }
          else
          {
            json[jsonIndex] = data[i];
            jsonIndex++;
          }
        }
        Serial.println("");
        char newJson[jsonIndex + 1];
        strncpy(newJson, json, jsonIndex);
        newJson[jsonIndex] = '\0';
        // Serial.println(newJson); //print the whole json

        DeserializationError error = deserializeJson(doc, newJson);

        // Test if parsing succeeds.

        //TODO Return 404 error
        if (error)
        {
          Serial.print(F("deserializeJson() failed: "));
          Serial.println(error.f_str());
          return;
        }

        //TODO MAKE THE ROBOT NOT CRASH HERE IF IT DOESN'T FIND THE KEY
        // deserializeJSON comes from the ESPHTTPTopics.py
        motor1PWM = doc["motor1pwm"];
        motor2PWM = doc["motor2pwm"];
        weaponPWM = doc["weapon_pwm"];
        desiredHeading = doc["desiredHeading"];
        robotMovementType = doc["RobotMovementType"].as<const char *>();
        auto weaponTest = doc["WeaponArmedState"].as<const char *>(); //adding this greatly increased RTT, but should be double checked
        auto driveTest = doc["ArmDriveState"].as<const char *>();
        bool tuning_kp = doc["tuning_kp"];
        bool tuning_ki = doc["tuning_ki"];
        bool tuning_kd = doc["tuning_kd"];

        static double kp = .2;
        static double ki = 0;
        static double kd = 0;

        if (tuning_kp) {
          kp = doc["kp"];
        }
        else if (tuning_ki) {
          ki = doc["ki"];
        }
        else if (tuning_kd) {
          kd = doc["kd"];
        }

        Serial.print("kp is ");
        Serial.print(kp);
        Serial.print("  ki is ");
        Serial.print(ki);
        Serial.print("  kd is ");
        Serial.println(kd);

        driveArmed = doc["ArmDriveState"];
        //Serial.print("JSON TEST Print  ");
        //Serial.println(motor1PWM);

        // set pid gains based on json input
        setPIDGains(kp, ki, kd);

        // ARM and Disarm checks
        if (strcmp(weaponTest, "false") == 0)
        {
          weaponArmed = false;
        }
        else
        {
          weaponArmed = true;
        }

        if (strcmp(driveTest, "false") == 0)
        {
          driveArmed = false;
        }
        else
        {
          driveArmed = true;
        }

        if (robotMovementType.equals("gyroMode"))
        {
          state = autonomous;
        }

        request->send(200);
        Serial.println("Response Sent");
        mainTime = millis();
      });

  //start the webserver
  server.begin();

  //motion setup
  //if not connected to wifi nothing should move
  movementSetup();
  sensorSetup();

  state = teleop;

  Serial.println("End Of Calibration");
  delay(1000);

  mainTime = millis();
}

void updateTime()
{
  //this should probably watch for overflow on mainTime
  mainTime = millis();
}

void loop()
{

  switch ((state))
  {
  case disabled:
    Serial.println("State Disabled");
    /* code */
    disablePWM("all");
    if (robotDisabled)
    {
      state = disabled;
    }
    else
    {
      state = configureRobot;
    }
    break;

  case updateSensors:

    updateTime();

    //the minimum value for this is 10 milliseconds, the BNo055 will not provide data faster over i2c
    if (mainTime - SensorPrevTime > 15)
    {
      measureCurrent();
      weaponCurrent = currentCheck("sensor1");
      driveCurrent = currentCheck("sensor2");
      updateGyroData();
      currHeading = getGyroData();
      //isUpsideDown();
      //Serial.println(getGyroData());
      SensorPrevTime = mainTime;
      //Serial.println("Reading GYRO");
    }

    state = previousState;
    previousState = updateSensors;

    break;

  case teleop:

    //movement functions need to be aware of arm and disarm states
    //Serial.println("Teleop");
    updateTime();
    //Serial.println("In Teleop");
    if (weaponArmed)
    {
      if (PWMWeaponDisabled())
      {
        enablePWM("weapon");
      }
      //Serial.println(currentCheck("sensor1"));
      setWeapon(weaponPWM);
    }
    else
    {
      disablePWM("weapon");
    }

    if (driveArmed)
    {
      if (PWMDriveDisabled())
      {
        enablePWM("drive");
      }
      setRight(motor1PWM);
      setLeft(motor2PWM);
    }
    else
    {
      disablePWM("drive");
    }

    previousState = state;
    state = updateSensors;
    //state = teleop;

    /* code */
    // leave teleop if the state is changed by the control system
    // change variable with json

    break;

  case autonomous:
    updateTime();

    //turn to a defined angle
    if (robotMovementType.equals("gyroMode"))
    {
      if (turnToAngle(currHeading, desiredHeading))
      { //turnToAngle returns true when the robot is at the correct heading
        disablePWM("drive");
        robotMovementType = "gyroMode";
      }
      else
      {
        robotMovementType = "gyroMode";
      }
    }

    if(robotMovementType.equals("waiting")){
      disablePWM("drive");
    }

       //drive a set distance
    // Need actual JSON word
    if (robotMovementType.equals("driveDistance")){
      if (driveDistance(encoder1Ticks, desiredDist)){
        robotMovementType = "waiting";
      }
      else
      {
        robotMovementType = "driveDistance";
      }
    }


    //drive a set distance

    //Serial.println("State Autonomous");

    previousState = state;
    state = updateSensors;

    break;

  case configureRobot:
    disablePWM("all");
    Serial.println("State configure robot");

    break;

  default:
    break;
  }

}
