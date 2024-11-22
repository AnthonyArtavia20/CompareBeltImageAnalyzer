#include <Servo.h>

// Configuración del sensor infrarrojo
const int infraredSensorPin = 13;
int lastState = HIGH; // Estado inicial del sensor
bool sensorEnabled = true; // Controla si el sensor está activo

// Configuración de los servomotores
const int SERVO_STOP = 90;      // Detener el servo (punto neutral)
const int SERVO_FORWARD = 0;    // Velocidad máxima hacia adelante (horaria)
const int SERVO_BACKWARD = 180; // Velocidad máxima hacia atrás (antihoraria)
const int ANGULOEMPUJE = 45;
const int ANGULODESCANSO = 0;

// Servos de la cinta
Servo servoCinta1; // Siempre conectado
Servo servoCinta2;

// Servos separadores
Servo separadorGrandes;
Servo separadorMedianos;
Servo separadorPequenos;
Servo separadorGranel;
Servo separadorDefectuosos;

void setup() {
  Serial.begin(9600);

  pinMode(infraredSensorPin, INPUT);

  // Conecta y configura los servos inicialmente
  servoCinta1.attach(2); // Mantener siempre conectado
  servoCinta2.attach(4);
  separadorGrandes.attach(4);
  separadorMedianos.attach(5);
  separadorPequenos.attach(6);
  separadorGranel.attach(7);
  separadorDefectuosos.attach(8);

  // Inicializa todos los servos en posición neutra
  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);
  separadorGrandes.write(ANGULODESCANSO);
  separadorMedianos.write(ANGULODESCANSO);
  separadorPequenos.write(ANGULODESCANSO);
  separadorGranel.write(ANGULODESCANSO);
  separadorDefectuosos.write(ANGULODESCANSO);

  // Desconecta los servos no utilizados después de configurarlos
  servoCinta2.detach();
  separadorGrandes.detach();
  separadorMedianos.detach();
  separadorPequenos.detach();
  separadorGranel.detach();
  separadorDefectuosos.detach();

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

  while (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.println("Comando recibido: " + command); // Depuración

    if (command == "CAJA_GRANDES") {
      moverServosCinta(2000, SERVO_BACKWARD);
      delay(2000);
      moverSeparadores("Grandes");
    } else if (command == "CAJA_MEDIANOS") {
      moverServosCinta(4000, SERVO_BACKWARD);
      delay(4000);
      moverSeparadores("Medianos");
    } else if (command == "CAJA_PEQUE") {
      moverServosCinta(6000, SERVO_BACKWARD);
      delay(6000);
      moverSeparadores("Pequenos");
    } else if (command == "SERVO_GRANEL_ON") {
      moverServosCinta(8000, SERVO_BACKWARD);
      delay(8000);
      moverSeparadores("Granel");
    } else if (command == "DEFECTUOSO") {
      moverServosCinta(10000, SERVO_BACKWARD);
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

void moverServosCinta(int tiempoMovimiento, int direccion) {
  // Mantén servoCinta1 siempre conectado
  servoCinta1.write(direccion);

  // Conecta el servoCinta2 temporalmente
  servoCinta2.attach(4);
  delay(10); // Pequeño retraso para estabilizar el servo

  servoCinta2.write(direccion);
  delay(tiempoMovimiento);

  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);

  // Desconecta el servoCinta2 después del movimiento
  servoCinta2.detach();

  Serial.println("COMPLETADO");
}

void moverSeparadores(String servoSeparador) {
  Servo *servoSeleccionado = nullptr;

  if (servoSeparador == "Grandes") {
    separadorGrandes.attach(4);
    servoSeleccionado = &separadorGrandes;
  } else if (servoSeparador == "Medianos") {
    separadorMedianos.attach(5);
    servoSeleccionado = &separadorMedianos;
  } else if (servoSeparador == "Pequenos") {
    separadorPequenos.attach(6);
    servoSeleccionado = &separadorPequenos;
  } else if (servoSeparador == "Granel") {
    separadorGranel.attach(7);
    servoSeleccionado = &separadorGranel;
  } else if (servoSeparador == "Defectuosos") {
    separadorDefectuosos.attach(8);
    servoSeleccionado = &separadorDefectuosos;
  } else {
    return;
  }

  delay(10); // Pequeño retraso después de conectar el servo
  servoSeleccionado->write(ANGULOEMPUJE); // Empujar
  delay(1000);
  servoSeleccionado->write(ANGULODESCANSO); // Volver al estado de descanso

  // Desconecta el servo después de moverlo
  servoSeleccionado->detach();

  Serial.print("Separador movido: ");
  Serial.println(servoSeparador);
}
