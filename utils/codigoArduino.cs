#include <Servo.h>

// Configuración del sensor infrarrojo
const int infraredSensorPin = 13;
int lastState = HIGH; // Estado inicial del sensor
bool sensorEnabled = true; // Controla si el sensor está activo

// Configuración de los servomotores>
const int SERVO_STOP = 90;   // Detener el servo (punto neutral)
const int SERVO_FORWARD = 0; // Velocidad máxima hacia adelante
const int ANGULOEMPUJE = 45;
const int ANGULODESCANSO = 0;

//Servos de la cinta
Servo servoCinta1;
Servo servoCinta2;

//Servos separadores
Servo separadorGrandes;
Servo separadorMedianos;
Servo separadorPequenos;
Servo separadorGranel;
Servo separadorDefectuosos;

void setup() { //Inicializaciones
  Serial.begin(9600);

  pinMode(infraredSensorPin, INPUT);
  servoCinta1.attach(2); //Servo1 de la cinta en el pin 2
  servoCinta2.attach(3); //Servo2 de la cinta en el pin 3

  separadorGrandes.attach(4);
  separadorMedianos.attach(5);
  separadorPequenos.attach(6);
  separadorGranel.attach(7);
  separadorDefectuosos.attach(8);

  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);
  separadorGrandes.write(ANGULODESCANSO);
  separadorMedianos.write(ANGULODESCANSO);
  separadorPequenos.write(ANGULODESCANSO);
  separadorGranel.write(ANGULODESCANSO);
  separadorDefectuosos.write(ANGULODESCANSO);

  Serial.println("Arduino listo.");
}

void loop() { //Bucle principal donde se ejecutan las llamadas a las funciones y los servos.
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

    if (command == "CAJA_GRANDES"){
      moverServosCinta(2000);
      delay(2000);
      moverSeparadores("Grandes");
    } else if (command == "CAJA_MEDIANOS") {
      moverServosCinta(4000);
      delay(4000);
      moverSeparadores("Medianos");
    } else if (command == "CAJA_PEQUE") {
      moverServosCinta(6000);
      delay(6000);
      moverSeparadores("Pequeños");
    } else if (command == "SERVO_GRANEL_ON") {
      moverServosCinta(8000);
      delay(8000);
      moverSeparadores("Granel");
    } else if (command == "DEFECTUOSO") {
      moverServosCinta(10000);
      delay(10000);
      moverSeparadores("Defectuosos");
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

void moverSeparadores(String servoSeparador){ //Servos de las columnas
  //Definimos una variable constante que permitirá indiar cual servo mover.
  Servo *servoSeleccionado = nullptr;

  if (servoSeparador == "Grandes"){
    servoSeleccionado = &separadorGrandes;
  } else if (servoSeparador == "Medianos"){
    servoSeleccionado = &separadorMedianos;
  } else if (servoSeparador == "Pequenos"){
    servoSeleccionado = &separadorPequenos;
  } else if (servoSeparador == "Granel"){
    servoSeleccionado = &separadorGranel;
  } else if (servoSeparador == "Defectuosos"){
    servoSeleccionado = &separadorDefectuosos;
  } else {
    return;
  }

  //Mueve el servo seleccionado y almacenado en la variable:
  servoSeleccionado->write(ANGULOEMPUJE); //Empujar
  delay(1000); //Se espera a que se termina de ejecutar el movimiento de empujar
  servoSeleccionado->write(ANGULODESCANSO); //Se vuelve al estado de descanso.
  Serial.print("Separador movido: ");
  Serial.println(servoSeparador);
}