#include <Arduino.h>
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "iostream"
#include "string.h"
#include "movement.h"

const char *ssid = "SPWEB2.4";
const char *password = "teaparty520";
// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

char general[] = "/general";
char ESTOP[] = "/ESTOP";
char APOS[] = "/readAPOS";

//mutex - varible names
int motor1PWM = 0;
int motor2PWM = 0;
int weaponPWM = 0;
double desiredHeading = 0;
double currHeading = 0;

double weaponCurrent;
double driveCurrent;
int test = 0;
int startTime = 0;


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
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // WiFi.begin(ssid, password);
  // while (WiFi.status() != WL_CONNECTED)
  // {
  //   delay(1000);
  //   Serial.println("Connecting to WiFi..");
  // }
  // Serial.println(WiFi.localIP());

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
      
      
      for (size_t i = 0; i < len; i++) {
        Serial.write(data[i]);
      }
 
      Serial.println();
      Serial.println("About to send request");
 
      request->send(200);
      Serial.println("Response Sent");
      test = 1;
      startTime = millis();
  });

  //start the webserver
  server.begin();

  //motion setup
  //if not connected to wifi nothing should move
  movementSetup();

}

void loop() {
  if (test) {
    for (int i = 90; i < 180; i++) {
      setRight(i);
      setLeft(i);
      delay(10);
    }
    for (int i = 180; i > 0; i--) {
      setRight(i);
      setLeft(i);
      delay(10);
    }
    for (int i = 0; i < 180; i++) {
      setRight(i);
      setLeft(i);
      delay(10);
    }
    for (int i = 180; i > 0; i--) {
      setRight(i);
      setLeft(i);
      delay(10);
    }
    for (int i = 0; i < 90; i++) {
      setRight(i);
      setLeft(i);
      delay(10);
    }
    test = 0;
  }
  
}