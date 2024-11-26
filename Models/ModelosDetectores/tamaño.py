import cv2
import numpy as np
from PIL import Image

class AnalizadorTamano:
    FACTOR_CONVERSION = 50  # Ejemplo: 50 píxeles = 1 cm

    def __init__(self, imagen):
        self.imagen_np = np.array(imagen)  # Convertir la imagen a un array de NumPy

    def detectar_diametro(self):
        # Convertir a escala de grises
        gris = cv2.cvtColor(self.imagen_np, cv2.COLOR_RGB2GRAY)

        # Aplicar un filtro de umbral para obtener el contorno
        _, umbral = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

        # Encontrar contornos
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Encontrar el contorno más grande
        if contornos:
            contorno_max = max(contornos, key=cv2.contourArea)

            # Calcular el diámetro usando el contorno
            (x, y), radio = cv2.minEnclosingCircle(contorno_max)
            diametro = 2 * radio
            return diametro
        else:
            return None

    def clasificar_por_diametro(self, diametro):
        UMBRAL_PEQUEÑO = 7  # Umbral en cm
        UMBRAL_MEDIANO = 10  # Umbral en cm

        if diametro is not None:
            diametro_cm = diametro / self.FACTOR_CONVERSION
            if diametro_cm <= UMBRAL_PEQUEÑO:
                return "Pequeño", diametro_cm
            elif diametro_cm <= UMBRAL_MEDIANO:
                return "Mediano", diametro_cm
            else:
                return "Grande", diametro_cm
        else:
            return "No se pudo detectar el contorno", None

    def analizar(self):
        diametro = self.detectar_diametro()
        clasificacion, diametro_cm = self.clasificar_por_diametro(diametro)
        return clasificacion, diametro_cm
