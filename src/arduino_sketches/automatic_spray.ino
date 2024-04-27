#include <Servo.h>

Servo servo;

int voltage_input_pin = A0;
int servo_pin = 9;
int no_spray_angle = 10;
int spray_angle = 65;
int angle;

void setup()
{
  Serial.begin(9600);

  servo.attach(servo_pin);

  pinMode(voltage_input_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  angle = no_spray_angle;
  servo.write(angle);
}

void loop()
{
  int sensor_value = analogRead(A0);
  float voltage = sensor_value * (5.0 / 1023.0);
  if (voltage > 1)
  {
    digitalWrite(LED_BUILTIN, HIGH);

    if (angle <= spray_angle)
    {
      angle++;
      delay(3);
    }
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);

    if (angle > no_spray_angle)
    {
      angle--;
      delay(3);
    }
  }

  servo.write(angle);
}
