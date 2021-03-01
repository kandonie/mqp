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

double desiredHeading = 90;
double currHeading = 0;

double weaponCurrent;
double driveCurrent;
int startTime = 0;

//Interrupt Booleans
boolean checkGyro;
boolean checkCurrent;

//JSON Library declarations
StaticJsonDocument<300> doc;

// BNo055 Sensor Varibles (todo break into separate c++ files)
double xPos = 0, yPos = 0, headingVel = 0;
uint16_t BNO055_SAMPLERATE_DELAY_MS = 10; //how often to read data from the board
uint16_t PRINT_DELAY_MS = 500;            // how often to print the data
uint16_t printCount = 0;                  //counter to avoid printing every 10MS sample

//velocity = accel*dt (dt in seconds)
//position = 0.5*accel*dt^2
double ACCEL_VEL_TRANSITION = (double)(BNO055_SAMPLERATE_DELAY_MS) / 1000.0;
double ACCEL_POS_TRANSITION = 0.5 * ACCEL_VEL_TRANSITION * ACCEL_VEL_TRANSITION;
double DEG_2_RAD = 0.01745329251; //trig functions require radians, BNO055 outputs degrees
unsigned long SensorPrevTime = 0; //prevtime is the previous time that the bno055 was polled
unsigned long mainTime;

//state machine testing
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
  Serial.println("Read current heading");
  char currHeading_str[10];
  sprintf(currHeading_str, "%f", currHeading);
  return currHeading_str;
}

String generalHandler()
{

  return "0";
}

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
  server.on(general, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
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
        //desiredHeading = doc["desiredHeading"];
        robotMovementType = doc["RobotMovementType"].as<const char *>();
        auto weaponTest = doc["WeaponArmedState"].as<const char *>(); //adding this greatly increased RTT, but should be double checked
        auto driveTest = doc["ArmDriveState"].as<const char *>();
        bool tuning_kp = doc["tuning_kp"];
        bool tuning_ki = doc["tuning_ki"];
        bool tuning_kd = doc["tuning_kd"];

        //Serial.print("kp is ");
        //Serial.print(kp);
        //Serial.print("  ki is ");
        //Serial.print(ki);
        //Serial.print("  kd is ");
        //Serial.println(kd);

        driveArmed = doc["ArmDriveState"];
        //Serial.print("JSON TEST Print  ");
        //Serial.println(motor1PWM);

        // set pid gains based on json input


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


        static double kp = 0.01;
        static double ki = 0.05;
        static double kd = 0.01;

        if (tuning_kp) {
          driveArmed = false;
          weaponArmed = false;
          kp = doc["kp"];
        }
        else if (tuning_ki) {
          driveArmed = false;
          weaponArmed = false;
          ki = doc["ki"];
        }
        else if (tuning_kd) {
          driveArmed = false;
          weaponArmed = false;
          kd = doc["kd"];
        }
        setPIDGains(kp, ki, kd);

        if (robotMovementType.equals("gyroMode"))
        {
          state = autonomous;
        } else if (robotMovementType.equals("rcMode")); {
          //state = teleop;
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
        Serial.println(getGyroData());
        Serial.println("At expected angle");
        setLeft(1500);
        setRight(1500);
        //robotMovementType = "teleop";
        //state = teleop;
      }
      else
      {
        robotMovementType = "gyroMode";
      }
    }

    //drive a set distance
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
