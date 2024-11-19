#include <Servo.h>

// Configuración del sensor infrarrojo
const int infraredSensorPin = 13;
int lastState = HIGH; // Estado inicial del sensor
bool sensorEnabled = true; // Controla si el sensor está activo

// Configuración de los servomotores>
const int SERVO_STOP = 90;   // Detener el servo (punto neutral)
const int SERVO_FORWARD = 0; // Velocidad máxima hacia adelante
Servo servoCinta1;
Servo servoCinta2;

void setup() {
  Serial.begin(9600);

  pinMode(infraredSensorPin, INPUT);
  servoCinta1.attach(2); //Servo1 de la cinta en el pin 2
  servoCinta2.attach(3); //Servo2 de la cinta en el pin 3

  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);

  Serial.println("Arduino listo.");
}

void loop() {
  if (sensorEnabled) {
    int currentState = digitalRead(infraredSensorPin);

    if (currentState == LOW && lastState == HIGH) {
      Serial.println("DETECTADO");
      sensorEnabled = false; // Desactiva el sensor hasta recibir "ENCENDER"
    }

    lastState = currentState;
  }

  while (Serial.available()>0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.println("Comando recibido: " + command); // Depuración

    if (command == "CAJA_GRANDES")
    {
      moverServosCinta(2000);
    } else if (command == "CAJA_MEDIANOS") {
      moverServosCinta(4000);
    } else if (command == "CAJA_PEQUE") {
      moverServosCinta(6000);
    } else if (command == "SERVO_GRANEL_ON") {
      moverServosCinta(8000);
    } else if (command == "DEFECTUOSO") {
      moverServosCinta(10000);
    } else if (command == "ENCENDER") {
      sensorEnabled = true;
      Serial.println("SENSOR_ENCENDIDO");
    } else {
      Serial.println("COMANDO_DESCONOCIDO");
    }
  }
}

void moverServosCinta(int tiempoMovimiento) { //Para mover los servos dedicados a la cinta.
  servoCinta1.write(SERVO_FORWARD);
  servoCinta2.write(SERVO_FORWARD);
  delay(tiempoMovimiento);
  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);
  Serial.println("COMPLETADO");
}
