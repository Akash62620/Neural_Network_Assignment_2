# -*- coding: utf-8 -*-
"""HomeAssignment2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DJa55bKEhuvGAIIoHOnOF5yQO-dSlrFT
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, Input, MaxPooling2D, AveragePooling2D, InputLayer, Flatten, Dense, Dropout, Add
import cv2
import matplotlib.pyplot as plt

"""# --- QUESTION 2: Convolution Operations ---

"""

# Define the 5x5 input matrix
input_matrix = np.array([
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [6, 7, 8, 9, 0],
    [0, 9, 8, 7, 6],
    [1, 3, 5, 7, 9]
], dtype=np.float32).reshape((1, 5, 5, 1))

# Define the 3x3 kernel
kernel = np.array([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]
], dtype=np.float32).reshape((3, 3, 1, 1))

# Define a single reusable model
def build_model(stride, padding):
    model = Sequential([
        Input(shape=(5, 5, 1)),  # Input Layer
        Conv2D(filters=1, kernel_size=(3, 3), strides=stride, padding=padding, use_bias=False)
    ])
    model.layers[0].set_weights([kernel])
    return model

# Apply convolution using the same model instance to prevent retracing

def apply_convolution(model):
    output = model.predict(input_matrix)
    return output[0, :, :, 0]

# Running for different stride and padding values
for stride, padding in [(1, 'valid'), (1, 'same'), (2, 'valid'), (2, 'same')]:
    model = build_model(stride, padding)
    output_feature_map = apply_convolution(model)
    print(f"\nStride = {stride}, Padding = '{padding}'")
    print(output_feature_map)

"""# --- QUESTION 3: Edge Detection and Pooling ---"""

# --- TASK 1: EDGE DETECTION USING SOBEL FILTER ---

def apply_sobel_filter(image_path):
    """Applies Sobel filter for edge detection in X and Y directions with improved visibility."""
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Sobel filters
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # X-direction
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)  # Y-direction

    # Convert to absolute values to enhance visibility
    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)

    # Display images using matplotlib
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(sobel_x, cmap='gray')
    plt.title("Sobel X (Enhanced)")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(sobel_y, cmap='gray')
    plt.title("Sobel Y (Enhanced)")
    plt.axis("off")

    plt.show()

# --- TASK 2: MAX POOLING AND AVERAGE POOLING ---

# Generate a random 4x4 matrix (as a sample input image)
input_matrix = np.random.rand(1, 4, 4, 1).astype(np.float32)

# Define a model with both MaxPooling and AveragePooling
model_pooling = Sequential([
    InputLayer(input_shape=(4, 4, 1)),  # Input layer
    MaxPooling2D(pool_size=(2,2), strides=2, name='max_pooling'),  # Max Pooling
    AveragePooling2D(pool_size=(2,2), strides=2, name='avg_pooling')  # Avg Pooling
])

# Get the outputs
max_pooled_output = model_pooling.get_layer('max_pooling')(input_matrix).numpy()
avg_pooled_output = model_pooling.get_layer('avg_pooling')(input_matrix).numpy()

# Print results
print("\nOriginal Matrix:\n", input_matrix[0, :, :, 0])
print("\nMax Pooled Matrix:\n", max_pooled_output[0, :, :, 0])
print("\nAverage Pooled Matrix:\n", avg_pooled_output[0, :, :, 0])

# Example usage (Upload an image and provide the correct path)
apply_sobel_filter("/content/Bob-Junior.jpg")

"""# --- QUESTION 4: CNN Architectures ---"""

# --- TASK 1: IMPLEMENT ALEXNET ---

def build_alexnet():
    """Builds a simplified AlexNet model."""
    model = Sequential([
        Conv2D(96, (11, 11), strides=4, activation='relu', input_shape=(227, 227, 3)),
        MaxPooling2D(pool_size=(3, 3), strides=2),
        Conv2D(256, (5, 5), activation='relu', padding="same"),
        MaxPooling2D(pool_size=(3, 3), strides=2),
        Conv2D(384, (3, 3), activation='relu', padding="same"),
        Conv2D(384, (3, 3), activation='relu', padding="same"),
        Conv2D(256, (3, 3), activation='relu', padding="same"),
        MaxPooling2D(pool_size=(3, 3), strides=2),
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')  # 10 classes output
    ])

    return model

# Create AlexNet model and print summary
alexnet_model = build_alexnet()
print("\nAlexNet Model Summary:")
alexnet_model.summary()


# --- TASK 2: IMPLEMENT RESNET-LIKE MODEL ---

def residual_block(input_tensor, filters):
    """Defines a simple residual block with skip connections."""
    x = Conv2D(filters, (3, 3), activation='relu', padding='same')(input_tensor)
    x = Conv2D(filters, (3, 3), activation='relu', padding='same')(x)
    x = Add()([x, input_tensor])  # Skip connection (adds input to output)
    return x

def build_resnet():
    """Builds a simple ResNet-like model."""
    inputs = Input(shape=(32, 32, 3))  # CIFAR-10 size input
    x = Conv2D(64, (7, 7), strides=2, activation='relu', padding='same')(inputs)
    x = residual_block(x, 64)
    x = residual_block(x, 64)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    outputs = Dense(10, activation='softmax')(x)  # 10 classes output

    model = Model(inputs, outputs)
    return model

# Create ResNet-like model and print summary
resnet_model = build_resnet()
print("\nResNet-like Model Summary:")
resnet_model.summary()
