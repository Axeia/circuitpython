#include <HardwareSerial.h>

void setup() {
  Serial.begin(115200); // Begin the first serial port at 115200 baud
}

void loop() {
  if (Serial.available()) { // If data is available to read
    String data = Serial.readString(); // Read the incoming data
    Serial.println(data); // Print the incoming data to the serial monitor
  }
}
