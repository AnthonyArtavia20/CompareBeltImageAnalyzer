import sys
import os

# Agregar la ruta base al PYTHONPATH esto es para que pueda "devolverse" un directorio atrás
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_path)

from Entities.RutasConfiguracion import (
    defects_model_path,
    color_model_path,
    captured_image_path,
    defect_labels_path,
    color_labels_path
)
from Entities.CargaModelos import cargar_etiquetas, cargar_modelo
from functionAnalysis.CapturaImagen import capture_image
from DataManager.clasificadorPrediccion import classify_imagePredictor
from PIL import Image

# Capturar imagen
capture_image(captured_image_path)

# Cargar modelos
defect_interpreter, defect_input_details, defect_output_details = cargar_modelo(defects_model_path)
color_interpreter, color_input_details, color_output_details = cargar_modelo(color_model_path)

# Cargar etiquetas
defect_labels = cargar_etiquetas(defect_labels_path)
color_labels = cargar_etiquetas(color_labels_path)

# Cargar y clasificar la imagen capturada
try:
    image = Image.open(captured_image_path).convert("RGB")

    # Aplicar el modelo de defectos
    defect_index, defect_confidence = classify_imagePredictor(defect_interpreter, defect_input_details, defect_output_details, image)
    defect_label = defect_labels[defect_index]

    # Si se detectan defectos, imprimir "Defecto" y finalizar
    if "Malos" in defect_label:
        print(f"Defecto detectado en: {defect_label}, Confidence: {defect_confidence}. Se envía a la caja de dañados.")

        if "PapasMalas" in defect_label:
            print(f"Se detecta una papa mala {defect_label}, enviado a la caja de papas/tomates con defectos...")
        if "TomatesMalos" in defect_label:
            print(f"Se detecta un tomate malo {defect_label}, enviado a la caja de papas/tomates con defectos...")

    else:
        # Si no hay defectos, aplicar el modelo de color/objeto
        color_index, color_confidence = classify_imagePredictor(color_interpreter, color_input_details, color_output_details, image)
        color_label = color_labels[color_index]
        print(f"El objeto detectado es: {color_label}, no tiene defectos. Confidence: {color_confidence}")
        print("Se procede a clasificar el objeto sano...")

        # Clasificación según el color
        if "TomatesRojos(Maduros)" in color_label:
            print(f"Se detecta un tomate maduro ({color_label}), se procesará por tamaño...")
            

            #Procesa con el modelo de tamaño aqui: 
            #--><--

        elif "TomatesVerdes" in color_label:
            print(f"Se detecta un tomate verde ({color_label}), se envía a Granel.")
        elif "TomatesAmarillos" in color_label:
            print(f"Se detecta un tomate amarillo ({color_label}), se envía a Granel.")
        elif "Papas" in color_label:
            print(f"Se detecta una papa sana({color_label}).")

except FileNotFoundError:
    print("El archivo de imagen no se encontró. Verifica la ruta.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
