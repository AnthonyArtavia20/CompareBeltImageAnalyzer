import cv2

def capture_image(save_path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    print("Presiona 's' para capturar la imagen o 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el marco de la cámara.")
            break

        cv2.imshow("Capturando imagen", frame)

        # Presiona 's' para guardar la imagen, 'q' para salir
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(save_path, frame)
            print(f"Imagen guardada en {save_path}")
            break
        elif key == ord('q'):
            print("Saliendo sin capturar.")
            break

    cap.release()
    cv2.destroyAllWindows()
