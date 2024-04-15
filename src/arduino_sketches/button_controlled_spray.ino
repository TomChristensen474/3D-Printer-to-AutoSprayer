#include <Servo.h>

Servo servo;

int button_pin = 12;
int servo_pin = 9;
int no_spray_angle = 0;
int spray_angle = 90;
int angle;

void setup()
{
  Serial.begin(9600);

  servo.attach(servo_pin);

  pinMode(button_pin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  angle = no_spray_angle;
  servo.write(angle);
}

void loop()
{
  // Serial.println(digitalRead(button_pin));
  if (digitalRead(button_pin) == LOW)
  {
    digitalWrite(LED_BUILTIN, HIGH);

    if (angle <= spray_angle)
    {
      angle++;
      delay(2);
    }
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);

    if (angle > no_spray_angle)
    {
      angle--;
      delay(2);
    }
  }

  servo.write(angle);
}