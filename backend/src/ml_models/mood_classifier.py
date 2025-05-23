import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

class MoodClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.mood_labels = ['happy', 'sad', 'energetic', 'calm', 'focused']

    def preprocess_features(self, features):
        """Preprocess audio features for model input"""
        return self.scaler.transform(features)

    def train(self, X, y):
        """Train the mood classifier"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict_mood(self, features):
        """Predict mood from audio features"""
        X_scaled = self.preprocess_features(features.reshape(1, -1))
        return self.mood_labels[self.model.predict(X_scaled)[0]]

    def save_model(self, path):
        """Save the trained model"""
        joblib.dump({'model': self.model, 'scaler': self.scaler}, path)

    def load_model(self, path):
        """Load a trained model"""
        saved_model = joblib.load(path)
        self.model = saved_model['model']
        self.scaler = saved_model['scaler']
