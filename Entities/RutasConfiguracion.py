import os

# Establecer la ruta base actual (debería incluir 'CodigoCompareBelt')
base_path = os.getcwd()

# Carpeta donde se guardará la imagen capturada en el nuevo directorio
test_image_folder = os.path.join(base_path, "Client", "test")
os.makedirs(test_image_folder, exist_ok=True)

# Ruta para guardar la imagen capturada
captured_image_path = os.path.join(test_image_folder, "captured_image.jpg")

# Nuevas rutas para los modelos en base a 'CodigoCompareBelt'
defects_model_path = os.path.join(base_path, "Models", "ModelosDetectores", "defectos_model.tflite")
color_model_path = os.path.join(base_path, "Models", "ModelosDetectores", "color_model.tflite")

# Nuevas rutas para los archivos de etiquetas
defect_labels_path = os.path.join(base_path, "Models", "labelsDetectores", "labelsDefectosModel.txt")
color_labels_path = os.path.join(base_path, "Models", "labelsDetectores", "labelsColorModel.txt")
