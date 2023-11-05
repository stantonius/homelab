// PubSubHandler.h

#ifndef PUBSUBHANDLER_H
#define PUBSUBHANDLER_H

#include <PubSubClient.h>
#include <WiFi.h>
#include "LEDHandler.h"
#include "Globals.h"

WiFiClient wifiClient;
PubSubClient client(wifiClient);
const char* mqttServer = "192.168.1.14";
const int mqttPort = 1883;
const char* deviceName = "BedroomLights";
const char* controlTopic = "home/lights/bedroom/control"; // The MQTT topic for light control



void callback(char* topic, byte* payload, unsigned int length) {
    // Convert the payload to a string
    char message[length + 1];
    memcpy(message, payload, length);
    message[length] = '\0';

    // Check if the topic matches our control topic
    if (strcmp(topic, controlTopic) == 0) {
        if (strcmp(message, "on") == 0) {
            // Display the pride animation
            lightsOn = true;
        } else if (strcmp(message, "off") == 0) {
            // Turn off the lights
            lightsOn = false;
        }
    }
}


void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect without username and password
        if (client.connect(deviceName)) {
            Serial.println("connected");
            // Subscribe to topic
            client.subscribe(controlTopic);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void setupPubSub() {
    client.setServer(mqttServer, mqttPort);
    client.setCallback(callback);
}

void handlePubSub() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}

#endif