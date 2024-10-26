import sys
import os

# Agregar la ruta base al PYTHONPATH
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
from DataManager.clasificadorPrediccion import classify_image
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
    defect_index, defect_confidence = classify_image(defect_interpreter, defect_input_details, defect_output_details, image)
    defect_label = defect_labels[defect_index]

    # Verificar defectos
    if "Malos" in defect_label:
        print(f"Defecto detectado en: {defect_label}, Confidence: {defect_confidence}. Se envía a la caja de dañados.")
    else:
        color_index, color_confidence = classify_image(color_interpreter, color_input_details, color_output_details, image)
        color_label = color_labels[color_index]
        print(f"El objeto detectado es: {color_label}, no tiene defectos. Confidence: {color_confidence}")

except FileNotFoundError:
    print("El archivo de imagen no se encontró. Verifica la ruta.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
