import serial
import time
import sys
import os
import json
from Entities.RutasConfiguracion import (
    defects_model_path,
    color_model_path,
    captured_image_path,
    defect_labels_path,
    color_labels_path,
    contadores_path
)
from Entities.CargaModelos import cargar_etiquetas, cargar_modelo
from ImageAnalysis.CapturaImagen import capture_image
from Core.clasificadorPrediccion import classify_imagePredictor
from Models.ModelosDetectores.tamaño import AnalizadorTamano
from PIL import Image

# Contadores globales para las clasificaciones
contador_papasTomates_Grades = 0
contador_papasTomates_medianos = 0
contador_papasTomates_pequeñas = 0
contador_granel = 0
contador_defectuosos = 0

def main():
    global contador_papasTomates_Grades, contador_papasTomates_medianos, contador_papasTomates_pequeñas, contador_granel, contador_defectuosos

    # Configuración del puerto serial
    ser = serial.Serial('COM5', 9600)
    sensor_active = False

    # Agregar la ruta base al PYTHONPATH
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(base_path)

    # Cargar modelos y etiquetas
    defect_interpreter, defect_input_details, defect_output_details = cargar_modelo(defects_model_path)
    color_interpreter, color_input_details, color_output_details = cargar_modelo(color_model_path)
    defect_labels = cargar_etiquetas(defect_labels_path)
    color_labels = cargar_etiquetas(color_labels_path)

    print("Sistema iniciado, esperando señal del sensor infrarrojo...")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Mensaje recibido del Arduino: {line}")

            if line == "DETECTADO" and not sensor_active:
                sensor_active = True
                print("Movimiento detectado. Esperando 2 segundos antes de capturar la imagen...")
                time.sleep(2)

                ser.write(b"APAGAR\n")
                    # Leer la respuesta del Arduino
                while ser.in_waiting > 0:
                    respuesta = ser.readline().decode('utf-8').strip()
                    print(f"Arduino respondió: {respuesta}")

                print("Capturando imagen...")
                capture_image(captured_image_path)

                try:
                    image = Image.open(captured_image_path).convert("RGB")

                    defect_index, defect_confidence = classify_imagePredictor(
                        defect_interpreter, defect_input_details, defect_output_details, image
                    )
                    defect_label = defect_labels[defect_index]

                    if "Malos" in defect_label:
                        print(f"Defecto detectado: {defect_label}, Confianza: {defect_confidence}")
                        manejar_objeto_defectuoso(defect_label, ser)
                    else:
                        procesar_color_y_clasificar(image, color_interpreter, color_input_details, color_output_details, color_labels, ser)

                except FileNotFoundError:
                    print("El archivo de imagen no se encontró. Verifica la ruta.")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

                print("Esperando 5 segundos antes de volver a detectar...")
                time.sleep(5)
                print("Encendiendo el sensor y esperando nueva detección...")
                ser.write(b"ENCENDER\n")
                sensor_active = False

        time.sleep(0.1)

def manejar_objeto_defectuoso(defect_label, ser):
    global contador_defectuosos
    print(f"Objeto defectuoso detectado: {defect_label}")
    ser.write(b"DEFECTUOSO\n")
    print("Enviando a la caja de defectuosos.....")
    time.sleep(10)
    contador_defectuosos += 1
    print("Cantidad de objetos defectuosos: ", contador_defectuosos)
    contadoresAjson()

def procesar_color_y_clasificar(image, color_interpreter, input_details, output_details, color_labels, ser):
    global contador_papasTomates_Grades, contador_papasTomates_medianos, contador_papasTomates_pequeñas, contador_granel

    color_index, color_confidence = classify_imagePredictor(color_interpreter, input_details, output_details, image)
    color_label = color_labels[color_index]
    print(f"Se ha detectado un objeto sano, Confidence: {color_confidence}")
    print("Se procede a clasificar el objeto...")

    if "TomatesRojos(Maduros)" in color_label or "Papas" in color_label:
        print(f"Se detecta un/una ({color_label}), se procesará por tamaño...")
        analizador = AnalizadorTamano(image)
        clasificacion_tamaño, diametro_cm = analizador.analizar()

        if diametro_cm is not None:
            print(f"El diámetro detectado es: {diametro_cm:.2f} cm, Clasificación: {clasificacion_tamaño}")
            
            if clasificacion_tamaño == "Grande":
                ser.write(b"CAJA_GRANDES\n")
                time.sleep(2)
                print("Cantidad de objetos en caja de grandes: ", contador_papasTomates_Grades)
                contador_papasTomates_Grades += 1
                contadoresAjson()
            elif clasificacion_tamaño == "Mediano":
                ser.write(b"CAJA_MEDIANOS\n")
                time.sleep(4)
                print("Cantidad de objetos en caja de mediados: ", contador_papasTomates_medianos)
                contador_papasTomates_medianos += 1
                contadoresAjson()
            elif clasificacion_tamaño == "Pequeño":
                ser.write(b"CAJA_PEQUE\n")
                time.sleep(6)
                print("Cantidad de objetos en caja de pequeños: ", contador_papasTomates_pequeñas)
                contador_papasTomates_pequeñas += 1
                contadoresAjson()
        else:
            print("No se pudo detectar el contorno para analizar el tamaño.")

    elif "TomatesVerdes" in color_label or "TomatesAmarillos" in color_label:
        print(f"Se detecta un tomate {color_label.lower()}, se envía a Granel.")
        ser.write(b"SERVO_GRANEL_ON\n")
        time.sleep(8)
        contador_granel += 1
        print("Cantidad de objetos en la caja granel: ", contador_granel)
        contadoresAjson()

def esperar_respuesta(ser):
    while True:
        if ser.in_waiting > 0:
            respuesta = ser.readline().decode('utf-8').strip()
            if respuesta == "COMPLETADO":
                break

def contadoresAjson():
    with open(contadores_path, "w") as file:
        data = {
            "contadores": [
                {"nombre": "Tomates Grandes", "cantidad": contador_papasTomates_Grades},
                {"nombre": "Tomates Medianos", "cantidad": contador_papasTomates_medianos},
                {"nombre": "Tomates Pequeños", "cantidad": contador_papasTomates_pequeñas},
                {"nombre": "Tomates Granel", "cantidad": contador_granel},
                {"nombre": "Tomates Defectuosos", "cantidad": contador_defectuosos}
            ]
        }
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
