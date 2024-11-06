import cv2
import time

def capture_image(save_path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    print("Esperando 2 segundo para estabilizar la cámara...")
    time.sleep(1)  # Espera de 2 segundo al inicializar la cámara

    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el marco de la cámara.")
    else:
        time.sleep(4) #Se agrega una pausa de 4 segundos antes de que tome la foto para que enfoque.
        cv2.imwrite(save_path, frame)
        print(f"Imagen guardada en {save_path}")

    cap.release()
    cv2.destroyAllWindows()
