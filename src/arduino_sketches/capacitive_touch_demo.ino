#include <CapacitiveSensor.h>
#include <Keyboard.h>

CapacitiveSensor sensor1 = CapacitiveSensor(9,8); // sensor between pins 4 and 2
CapacitiveSensor sensor2 = CapacitiveSensor(7,6); // sensor between pins 4 and 2
CapacitiveSensor sensor3 = CapacitiveSensor(4,5); // sensor between pins 4 and 2
CapacitiveSensor sensor4 = CapacitiveSensor(15,14); // sensor between pins 4 and 2

void setup(){

sensor1.set_CS_AutocaL_Millis(0xFFFFFFFF); // turn off autocalibrate on channel 1
sensor2.set_CS_AutocaL_Millis(0xFFFFFFFF);
sensor3.set_CS_AutocaL_Millis(0xFFFFFFFF);
sensor4.set_CS_AutocaL_Millis(0xFFFFFFFF);

// Serial.begin(921600);

Keyboard.begin();
}

void loop() {
  long sensor_data1 = sensor1.capacitiveSensor(120);
  long sensor_data2 = sensor2.capacitiveSensor(120);
  long sensor_data3 = sensor3.capacitiveSensor(120);
  long sensor_data4 = sensor4.capacitiveSensor(120);
  if (sensor_data1 > 25) {
    // press RIGHT ARROW
    Keyboard.write(39);
  } else {
    Keyboard.release(39);
  }
  if (sensor_data2 > 25) {
    // press Z (jump - A)
    Keyboard.write(90);
  } else {
    Keyboard.release(90);
  }
  if (sensor_data3 > 200) {
    // press LEFT ARROW
    Keyboard.write(37);
  } else {
    Keyboard.release(37);
  }
  if (sensor_data4 > 200) {
    // press X (use ability - B)
    Keyboard.write(88);
  } else {
    Keyboard.release(88);
  }

}