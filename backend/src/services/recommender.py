import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from typing import List, Dict

class MoodRecommender:
    def __init__(self):
        # Initialize Spotify client
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )
        self.feature_weights = {
            'valence': 0.3,
            'energy': 0.2,
            'danceability': 0.15,
            'tempo': 0.15,
            'instrumentalness': 0.1,
            'acousticness': 0.1
        }

    def get_audio_features(self, track_id: str) -> Dict:
        """Get audio features for a track from Spotify"""
        try:
            return self.sp.audio_features(track_id)[0]
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            return None

    def get_recommendations_by_mood(self, mood: str, limit: int = 10) -> List[Dict]:
        """Get song recommendations based on mood"""
        # Mood-based feature targets
        mood_targets = {
            'happy': {'valence': 0.8, 'energy': 0.7},
            'sad': {'valence': 0.3, 'energy': 0.4},
            'energetic': {'valence': 0.6, 'energy': 0.9},
            'calm': {'valence': 0.5, 'energy': 0.3},
            'focused': {'valence': 0.5, 'energy': 0.5}
        }

        if mood not in mood_targets:
            raise ValueError(f"Unsupported mood: {mood}")

        # Get recommendations from Spotify based on mood targets
        recommendations = self.sp.recommendations(
            seed_genres=['pop', 'rock', 'indie', 'electronic'],
            target_valence=mood_targets[mood]['valence'],
            target_energy=mood_targets[mood]['energy'],
            limit=limit
        )

        # Enhance recommendations with audio features
        enhanced_recommendations = []
        for track in recommendations['tracks']:
            features = self.get_audio_features(track['id'])
            if features:
                enhanced_recommendations.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'features': features,
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify']
                })

        return enhanced_recommendations

    def compute_similarity(self, features1: Dict, features2: Dict) -> float:
        """Compute similarity between two songs based on their audio features"""
        v1 = np.array([features1[f] * self.feature_weights[f] 
                      for f in self.feature_weights.keys()])
        v2 = np.array([features2[f] * self.feature_weights[f] 
                      for f in self.feature_weights.keys()])
        return cosine_similarity(v1.reshape(1, -1), v2.reshape(1, -1))[0][0]

    def get_similar_songs(self, track_id: str, limit: int = 5) -> List[Dict]:
        """Get similar songs based on audio features"""
        base_features = self.get_audio_features(track_id)
        if not base_features:
            return []

        # Get a larger pool of recommendations to find the most similar
        recommendations = self.sp.recommendations(
            seed_tracks=[track_id],
            limit=limit * 2
        )

        similar_songs = []
        for track in recommendations['tracks']:
            features = self.get_audio_features(track['id'])
            if features:
                similarity = self.compute_similarity(base_features, features)
                similar_songs.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'similarity': similarity,
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify']
                })

        # Sort by similarity and return top results
        similar_songs.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_songs[:limit]
