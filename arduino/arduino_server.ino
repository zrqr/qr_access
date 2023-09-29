/*
  This a simple example of the aREST Library for the ESP32 WiFi chip.
  See the README file for more details.

  Written in 2017 by Marco Schwartz under a GPL license.
  
*/

// Import required libraries
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <uri/UriBraces.h>

// WiFi parameters
const char* ssid = "CenturyLink8017";
const char* password = "844588c97cfb72";

const int SOCIAL_PIN = 13;
const int GARAGE_PIN = 12;
const int KEYPAD_D0_PIN = 1;
const int KEYPAD_D1_PIN = 2;
const int REDLED_PIN = 3;
const int BUZZ_PIN = 4;

// Create an instance of the server
WebServer server(80);

StaticJsonDocument<250> jsonDocument;
char buffer[250];

void setup()
{
  
  // Start Serial
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Print the IP address
  Serial.println(WiFi.localIP());
  pinMode(13, OUTPUT);
  server.on(UriBraces("/open_the_gate/{}"), gateHandler);     
  server.begin(); 
}
void gateHandler(){
    if (server.hasArg("plain") == false) {
  }
  String body = server.arg("plain");
  deserializeJson(jsonDocument, body);

  bool open = jsonDocument["open"];
  String apikey = jsonDocument["apiKey"];
  Serial.println(open);
  Serial.println(apikey);
  Serial.println(body);
  if ((open==true) & (apikey == "pacatatucotianao")) {
    digitalWrite(SOCIAL_PIN, 1);
    delay(1000);
    digitalWrite(SOCIAL_PIN, 0);
  }

  server.send(200, "application/json", "{}");
}

void loop() {
  server.handleClient(); 
}
void ledAPI(){  
  
  String arg = server.pathArg(0);
  
  ledControl(arg);

  jsonDocument.clear();
  jsonDocument["state"] = arg;
  serializeJson(jsonDocument, buffer);
  server.send(200, "application/json", buffer);}

// Custom function accessible by the API
void ledControl(String command ) {

  // Get state from command
  int state = command.toInt();

  digitalWrite(13,state);

}