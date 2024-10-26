import tensorflow as tf

def cargar_modelo(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

def cargar_etiquetas(labels_path):
    with open(labels_path, "r") as file:
        labels = [line.strip() for line in file.readlines()]
    return labels
