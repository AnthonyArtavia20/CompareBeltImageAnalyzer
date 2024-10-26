import cv2  # cv2 (OpenCV): Se usa para el procesamiento de imágenes y la detección de contornos.
import numpy as np  # numpy: Se utiliza para manipular y transformar la imagen en una matriz numérica.
from PIL import Image  # PIL (Pillow): Se usa para cargar la imagen y convertirla al formato correcto para el procesamiento.

# Factor de conversión de píxeles a centímetros (ajustar según necesidad)
FACTOR_CONVERSION = 50  # Ejemplo: 50 píxeles = 1 cm

# Cargar la imagen y convertirla a NumPy
imagen = Image.open(r"C:\Users\Anthony\Desktop\CodigoCompareBelt\test\papagrande.jpg").convert("RGB")
imagen_np = np.array(imagen)  # Se convierte en un array de NumPy, lo cual es necesario para que OpenCV pueda procesarla.

def detectar_diametro(imagen_np):  # Objetivo: Encontrar el diámetro de un objeto circular en la imagen
    # Convertir a escala de grises
        #Convierte la imagen de RGB a escala de grises para simplificar el procesamiento.
        #La escala de grises reduce la complejidad de la imagen, ya que solo necesita un canal en lugar de tres (rojo, verde, azul).
    gris = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2GRAY)

    # Aplicar un filtro de umbral para obtener el contorno
        #Aplica un umbral binario a la imagen, lo cual convierte los píxeles a blanco (255) si su valor es mayor que 127, o a negro (0) si es menor.
        #Esto facilita la detección de contornos, ya que convierte la imagen en blanco y negro.
    _, umbral = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

    # Encontrar contornos
        #cv2.findContours() detecta los contornos de los objetos en la imagen binaria.
        #Se usa cv2.RETR_EXTERNAL para detectar solo los contornos externos y cv2.CHAIN_APPROX_SIMPLE para simplificar los contornos detectados.
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande
    if contornos:  # Verifica si se encuentran contornos (un tomate redondo o papa redonda)
        contorno_max = max(contornos, key=cv2.contourArea)  # Selecciona el contorno más grande

        # Calcular el diámetro usando el contorno
        (x, y), radio = cv2.minEnclosingCircle(contorno_max)  # Encuentra el círculo más pequeño que encierra el contorno

        diametro = 2 * radio
        return diametro
    else:
        return None

# Clasificación basada en el diámetro retornado
def clasificar_por_diametro(diametro_cm):
    UMBRAL_PEQUEÑO = 71  # Umbral en cm
    UMBRAL_MEDIANO = 120  # Umbral en cm

    if diametro_cm is not None:
        if diametro_cm <= UMBRAL_PEQUEÑO:
            return "Pequeño"
        elif diametro_cm <= UMBRAL_MEDIANO:
            return "Mediano"
        else:
            return "Grande"
    else:
        return "No se pudo detectar el contorno"

# Detectar el diámetro en píxeles
diametro = detectar_diametro(imagen_np)

# Convertir de píxeles a centímetros y clasificar
if diametro is not None:
    diametro_cm = diametro / FACTOR_CONVERSION # arriba está es 50px = 1cm
    resultado = clasificar_por_diametro(diametro_cm)
    print(f"El diámetro detectado del objeto es: {diametro_cm:.2f} cm, Clasificación: {resultado}")
else:
    print("No se pudo detectar el contorno, no se logra encontrar un objeto redondo.")
