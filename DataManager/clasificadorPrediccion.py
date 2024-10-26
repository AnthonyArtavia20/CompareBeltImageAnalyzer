import numpy as np
from PIL import Image, ImageOps

def classify_imagePredictor(interpreter, input_details, output_details, image):
    size = input_details[0]['shape'][1:3]
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image).astype(np.float32)
    normalized_image_array = (image_array / 127.5) - 1.0
    input_data = np.expand_dims(normalized_image_array, axis=0)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtener la predicción
    output_data = interpreter.get_tensor(output_details[0]['index'])
    index = np.argmax(output_data)
    return index, output_data[0][index]
