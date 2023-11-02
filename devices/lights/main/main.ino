#include <WiFi.h>
#include <ArduinoOTA.h>
#include "secrets.h"
#include "OTAHandler.h"
#include "LEDHandler.h"


#define LED_PIN 2 // Define the pin for the LED. Change this to your actual LED pin

void setup() {
  // DO NOT MODIFY OR REMOVE REMOTELY
  setupOTA(SSID, PASSWORD);  // DO NOT MODIFY OR REMOVE REMOTELY
  // DO NOT MODIFY OR REMOVE REMOTELY


  pinMode(LED_PIN, OUTPUT); // Initialize the LED pin as output

  setupFastLED(); // Initialize FastLED

}

void loop() {
  // DO NOT MODIFY OR REMOVE REMOTELY
  handleOTA();  // DO NOT MODIFY OR REMOVE REMOTELY
  // DO NOT MODIFY OR REMOVE REMOTELY


  // digitalWrite(LED_PIN, HIGH); // Turn the LED on
  // delay(500); // Wait for a second
  // digitalWrite(LED_PIN, LOW); // Turn the LED off
  // delay(500); // Wait for a second

  runLights(true); // Turn lights on

}