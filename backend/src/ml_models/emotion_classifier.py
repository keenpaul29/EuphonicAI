import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Emotion labels
EMOTION_LABELS = [
    'angry', 
    'disgust', 
    'fear', 
    'happy', 
    'sad', 
    'surprise', 
    'neutral'
]

# Load pre-trained model (you'll need to train this separately)
def load_emotion_model(model_path='emotion_model.h5'):
    """
    Load pre-trained emotion classification model
    """
    try:
        model = load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Global model variable
emotion_model = load_emotion_model()

def preprocess_image(image):
    """
    Preprocess image for emotion classification
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize to 48x48 (typical size for emotion models)
    resized = cv2.resize(gray, (48, 48))
    
    # Normalize
    normalized = resized / 255.0
    
    # Reshape for model input
    input_image = img_to_array(normalized)
    input_image = np.expand_dims(input_image, axis=0)
    
    return input_image

def classify_emotion(image):
    """
    Classify emotion from an image
    
    :param image: OpenCV image (numpy array)
    :return: Tuple of (emotion, confidence)
    """
    if emotion_model is None:
        raise ValueError("Emotion model not loaded")
    
    # Preprocess image
    processed_image = preprocess_image(image)
    
    # Predict
    predictions = emotion_model.predict(processed_image)
    
    # Get the index of the highest confidence prediction
    emotion_index = np.argmax(predictions[0])
    confidence = predictions[0][emotion_index]
    
    # Map index to emotion label
    emotion = EMOTION_LABELS[emotion_index]
    
    return emotion, float(confidence)

def train_emotion_model(train_data, train_labels, validation_data=None, validation_labels=None):
    """
    Train a custom emotion classification model
    
    :param train_data: Training image data
    :param train_labels: Training labels
    :param validation_data: Optional validation data
    :param validation_labels: Optional validation labels
    :return: Trained model
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(7, activation='softmax')  # 7 emotions
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train the model
    history = model.fit(
        train_data, train_labels, 
        epochs=50, 
        validation_data=(validation_data, validation_labels) if validation_data is not None else None
    )
    
    # Save the model
    model.save('emotion_model.h5')
    
    return model
