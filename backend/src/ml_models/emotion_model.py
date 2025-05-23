import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import img_to_array
import cv2

class EmotionClassifier:
    def __init__(self, input_shape=(48, 48, 1), num_classes=7):
        """
        Initialize emotion classification model
        
        Emotion classes:
        0: Angry
        1: Disgust
        2: Fear
        3: Happy
        4: Sad
        5: Surprise
        6: Neutral
        """
        self.model = self._build_model(input_shape, num_classes)
        self.emotion_labels = [
            'Angry', 'Disgust', 'Fear', 
            'Happy', 'Sad', 'Surprise', 'Neutral'
        ]

    def _build_model(self, input_shape, num_classes):
        """
        Build a Convolutional Neural Network for emotion classification
        """
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def preprocess_image(self, image_path):
        """
        Preprocess image for emotion detection
        """
        # Read image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Resize to 48x48
        image = cv2.resize(image, (48, 48))
        
        # Convert to array and normalize
        image = img_to_array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        
        return image

    def predict_emotion(self, image_path):
        """
        Predict emotion from an image
        """
        preprocessed_image = self.preprocess_image(image_path)
        
        # Predict
        predictions = self.model.predict(preprocessed_image)[0]
        emotion_index = np.argmax(predictions)
        confidence = predictions[emotion_index]
        
        return {
            'emotion': self.emotion_labels[emotion_index],
            'confidence': float(confidence)
        }

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        """
        Train the model (placeholder for actual training data)
        """
        # In a real scenario, you'd pass actual training data
        self.model.fit(
            X_train, y_train, 
            epochs=epochs, 
            batch_size=batch_size, 
            validation_split=0.2
        )

    def save_model(self, filepath='emotion_model.h5'):
        """
        Save trained model
        """
        self.model.save(filepath)

    def load_model(self, filepath='emotion_model.h5'):
        """
        Load pre-trained model
        """
        self.model = tf.keras.models.load_model(filepath)

# Create and save a default model if not exists
def create_default_emotion_model():
    classifier = EmotionClassifier()
    
    # Generate dummy training data for initial model
    X_train = np.random.random((100, 48, 48, 1))
    y_train = tf.keras.utils.to_categorical(
        np.random.randint(7, size=(100, 1)), 
        num_classes=7
    )
    
    classifier.train(X_train, y_train, epochs=5)
    classifier.save_model()
    return classifier

# Instantiate the model if not already present
emotion_classifier = create_default_emotion_model()
