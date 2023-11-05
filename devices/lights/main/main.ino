#include <WiFi.h>
#include <ArduinoOTA.h>
#include "secrets.h"
#include "OTAHandler.h"
#include "LEDHandler.h"
#include "PubSubHandler.h"
#include "Globals.h"


#define LED_PIN 2 // Define the pin for the LED. Change this to your actual LED pin

bool lightsOn = true;

void setup() {
  // DO NOT MODIFY OR REMOVE REMOTELY
  setupOTA(SSID, PASSWORD);  // DO NOT MODIFY OR REMOVE REMOTELY
  // DO NOT MODIFY OR REMOVE REMOTELY


  pinMode(LED_PIN, OUTPUT); // Initialize the LED pin as output

  setupFastLED(); // Initialize FastLED

  setupPubSub(); // Initialize PubSub

}

void loop() {
  // DO NOT MODIFY OR REMOVE REMOTELY
  handleOTA();  // DO NOT MODIFY OR REMOVE REMOTELY
  // DO NOT MODIFY OR REMOVE REMOTELY

  handlePubSub(); // Maintain PubSub connection and handle incoming messages

    // If the lights should be on, run the 'pride' function to update their color
  if (lightsOn) {
    pride(); 
    FastLED.show();
  } else {
    FastLED.clear();
    FastLED.show();
  }

}