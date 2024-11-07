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

    # Puerto serial en escucha para el infra rojo.
    ser = serial.Serial('COM9', 9600)  # Aquí el puerto se puede cambiar a conveniencia, frecuencia no se toca.
    sensor_active = False

    # Agregar la ruta base al PYTHONPATH
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(base_path)

    # Cargar modelos y etiquetas una sola vez para optimizar
    defect_interpreter, defect_input_details, defect_output_details = cargar_modelo(defects_model_path)
    color_interpreter, color_input_details, color_output_details = cargar_modelo(color_model_path)
    defect_labels = cargar_etiquetas(defect_labels_path)
    color_labels = cargar_etiquetas(color_labels_path)

    print("Sistema iniciado, esperando señal del sensor infrarrojo...")

    while True:
        if ser.in_waiting > 0:  # Verifica si hay datos disponibles en el puerto serial
            line = ser.readline().decode('utf-8').strip()

            if line == "DETECTADO" and not sensor_active:  # Si la señal indica movimiento detectado
                sensor_active = True
                print("Movimiento detectado. Esperando 2 segundos antes de capturar la imagen...")
                time.sleep(2)  # Esperar 2 segundos
                
                # Capturar imagen
                print("Capturando imagen...")
                capture_image(captured_image_path)

                try:
                    image = Image.open(captured_image_path).convert("RGB")

                    # Aplicar el modelo de defectos
                    defect_index, defect_confidence = classify_imagePredictor(
                        defect_interpreter, defect_input_details, defect_output_details, image
                    )
                    defect_label = defect_labels[defect_index]

                    # Lógica de clasificación de defectos
                    if "Malos" in defect_label:
                        print(f"Defecto detectado: {defect_label}, Confianza: {defect_confidence}")
                        manejar_objeto_defectuoso(defect_label)
                    else:
                        procesar_color_y_clasificar(image, color_interpreter, color_input_details, color_output_details, color_labels)

                except FileNotFoundError:
                    print("El archivo de imagen no se encontró. Verifica la ruta.")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

                print("Esperando 5 segundos antes de volver a detectar...")
                time.sleep(5)  # Tiempo de espera tras el procesamiento
                sensor_active = False

        time.sleep(0.1)  # Pausa breve para no saturar la CPU

def manejar_objeto_defectuoso(defect_label):
    global contador_defectuosos
    print(f"Objeto defectuoso detectado: {defect_label}")
    contador_defectuosos += 1
    print("Cantidad de objetos defectuosos: ", contador_defectuosos)
    contadoresAjson()

def procesar_color_y_clasificar(image, color_interpreter, input_details, output_details, color_labels):
    global contador_papasTomates_Grades, contador_papasTomates_medianos, contador_papasTomates_pequeñas, contador_granel

    color_index, color_confidence = classify_imagePredictor(color_interpreter, input_details, output_details, image)
    color_label = color_labels[color_index]    
    print(f"Se ha detectado un objeto sano, Confidence: {color_confidence}")
    print("Se procede a clasificar el objeto...")

    # Lógica de clasificación según el color y tamaño
    if "TomatesRojos(Maduros)" in color_label or "Papas" in color_label:

        print(f"Se detecta un/una ({color_label}), se procesará por tamaño...")
        analizador = AnalizadorTamano(image)
        clasificacion_tamaño, diametro_cm = analizador.analizar()

        if diametro_cm is not None:
            print(f"El diámetro detectado es: {diametro_cm:.2f} cm, Clasificación: {clasificacion_tamaño}")
            if clasificacion_tamaño == "Grande":
                contador_papasTomates_Grades += 1
                print("Cantidad de objetos en caja de grandes: ", contador_papasTomates_Grades)
                contadoresAjson()
            elif clasificacion_tamaño == "Mediano":
                contador_papasTomates_medianos += 1
                print("Cantidad de objetos en caja de mediados: ", contador_papasTomates_medianos)
                contadoresAjson()
            elif clasificacion_tamaño == "Pequeño":
                contador_papasTomates_pequeñas += 1
                print("Cantidad de objetos en caja de pequeños: ", contador_papasTomates_pequeñas)
                contadoresAjson()
        else:
            print("No se pudo detectar el contorno para analizar el tamaño.")
    elif "TomatesVerdes" in color_label or "TomatesAmarillos" in color_label:
        print(f"Se detecta un tomate {color_label.lower()}, se envía a Granel.")
        contador_granel += 1
        print("Cantidad de objetos en la caja granel: ", contador_granel)
        contadoresAjson()

def contadoresAjson():
    # Envia los contadores a un archivo json
    with open(contadores_path, "w") as file:
        data = {
            "contadores": [
                {"nombre": "Grandes", "cantidad": contador_papasTomates_Grades},
                {"nombre": "Medianos", "cantidad": contador_papasTomates_medianos},
                {"nombre": "Pequeños", "cantidad": contador_papasTomates_pequeñas},
                {"nombre": "Granel", "cantidad": contador_granel},
                {"nombre": "Defectuosos", "cantidad": contador_defectuosos}
            ]
        }
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
