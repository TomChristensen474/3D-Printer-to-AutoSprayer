#include <Servo.h>

Servo servo;

int voltage_input_pin = 10;
int servo_pin = 9;
int no_spray_angle = 0;
int spray_angle = 90;
int angle;

void setup()
{
  Serial.begin(9600);

  servo.attach(ServoPin);

  pinMode(voltage_input_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  angle = no_spray_angle;
  servo.write(angle);
}

void loop()
{
  if (digitalRead(voltage_input_pin) == HIGH)
  {
    digitalWrite(LED_BUILTIN, HIGH);

    if (angle <= spray_angle)
    {
      angle++;
      delay(5);
    }
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);

    if (angle > no_spray_angle)
    {
      angle--;
      delay(5);
    }
  }

  servo.write(angle);
}
