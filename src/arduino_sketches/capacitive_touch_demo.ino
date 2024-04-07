#include <CapacitiveSensor.h>
#include <Keyboard.h>

CapacitiveSensor sensor = CapacitiveSensor(4,2); // sensor between pins 4 and 2

void setup(){

sensor.set_CS_AutocaL_Millis(0xFFFFFFFF); // turn off autocalibrate on channel 1 - just as an example Serial.begin(9600);
Serial.begin(9600);

// Keyboard.begin();
}

void loop() {

long start = millis();

long sensor_data = sensor.capacitiveSensor(30);

if (sensor_data > 50) {
  // press SPACEBAR
  // Keyboard.write(32)
  // press A
  // Keyboard.write(65);
  Serial.println('A');
} else {
  // Keybaord.releaseAll();
}

delay(10); // arbitrary delay to limit data to serial port

}