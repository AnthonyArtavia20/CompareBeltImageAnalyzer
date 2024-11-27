#include <Servo.h>

// Configuración del sensor infrarrojo
const int infraredSensorPin = 13;
int lastState = HIGH; // Estado inicial del sensor
bool sensorEnabled = true; // Controla si el sensor está activo

// Configuración de los servomotores
const int SERVO_STOP = 90;      // Detener el servo (punto neutral)
const int SERVO_FORWARD = 0;    // Velocidad máxima hacia adelante (horaria)
const int SERVO_BACKWARD = 180; // Velocidad máxima hacia atrás (antihoraria)
const int ANGULOEMPUJE = 45;    // Ángulo de empuje de los separadores
const int ANGULODESCANSO = 0;   // Ángulo de descanso de los separadores

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
  separadorGrandes.attach(6);
  separadorMedianos.attach(7);
  separadorPequenos.attach(8);
  separadorGranel.attach(9);
  separadorDefectuosos.attach(10);

  // Inicializa todos los servos en posición de descanso
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

  Serial.println("Arduino listo. Todos los separadores en posición inicial.");
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
      moverServosCinta(1500, SERVO_BACKWARD);
      moverSeparadores("Grandes");
    } else if (command == "CAJA_MEDIANOS") {
      moverServosCinta(3000, SERVO_BACKWARD);
      moverSeparadores("Medianos");
    } else if (command == "CAJA_PEQUE") {
      moverServosCinta(3500, SERVO_BACKWARD);
      moverSeparadores("Pequenos");
    } else if (command == "SERVO_GRANEL_ON") {
      moverServosCinta(7500, SERVO_BACKWARD);
      moverSeparadores("Granel");
    } else if (command == "DEFECTUOSO") {
      moverServosCinta(8000, SERVO_BACKWARD);
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
  
  //Conectar los servos temporalmente
  servoCinta1.attach(2);
  servoCinta2.attach(4);

  delay(10); // Pequeño retraso para estabilizar los servos

  //Mover Ambos servos
  servoCinta1.write(direccion);
  servoCinta2.write(direccion);
  delay(tiempoMovimiento);

  //Detener ambos servos
  servoCinta1.write(SERVO_STOP);
  servoCinta2.write(SERVO_STOP);

  // Desconecta el servoCinta2 después del movimiento
  servoCinta1.detach();
  servoCinta2.detach();

  Serial.println("Movimiento de cinta completado.");
}

void moverSeparadores(String servoSeparador) {
  Servo *servoSeleccionado = nullptr;

  // Seleccionar el servo correspondiente
  if (servoSeparador == "Grandes") {
    separadorGrandes.attach(6);
    servoSeleccionado = &separadorGrandes;
  } else if (servoSeparador == "Medianos") {
    separadorMedianos.attach(7);
    servoSeleccionado = &separadorMedianos;
  } else if (servoSeparador == "Pequenos") {
    separadorPequenos.attach(8);
    servoSeleccionado = &separadorPequenos;
  } else if (servoSeparador == "Granel") {
    separadorGranel.attach(9);
    servoSeleccionado = &separadorGranel;
  } else if (servoSeparador == "Defectuosos") {
    separadorDefectuosos.attach(10);
    servoSeleccionado = &separadorDefectuosos;
  } else {
    return;
  }

  // Realizar el movimiento
  delay(10); // Pequeño retraso después de conectar el servo
  servoSeleccionado->write(ANGULOEMPUJE); // Golpear
  delay(3000); // Mantener en la posición de golpe por 3 segundos
  Serial.println("Moviendo a posición de descanso...");
  servoSeleccionado->write(ANGULODESCANSO); // Volver a la posición de descanso
  delay(500); // Esperar para garantizar que el movimiento se complete

  // Mantener el servo conectado un poco más para asegurar que mantiene su posición
  delay(500);

  // Desconectar el servo después del movimiento
  servoSeleccionado->detach();

  Serial.print("Separador golpeado y vuelto a posición original: ");
  Serial.println(servoSeparador);
}
