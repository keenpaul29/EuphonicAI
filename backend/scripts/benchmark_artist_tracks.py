import asyncio
import time
import sys
import os
from unittest.mock import MagicMock
from typing import List

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Mock spotipy before importing the service
mock_spotipy = MagicMock()
sys.modules['spotipy'] = mock_spotipy
sys.modules['spotipy.oauth2'] = MagicMock()

# Import the service
from backend.src.services.spotify_service import get_tracks_from_artists, SpotifyTrack

# Setup mock Spotify client
class MockSpotify:
    def artist_top_tracks(self, artist_id, country='US'):
        # Simulate network latency
        time.sleep(0.1)
        return {
            'tracks': [
                {
                    'id': f'track_{artist_id}_{i}',
                    'name': f'Track {i} by {artist_id}',
                    'artists': [{'name': f'Artist {artist_id}'}],
                    'album': {
                        'name': f'Album by {artist_id}',
                        'images': [{'url': 'http://example.com/image.jpg'}]
                    },
                    'preview_url': 'http://example.com/preview.mp3',
                    'external_urls': {'spotify': 'http://spotify.com/track'},
                    'uri': f'spotify:track:{artist_id}_{i}'
                } for i in range(3)
            ]
        }

async def run_benchmark():
    spotify = MockSpotify()
    artist_ids = [f'artist_{i}' for i in range(10)]
    limit = 10
    mood = 'happy'

    print(f"Benchmarking get_tracks_from_artists with {len(artist_ids)} artists...")
    start_time = time.perf_counter()
    tracks = await get_tracks_from_artists(spotify, artist_ids, limit, mood)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Number of tracks returned: {len(tracks)}")
    return duration

if __name__ == "__main__":
    asyncio.run(run_benchmark())
