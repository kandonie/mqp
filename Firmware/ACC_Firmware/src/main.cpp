#include <Arduino.h>
#include "WiFi.h"
#include "ESPAsyncWebServer.h"

const char* ssid = "MQP-Access-Point";
const char* password = "test12345678";
// Create AsyncWebServer object on port 80
AsyncWebServer server(80);


String readAPOS() {
  //This should check a global variable with the last heading reading
  return "North";
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);
  Serial.println("I am Alive");

  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  //Get Requests
  server.on("/readAPOS", HTTP_GET, [](AsyncWebServerRequest *request){  //Angular Position Get From Robot
    request->send_P(200, "text/plain", readAPOS().c_str());
  });

  server.begin();


}

void loop() {
  // put your main code here, to run repeatedly:



}