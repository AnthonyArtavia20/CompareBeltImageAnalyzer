#Aquí se hace la clasificación de los objetos utilizando la mayoría 
#de archivos y modelos en las distintas carpetas del programa.

#Contadores globales para las clasificaciones
contador_papasTomates_Grades = 0
contador_papasTomates_medianos = 0
contador_papasTomates_pequeñas = 0
contador_granel = 0
contador_defectuosos = 0


def main():

    global contador_papasTomates_Grades, contador_papasTomates_medianos, contador_papasTomates_pequeñas, contador_granel, contador_defectuosos
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
    from ImageAnalysis.CapturaImagen import capture_image
    from Core.clasificadorPrediccion import classify_imagePredictor
    from Models.ModelosDetectores.tamaño import AnalizadorTamano
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
            print(f"Se ha detectado un objeto sano, Confidence: {color_confidence}")
            print("Se procede a clasificar el objeto...")

            # Clasificación según el color
            if "TomatesRojos(Maduros)" in color_label:
                print(f"Se detecta un tomate maduro ({color_label}), se procesará por tamaño...")

                # Crear instancia de AnalizadorTamaño y procesar la imagen
                analizador = AnalizadorTamano(image)
                clasificacion_tamaño, diametro_cm = analizador.analizar()

                if diametro_cm is not None:
                    print(f"El diámetro detectado es: {diametro_cm:.2f} cm, Clasificación: {clasificacion_tamaño}")

                    if clasificacion_tamaño == "Grande":
                        contador_papasTomates_Grades += 1

                        print("Cantidad de objetos en caja de grandes: ", contador_papasTomates_Grades)
                    if clasificacion_tamaño == "Mediano":
                        contador_papasTomates_medianos += 1

                        print("Cantidad de objetos en caja de mediados: " ,contador_papasTomates_medianos)
                    if clasificacion_tamaño == "Pequeño":
                        contador_papasTomates_pequeñas += 1

                        print("Cantidad de objetos en caja de pequeños: ", contador_papasTomates_pequeñas)
                else:
                    print("No se pudo detectar el contorno para analizar el tamaño.")

            elif "TomatesVerdes" in color_label or "TomatesAmarillos" in color_label:
                print(f"Se detecta un tomate {color_label.lower()}, se envía a Granel.")

                contador_granel += 1
                print("Cantidad de objetos en la caja granel: ", contador_granel)

            elif "Papas" in color_label:
                print(f"Se detecta una papa sana({color_label}), se procederá a analizar su tamaño.")

                # Crear instancia de AnalizadorTamano y procesar la imagen
                analizador = AnalizadorTamano(image)
                clasificacion_tamaño, diametro_cm = analizador.analizar()

                if diametro_cm is not None:
                    print(f"El diámetro detectado es: {diametro_cm:.2f} cm, Clasificación: {clasificacion_tamaño}")

                    #Aquí se añadirán los condicionales de si es pequeño, mediano o grande sepa donde dirigir el tomate maduro en la cinta
                    # ---><---
                else:
                    print("No se pudo detectar el contorno para analizar el tamaño.")

    except FileNotFoundError:
        print("El archivo de imagen no se encontró. Verifica la ruta.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()