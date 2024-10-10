#include <Servo.h>

const int trigPin = 7;
const int echoPin = 8;
const int potPin = A0;
Servo servoMotor;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  servoMotor.attach(9);
  servoMotor.write(0);
  Serial.begin(9600);
}

void loop() {
  int valorPot = analogRead(potPin);
  int distanciaLimite = map(valorPot, 0, 1023, 0, 440);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duracao = pulseIn(echoPin, HIGH);
  int distancia = duracao * 0.034 / 2;

  Serial.print("Distancia: ");
  Serial.print(distancia);
  Serial.print(" cm | Limiar: ");
  Serial.print(distanciaLimite);
  Serial.println(" cm");

  if (distancia <= distanciaLimite) {
    servoMotor.write(90);
  } else if (distancia < 440) {
    servoMotor.write(0);
  }

  delay(500);
}
