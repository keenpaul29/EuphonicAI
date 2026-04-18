import asyncio
import time
import sys
from unittest.mock import MagicMock

# Structure the mocking before importing the service
mock_spotipy = MagicMock()
sys.modules['spotipy'] = mock_spotipy
sys.modules['spotipy.oauth2'] = MagicMock()

from backend.src.services.spotify_service import get_tracks_from_artists

# Mock Spotify client that simulates network latency
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

def test_get_tracks_from_artists_performance():
    spotify = MockSpotify()
    artist_ids = [f'artist_{i}' for i in range(10)]
    limit = 10
    mood = 'happy'

    start_time = time.perf_counter()
    tracks = asyncio.run(get_tracks_from_artists(spotify, artist_ids, limit, mood))
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"\nPerformance test duration: {duration:.4f} seconds")

    # Assertions
    assert len(tracks) <= limit
    # With 10 artists, 0.1s latency and Semaphore(5):
    # It should take approximately 0.2s.
    assert duration < 0.5

if __name__ == "__main__":
    test_get_tracks_from_artists_performance()
