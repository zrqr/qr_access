/*
  This a simple example of the aREST Library for the ESP32 WiFi chip.
  See the README file for more details.

  Written in 2017 by Marco Schwartz under a GPL license.
  
*/

// Import required libraries
#include <Wiegand.h>
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <uri/UriBraces.h>

// WiFi parameters
const char* ssid = "CenturyLink8017";
const char* password = "844588c97cfb72";

const int SOCIAL_PIN = 6;
const int GARAGE_PIN = 12;
const int KEYPAD_D0_PIN = 2;
const int KEYPAD_D1_PIN = 3;
const int REDLED_PIN = 4;
const int BUZZ_PIN = 5;
volatile bool check = false;

// Create an instance of the server
WebServer server(80);
WiFiClient client;
IPAddress ipn(192,168,0,17); 
Wiegand wiegand;

StaticJsonDocument<250> jsonDocument;
volatile char currpass[10];


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
  pinMode(SOCIAL_PIN, OUTPUT);
  server.on(UriBraces("/open_the_gate/{}"), gateHandler);     
  server.begin(); 
  currpass[0] = '\0';

  //Install listeners and initialize Wiegand reader
  wiegand.onReceive(receivedData, "Card readed: ");
  wiegand.begin(Wiegand::LENGTH_ANY, true);

  //initialize pins as INPUT and attaches interruptions
  pinMode(KEYPAD_D0_PIN, INPUT);
  pinMode(KEYPAD_D1_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(KEYPAD_D0_PIN), pinStateChanged, CHANGE);
  attachInterrupt(digitalPinToInterrupt(KEYPAD_D1_PIN), pinStateChanged, CHANGE);

  //Sends the initial pin state to the Wiegand library
  pinStateChanged();
}

void loop() {

  noInterrupts();
  wiegand.flush();
  interrupts();
  callAPI();
  server.handleClient(); 
}

// When any of the pins have changed, update the state of the wiegand library
void pinStateChanged() {
  wiegand.setPin0State(digitalRead(KEYPAD_D0_PIN));
  wiegand.setPin1State(digitalRead(KEYPAD_D1_PIN));
}

void callAPI(){
    bool check_state;
    check_state = check;
    if (check_state==true) {
      const uint16_t port = 8000;
      const char * host = "192.168.0.17"; // ip or dns

      // WRITE --------------------------------------------------------------------------------------------
      
      if (!client.connect(host, port)) {
          Serial.println("Connection failed.");
          Serial.println("Waiting 5 seconds before retrying...");
          return;
      }
      noInterrupts();
      char frozenChar[10];  // Make sure bufferSize is large enough to hold the data
      for (int i = 0; i < 10; i++) {
        frozenChar[i] = currpass[i];
      }
      char footer[100] = " HTTP/1.1\r\nHost: 192.168.0.17\r\n" ;
      char request[1000]; // Make sure the buffer is large enough
      strcpy(request, "GET /check_password/");
      strcat(request, frozenChar);
      strcat(request, footer);
      
      for (int i = 0; i < 10; i++) {
        currpass[i] = '\0';
      }
      check=false;
      interrupts();
      client.print(request);
      readResponse();
    }
  
}

void receivedData(uint8_t* data, uint8_t bits, const char* message) {
    //Print value in HEX
    noInterrupts();
    char nonVolatileBuffer[10];

    uint8_t bytes = (bits+7)/8;
    for (int i=0; i<bytes; i++) {
        for (int i = 0; i < 10; i++) {
          nonVolatileBuffer[i] = currpass[i];
        }
        uint8_t result = data[i] & 0xF;
        char hexChar;

        if (result < 10) {
          hexChar = '0' + result; // Convert to ASCII character '0' to '9'
        } else {
          hexChar = 'A' + (result - 10); // Convert to ASCII character 'A' to 'F'
        }
        currpass[strlen(nonVolatileBuffer)] = hexChar;
        for (int i = 0; i < 10; i++) {
          nonVolatileBuffer[i] = currpass[i];
        }
        Serial.println(nonVolatileBuffer);

        if (strlen(nonVolatileBuffer)>=6) {
            
            check = true;
            
        }

    }
    interrupts();
}

void readResponse(){
  
   if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();

    // do nothing forevermore:
    for(;;)
      ;
  }
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
    delay(500);
    digitalWrite(SOCIAL_PIN, 0);
  }

  server.send(200, "application/json", "{}");
  delay(3000);
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

  digitalWrite(SOCIAL_PIN,state);

}