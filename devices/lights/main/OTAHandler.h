#ifndef OTA_HANDLER_H
#define OTA_HANDLER_H

#include <WiFi.h>
#include <ArduinoOTA.h>

void setupOTA(const char* ssid, const char* password) {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  ArduinoOTA.begin();
  
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void handleOTA() {
  ArduinoOTA.handle();
}

#endif // OTA_HANDLER_H
