import cv2
import time

def find_camera():
    print("Buscando cámaras disponibles...")
    for i in range(10):  # Prueba los índices de 0 a 9
        for backend in [cv2.CAP_MSMF, cv2.CAP_VFW, cv2.CAP_ANY]:  # Probar diferentes backends
            cap = cv2.VideoCapture(i, backend)
            if cap.isOpened():
                print(f"Cámara detectada en el índice {i} con backend {backend}")
                cap.release()
                return i, backend
    print("No se detectó ninguna cámara disponible.")
    return -1, None

def capture_image(save_path):
    cam_index, backend = find_camera()
    if cam_index == -1:
        print("No se puede capturar la imagen porque no hay cámaras disponibles.")
        return

    cap = cv2.VideoCapture(cam_index, backend)
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    print("Esperando 2 segundos para estabilizar la cámara...")
    time.sleep(2)

    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el marco de la cámara.")
    else:
        cv2.imwrite(save_path, frame)
        print(f"Imagen guardada en {save_path}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image("captured_image.jpg")
