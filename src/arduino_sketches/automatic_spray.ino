#include <Servo.h>

Servo servo;

int voltage_input_pin=10;
int servo_pin=9;
int no_spray_angle=0;
int spray_angle=90;
int angle;
                                                   
void setup() {
  Serial.begin(9600);

  servo.attach(ServoPin);

  pinMode(voltage_input_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

 servo.write(no_spray_angle);
 angle = 0;
}

void loop() {
  if (digitalRead(SensePin) == HIGH) {
    // Serial.println("spraying!");
    for (angle=angle; angle<=spray_angle; angle++) {
        servo.write(angle);
        // account for servo's travel time
        delay(3);
    }
  } else {
    for (angle=angle; angle>=no_spray_angle; angle--) {
        servo.write(angle);
        // account for servo's travel time
        delay(3);
    }
  }
}
