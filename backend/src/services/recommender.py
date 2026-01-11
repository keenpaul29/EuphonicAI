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
        if not client_id or not client_secret:
            print("Warning: Spotify credentials not found in environment variables.")
            self.sp = None
        else:
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
        if not self.sp: return None
        try:
            features = self.sp.audio_features(track_id)
            return features[0] if features else None
        except Exception as e:
            print(f"Error fetching audio features: {e}")
            return None

    def get_recommendations_by_mood(self, mood: str, limit: int = 12) -> List[Dict]:
        """Get song recommendations based on mood"""
        if not self.sp: return []
        
        # Comprehensive mood-based mapping
        mood_configs = {
            'happy': {
                'targets': {'target_valence': 0.8, 'target_energy': 0.7, 'target_danceability': 0.7},
                'genres': ['pop', 'happy', 'dance', 'summer']
            },
            'sad': {
                'targets': {'target_valence': 0.2, 'target_energy': 0.3, 'target_acousticness': 0.7},
                'genres': ['acoustic', 'sad', 'blues', 'rainy-day']
            },
            'energetic': {
                'targets': {'target_valence': 0.6, 'target_energy': 0.9, 'target_danceability': 0.8},
                'genres': ['work-out', 'edm', 'rock', 'party']
            },
            'calm': {
                'targets': {'target_valence': 0.5, 'target_energy': 0.2, 'target_acousticness': 0.8},
                'genres': ['ambient', 'chill', 'sleep', 'study']
            },
            'angry': {
                'targets': {'target_valence': 0.3, 'target_energy': 0.9, 'target_danceability': 0.5},
                'genres': ['metal', 'hardcore', 'punk', 'rock']
            },
            'neutral': {
                'targets': {'target_valence': 0.5, 'target_energy': 0.5},
                'genres': ['indie', 'pop', 'folk', 'chill']
            },
            'surprised': {
                'targets': {'target_valence': 0.7, 'target_energy': 0.8},
                'genres': ['electronic', 'pop', 'dance']
            },
            'fearful': {
                'targets': {'target_valence': 0.3, 'target_energy': 0.4},
                'genres': ['ambient', 'soundtrack', 'dark-chills']
            },
            'disgusted': {
                'targets': {'target_valence': 0.4, 'target_energy': 0.5},
                'genres': ['indie', 'alternative', 'grunge']
            }
        }

        config = mood_configs.get(mood.lower(), mood_configs['neutral'])

        try:
            # Get recommendations from Spotify
            recommendations = self.sp.recommendations(
                seed_genres=config['genres'][:3],
                limit=limit,
                **config['targets']
            )

            enhanced_recommendations = []
            for track in recommendations['tracks']:
                enhanced_recommendations.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album_name': track['album']['name'],
                    'album_art_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify']
                })

            return enhanced_recommendations
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    def compute_similarity(self, features1: Dict, features2: Dict) -> float:
        """Compute similarity between two songs based on their audio features"""
        try:
            v1 = np.array([features1.get(f, 0) * self.feature_weights[f] 
                          for f in self.feature_weights.keys()])
            v2 = np.array([features2.get(f, 0) * self.feature_weights[f] 
                          for f in self.feature_weights.keys()])
            return cosine_similarity(v1.reshape(1, -1), v2.reshape(1, -1))[0][0]
        except:
            return 0.0

    def get_similar_songs(self, track_id: str, limit: int = 6) -> List[Dict]:
        """Get similar songs based on audio features"""
        if not self.sp: return []
        
        try:
            base_features = self.get_audio_features(track_id)
            if not base_features:
                return []

            # Get a pool of recommendations
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
                        'album_art_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'similarity': float(similarity),
                        'external_url': track['external_urls']['spotify']
                    })

            # Sort by similarity and return top results
            similar_songs.sort(key=lambda x: x['similarity'], reverse=True)
            return similar_songs[:limit]
        except Exception as e:
            print(f"Error getting similar songs: {e}")
            return []
