import tensorflow as tf

# Load model
model_path = "./model/mobilefacenet.tflite"  # letakkan di root proyek sementara
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input & output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("=== Input Details ===")
print("Shape:", input_details[0]['shape'])
print("Type:", input_details[0]['dtype'])
print("Name:", input_details[0]['name'])

print("\n=== Output Details ===")
print("Shape:", output_details[0]['shape'])
print("Type:", output_details[0]['dtype'])
print("Name:", output_details[0]['name'])