#include <Arduino.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "iostream"
#include "string.h"
#include "movement.h"

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
  delay(1000);
  Serial.println("I am Alive");

  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open

  //Uncomment to host esp access point
  /*
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  */


  // Uncomment to connect to wifi
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
   {
     delay(1000);
     Serial.println("Connecting to WiFi..");
   }
   Serial.println(WiFi.localIP());
   

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
    

      char json[] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";  
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
      Serial.println(newJson);

      DeserializationError error = deserializeJson(doc, newJson);

        // Test if parsing succeeds.
      if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
      }

      motor1PWM = doc["motor1pwm"];
      Serial.print("JSON TEST Print  ");
      Serial.println(motor1PWM);


      Serial.println();
      Serial.println("About to send request");
 
      request->send(200);
      Serial.println("Response Sent");
      test = 1;
      //startTime = millis();
  });

  //start the webserver
  server.begin();

  //motion setup
  //if not connected to wifi nothing should move
  movementSetup();

  //going from 1000-2000
  //has to have been 6 seconds 
  //100us above and below 1500
  //send 1000 for a sec then send

  // to exit the calibration routine
  // must be within 100us of 1500
  // check that it is really outputting 1500us on the pwm channel 
  // no power cycle after calibration 

  //this is the jitter
  setRight(1500);
  setLeft(1500);
  delay(10);

  Serial.println("End Of Calibration");
  delay(1000);

}

void loop() {
 
  setRight(motor1PWM);
  setLeft(motor2PWM);
  
}
