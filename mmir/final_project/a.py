import numpy as np
import tensorflow as tf
import cv2 as cv

# Load TFLite model and allocate tensors.
interpreter = tf.contrib.lite.Interpreter(model_path="/Users/cuongpham/Documents/mmir/final_project/object-detection/detect.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# Test model on random input data.

img = cv.imread('cat.jpg')
 
img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
# print(img.shape)
input_shape = input_details[0]['shape']

input_data = img
# print(input_data.shape)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data.shape)
print(output_data)