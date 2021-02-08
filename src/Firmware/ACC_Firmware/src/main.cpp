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

//
String robotMovementType;

//Robot State variable triggers
boolean robotDisabled = true;


double desiredHeading = 0;
double currHeading = 0;

double weaponCurrent;
double driveCurrent;
int test = 0;
int startTime = 0;


//Interrupt Booleans
boolean checkGyro;
boolean checkCurrent;


//JSON Library declarations
StaticJsonDocument<200> doc;


// BNo055 Sensor Varibles (todo break into separate c++ files)
double xPos = 0, yPos = 0, headingVel = 0;
uint16_t BNO055_SAMPLERATE_DELAY_MS = 10; //how often to read data from the board
uint16_t PRINT_DELAY_MS = 500; // how often to print the data
uint16_t printCount = 0; //counter to avoid printing every 10MS sample

//velocity = accel*dt (dt in seconds)
//position = 0.5*accel*dt^2
double ACCEL_VEL_TRANSITION =  (double)(BNO055_SAMPLERATE_DELAY_MS) / 1000.0;
double ACCEL_POS_TRANSITION = 0.5 * ACCEL_VEL_TRANSITION * ACCEL_VEL_TRANSITION;
double DEG_2_RAD = 0.01745329251; //trig functions require radians, BNO055 outputs degrees
unsigned long SensorPrevTime = 0; //prevtime is the previous time that the bno055 was polled
unsigned long mainTime;

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

//state machine testing
static enum stateChoices {
  disabled,
  teleop,
  autonomous,
  configureRobot,
  updateSensors
} state, previousState;







String readAPOS()
{
  //This should check a global variable with the last heading reading
  Serial.println("Read APOS");
  return "North";
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
  
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  


  // Uncomment to connect to wifi
 
  // WiFi.begin(ssid, password);
  // while (WiFi.status() != WL_CONNECTED)
  //  {
  //    delay(1000);
  //    Serial.println("Connecting to WiFi..");
  //  }
  //  Serial.println(WiFi.localIP());
   

  //Get Requests (Test Request)
  server.on(APOS, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

  //ESTOP Request
  server.on(ESTOP, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

  //ESTOP Request
  server.on(general, HTTP_GET, [](AsyncWebServerRequest *request) { //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

    server.on(
    "/generaltest",
    HTTP_POST,
    [](AsyncWebServerRequest * request){},
    NULL,
    [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {
    

      char json[] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";  
      // TODO actual memory safety 
      int jsonIndex = 0;
      for (size_t i = 0; i < len; i++) {
        
        //Serial.write(data[i]);
        if(data[i] == ' '){
          continue;
        } else {
          json[jsonIndex] = data[i];
          jsonIndex++;
        }        
        
      }
      Serial.println("");
      char newJson[jsonIndex+1];
      strncpy(newJson, json, jsonIndex); 
      newJson[jsonIndex] = '\0';
      //Serial.println(newJson); //print the whole json

      DeserializationError error = deserializeJson(doc, newJson);

        // Test if parsing succeeds.

      //TODO Return 404 error
      if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
      }



      //TODO MAKE THE ROBOT NOT CRASH HERE IF IT DOESN'T FIND THE KEY
      // deserializeJSON comes from the ESPHTTPTopics.py
      motor1PWM = doc["motor1pwm"];
      motor2PWM = doc["motor2pwm"];
      weaponPWM = doc["weapon_pwm"];
      robotMovementType = doc["RobotMovementType"].as<const char*>();
      auto weaponTest = doc["WeaponArmedState"].as<const char*>();  //adding this greatly increased RTT, but should be double checked
      auto driveTest = doc["ArmDriveState"].as<const char*>();

      driveArmed = doc["ArmDriveState"];
      //Serial.print("JSON TEST Print  ");
      //Serial.println(motor1PWM);


      //this might also be fucking the RTT
      if(strcmp(weaponTest, "false")== 0){
        weaponArmed = false;
      } else {
        weaponArmed = true;
      }

      if(strcmp(driveTest, "false")== 0){
        driveArmed = false;
      } else {
        driveArmed = true;
      }

      //Serial.print("Weapon Armed Status-  ");
      //Serial.println(weaponArmed);
      //Serial.print("Drive Armed Status-  ");
      //Serial.println(driveArmed);

      //these prints are probably slowing down the RTT
      Serial.println();
      Serial.println("About to send request");

      

      request->send(200);
      Serial.println("Response Sent");
      test = 1;
      mainTime = millis();
  });

  //start the webserver
  server.begin();

  //motion setup
  //if not connected to wifi nothing should move
  movementSetup();
  sensorSetup();

  //going from 1000-2000
  //has to have been 6 seconds 
  //100us above and below 1500
  //send 1000 for a sec then send

  // to exit the calibration routine
  // must be within 100us of 1500
  // check that it is really outputting 1500us on the pwm channel 
  // no power cycle after calibration 

  /*
  //  BNo055 Sensor Setup
    if (!bno.begin())
  {
    Serial.print("No BNO055 detected");
    while (1);
  }
  */
 //set starting state
  state = teleop;

  Serial.println("End Of Calibration");
  delay(1000);

  mainTime = millis();


}

void updateTime(){
  //this should probably watch for overflow on mainTime
  mainTime = millis();

}


void loop() {
  /*
  if(prevTime-mainTime > 200){
    //lauren cares about stuff in getjsonvars
    sensors_event_t orientationData , linearAccelData, gravityData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    //Serial.println(orientationData.orientation.x);
    currHeading = orientationData.orientation.x;
    
  }
  */


  switch ( (state))
  {
  case disabled:
    Serial.println("State Disabled");
    /* code */
    disablePWM("all");
    if(robotDisabled){
      state = disabled;
    } else {
      state = configureRobot;
      
    }
    break;

  case updateSensors:

      updateTime();

      //check if it is time to poll the sensors again
      if ((mainTime - SensorPrevTime >100))
      {
        //Serial.println("Sensors Updated");
        measureCurrent();
      }

      SensorPrevTime = mainTime;
      state = previousState;
      previousState = updateSensors;

      



    break;


  case teleop:

    //movement functions need to be aware of arm and disarm states
    //Serial.println("Teleop");
    updateTime();
    //Serial.println("In Teleop");
    if(weaponArmed){
      if(PWMWeaponDisabled()){
        enablePWM("weapon");
      }
      Serial.println(currentCheck("sensor1"));
      setWeapon(weaponPWM);
    } else{
      disablePWM("weapon");
    }
    

    if(driveArmed){
      if(PWMDriveDisabled()){
        enablePWM("drive");
      }
      setRight(motor1PWM);
      setLeft(motor2PWM);
    } else {
      disablePWM("drive");
    }
    

    previousState = state;
    state = updateSensors;

    
    /* code */
    // leave teleop if the state is changed by the control system
    // change variable with json
    

    break;

  case autonomous:
    //wait for movment goals, then execute them
    updateTime();
    Serial.println("State Autonomous");

    break;


  case configureRobot:
    disablePWM("all");
    Serial.println("State configure robot");
    
    //disable motors
    //ability to adjust pwm limits
    //change PWM and motor connections
    //leaves this state on a the main json or a separate save changes json passing into the robot
    //maybe save changes to eeprom

    break;
  
  default:
    break;
  }
}
