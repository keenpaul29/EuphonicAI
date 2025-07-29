import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from typing import List, NamedTuple, Union, Optional
import asyncio
import random
import logging
import traceback

from .schemas import SpotifyArtist

logger = logging.getLogger(__name__)

# Mood parameters for Spotify recommendations
mood_params = {
    'happy': {
        'target_energy': 0.8,
        'target_valence': 0.8,
        'target_tempo': 120,
        'min_danceability': 0.6,
        'seed_genres': ['pop', 'dance', 'happy']
    },
    'sad': {
        'target_energy': 0.4,
        'target_valence': 0.3,
        'target_tempo': 80,
        'max_danceability': 0.5,
        'seed_genres': ['sad', 'acoustic', 'piano']
    },
    'angry': {
        'target_energy': 0.9,
        'target_valence': 0.3,
        'target_tempo': 140,
        'min_danceability': 0.5,
        'seed_genres': ['rock', 'metal', 'punk']
    },
    'neutral': {
        'target_energy': 0.5,
        'target_valence': 0.5,
        'target_tempo': 100,
        'seed_genres': ['pop', 'indie', 'alternative']
    },
    'surprised': {
        'target_energy': 0.7,
        'target_valence': 0.6,
        'target_tempo': 110,
        'seed_genres': ['electronic', 'dance', 'pop']
    },
    'fearful': {
        'target_energy': 0.6,
        'target_valence': 0.2,
        'target_tempo': 90,
        'seed_genres': ['ambient', 'soundtrack', 'classical']
    },
    'disgusted': {
        'target_energy': 0.7,
        'target_valence': 0.3,
        'target_tempo': 120,
        'seed_genres': ['rock', 'alternative', 'indie']
    }
}

# Language configurations for Spotify recommendations
LANGUAGE_CONFIGS = {
    'english': {
        'market': 'US',
        'seed_artists': ['4gzpq5DPGxSnKTe4SA8HAU', '6eUKZXaKkcviH0Ku9w2n3V', '1uNFoZAHBGtllmzznpCI3s'],  # Taylor Swift, Coldplay, Justin Bieber
        'seed_tracks': ['2takcwOaAZWiXQijPHIx7B', '0VjIjW4GlUZAMYd2vXMi3b', '7qiZfU4dY1lWllzX7mPBI3'],  # Blinding Lights, Shape of You, Despacito
    },
    'hindi': {
        'market': 'IN',
        'seed_artists': ['4YRxDV8wJFPHPTeXepOstw', '0oOet2f43PA68X5RxKobEy', '1mYsTxnqsietFxj1OgoGbG'],  # Arijit Singh, A.R. Rahman, Shreya Ghoshal
        'seed_tracks': ['5wHqgVs1zikTUKsK01IUbV', '0KYP5Qe9ihAMvQzRVqrNxZ', '6rZVy6FIG7lSJQMFXHo12z'],  # Popular Hindi songs
    },
    'bangla': {
        'market': 'BD',
        'seed_artists': ['2oBG74gAecwNl8MXGgWbN5', '5f4QpKfy7ptCHwTqspnSJI', '6CMoXN9KmMvwEeEjcm3FC9'],  # Bangladeshi artists
        'seed_tracks': ['5Jm4w8jmPEBTLjI9vH4fXo', '0Xdk2wFVKQe8bfySLLjmtD', '1D3z6HTiQsNmZxjl7F7eoK'],  # Popular Bangla songs
    },
    'korean': {
        'market': 'KR',
        'seed_artists': ['3Nrfpe0tUJi4K4DXYWgMUX', '41MozSoPIsD1dJM0CLPjZF', '3HqSLMAZ3g3d5poNaI7GOU'],  # BTS, Blackpink, IU
        'seed_tracks': ['5KawlOMHjWeUjQtnuRs22c', '4TnjEaWOeW0eKTKIpJG0L2', '0WMGDXXMbHLGC7pVuJZ7xA'],  # Popular K-pop songs
    },
    'spanish': {
        'market': 'ES',
        'seed_artists': ['4q3ewBCX7sLwd24euuV69X', '1vyhD5VmyZ7KMfW5gqLgo5', '4VMYDCV2IEDYJArk749S6m'],  # J Balvin, J. Balvin, Bad Bunny
        'seed_tracks': ['6habFhsOp2NvshLv26DqMb', '0TK2YIli7K1leLovkQiNik', '0pqnGHJpmpxLKifKRmU6WP'],  # Popular Spanish songs
    },
    'japanese': {
        'market': 'JP',
        'seed_artists': ['2nvl0N9GwyX69RRBMEZ4OD', '5Vo1hnCRmCM6M4thZCInCj', '7k73EtZwoPs516ZxE72KsO'],  # Japanese artists
        'seed_tracks': ['3xdjjKMcMOFgo1eQrfbogM', '2QDyYdZyhlP2fp79KZX8Bi', '5ZRxxkirkxOBSjvLM4Avu3'],  # Popular Japanese songs
    },
    'french': {
        'market': 'FR',
        'seed_artists': ['5dsGFkBQ4IXabIXmaW5ajh', '4FpJcN1nPpEDMHWZxKHGYB', '5BvJzeQpmsdsFp4HGUYUEx'],  # French artists
        'seed_tracks': ['3V8FA5jZ51SscvmJPEkVhF', '75JFxkI2RXiU7L9VXzMkle', '2fuYIq7jrH9l0JH9Y7u8YF'],  # Popular French songs
    },
    'portuguese': {
        'market': 'BR',
        'seed_artists': ['1vCWHaC5f2uS3yhpwWbIA6', '7rXMvXRJAw4JnHr6oJ8lQm', '4gzpq5DPGxSnKTe4SA8HAU'],  # Brazilian artists
        'seed_tracks': ['6Qn5zhYkTa37e91HC1D7lb', '6PtNU1hHKkRxkfUdOswFj3', '3AJwUDP919kvQ9QcozQPxg'],  # Popular Portuguese songs
    }
}

class SpotifyTrack(NamedTuple):
    id: str
    name: str
    artists: List[SpotifyArtist]
    mood: str
    uri: str
    image_url: Optional[str] = None
    preview_url: Optional[str] = None

class Track(NamedTuple):
    id: str
    name: str
    artists: List[dict]
    mood: str
    preview_url: Optional[str] = None
    uri: Optional[str] = None

def get_spotify_client():
    """
    Initialize and return a Spotify client using environment variables.
    If authentication fails, return None.
    """
    try:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # Log credential presence without revealing actual values
        logger.info(f"Spotify credentials present: Client ID: {bool(client_id)}, Client Secret: {bool(client_secret)}")
        
        if not client_id or not client_secret:
            logger.error("Spotify credentials not found in environment variables")
            return None
            
        # Remove any whitespace that might have been included in the environment variables
        client_id = client_id.strip()
        client_secret = client_secret.strip()
        
        logger.info("Initializing Spotify client...")
        
        try:
            # Create the client credentials manager
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, 
                client_secret=client_secret
            )
            
            # Create the Spotify client
            client = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager,
                requests_timeout=15,  # Increased timeout
                retries=5             # Increased retries
            )
            
            # Test with a simple search query first
            logger.debug("Testing Spotify client with search query...")
            search_result = client.search(q='test', limit=1, type='track')
            if not search_result or 'tracks' not in search_result:
                logger.error("Spotify search test failed: Invalid response format")
                return None
                
            logger.info("Successfully initialized Spotify client")
            return client
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Spotify: {str(e)}")
            logger.error("Please check if your Spotify API credentials are valid")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            return None
        
    except Exception as e:
        logger.error(f"Failed to initialize Spotify client: {str(e)}")
        return None

async def generate_mood_playlist(mood: str, limit: int = 10) -> List[SpotifyTrack]:
    """
    Generate a playlist based on the given mood.
    
    :param mood: Emotional state to generate playlist for
    :param limit: Maximum number of tracks to return
    :return: List of SpotifyTrack objects
    """
    # Use asyncio to run the blocking Spotify API call
    loop = asyncio.get_event_loop()
    tracks = await loop.run_in_executor(None, _generate_mood_playlist, mood, limit)
    return [
        SpotifyTrack(
            id=track.id,
            name=track.name,
            artists=[SpotifyArtist(id=artist['id'], name=artist['name']) for artist in track.artists],
            mood=track.mood,
            uri=track.uri,
            image_url=None,
            preview_url=track.preview_url
        ) for track in tracks
    ]

def _generate_mood_playlist(mood: str, limit: int = 10) -> List[Track]:
    """
    Synchronous implementation of playlist generation.
    
    :param mood: Emotional state to generate playlist for
    :param limit: Maximum number of tracks to return
    :return: List of Track objects
    """
    # Use recommendations API to get mood-based tracks
    spotify_tracks = fetch_random_tracks(mood, limit)
    
    # Convert SpotifyTrack to Track objects
    tracks = [
        Track(
            id=track.id,
            name=track.name,
            artists=[{'id': artist.id, 'name': artist.name} for artist in track.artists],
            mood=track.mood,
            preview_url=track.preview_url,
            uri=track.uri
        ) for track in spotify_tracks
    ]
    
    return tracks[:limit]

def search_tracks(query: str, limit: int = 10) -> List[SpotifyTrack]:
    """
    Search Spotify tracks based on a query.
    
    :param query: Search query
    :param limit: Maximum number of tracks to return
    :return: List of SpotifyTrack objects
    """
    sp = get_spotify_client()
    
    results = sp.search(q=query, type='track', limit=limit)
    
    tracks = []
    for item in results['tracks']['items']:
        # Get album image URL
        image_url = None
        if item['album']['images']:
            if len(item['album']['images']) > 1:
                image_url = item['album']['images'][1]['url']
            else:
                image_url = item['album']['images'][0]['url']
                
        track = SpotifyTrack(
            id=item['id'],
            name=item['name'],
            artists=[
                SpotifyArtist(
                    id=artist['id'],
                    name=artist['name']
                ) for artist in item['artists']
            ],
            mood='unknown',
            uri=item['uri'],
            image_url=image_url,
            preview_url=item.get('preview_url')
        )
        tracks.append(track)
    
    return tracks

LANGUAGE_CONFIGS = {
    'english': {
        'market': 'US',
        'seed_artists': [
            '06HL4z0CvFAxyc27GXpf02',  # Taylor Swift
            '3TVXtAsR1Inumwj472S9r4',  # Drake
            '6eUKZXaKkcviH0Ku9w2n3V',  # Ed Sheeran
            '1uNFoZAHBGtllmzznpCI3s',  # Justin Bieber
            '66CXWjxzNUsdJxJ2JdwvnR',  # Ariana Grande
            '0du5cEVh5yTK9QJze8zA0C',  # Bruno Mars
            '3WrFJ7ztbogyGnTHbHJFl2',  # The Beatles
            '6M2wZ9GZgrQXHCFfjv46we',  # Dua Lipa
            '1Xyo4u8uXC1ZmMpatF05PJ',  # The Weeknd
            '0C8ZW7ezQVs4URX5aX7Kqx',  # Selena Gomez
        ],
        'seed_genres': ['pop', 'rock', 'hip-hop', 'r-n-b', 'indie']
    },
    'bangla': {
        'market': 'BD',
        'seed_artists': [
            '6PvvGcCY2XtUcuJyEZpyJW',  # Miles
            '1W9sHAhVyTEQDXVFRXk9yu',  # Shironamhin
            '5IEuvKZG8IHY7kMURADNhS',  # Cryptic Fate
            '4fEkbug6kZzzJ8eYX6Kbbp',  # Black
            '1uU7g3DNSbsu0QjSvDRqYE',  # Nemesis
        ],
        'seed_genres': ['rock', 'metal', 'folk-rock', 'alternative rock', 'progressive rock']
    },
    'hindi': {
        'market': 'IN',
        'seed_artists': [
            '1wRPtKGflJrBx9BmLsSwlU',  # Arijit Singh
            '4YRxDV8wJFPHPTeXepOstw',  # Jubin Nautiyal
            '5f4QpKfy7ptCHwTqspnSJI',  # Neha Kakkar
            '4WUepByoeqcedHoYhSNHRt',  # A.R. Rahman
            '0ZUKzU83dg0WfNmQR4FpXG',  # Shreya Ghoshal
        ]
    },
    'korean': {
        'market': 'KR',
        'seed_artists': [
            '3Nrfpe0tUJi4K4DXYWgMUX',  # BTS
            '41MozSoPIsD1dJM0CLPjZF',  # BLACKPINK
            '2AMysGXOe0zzZJMtH3Nizb',  # TWICE
            '4Uc4O8hMuU5QDzWHOJOAHD',  # EXO
            '4rCSDrYm1yT0VaLP78j66p',  # IU
        ]
    },
    'spanish': {
        'market': 'ES',
        'seed_artists': [
            '4q3ewBCX7sLwd24euuV69X',  # Bad Bunny
            '790FomKkXshlbRYZFtlgla',  # KAROL G
            '1vyhD5VmyZ7KMfW5gqLgo5',  # J Balvin
            '0EmeFodog0BfRgEMvOorUz',  # Shakira
            '1i8SpTcr7yvDOmTqDMmeu6',  # Enrique Iglesias
        ]
    },
    'japanese': {
        'market': 'JP',
        'seed_artists': [
            '2DlGxzQSjYe5N6G9nkYghR',  # YOASOBI
            '5Vo1hnCRmCM6M4thZQrkU2',  # Official HIGE DANdism
            '6zYpuEmxNFJwQQnUJfUVKi',  # LiSA
            '4nBPzFONLDzAcj8VDhtrDt',  # RADWIMPS
            '5qqxHdMGrAMwBTcgDIRpjK',  # ONE OK ROCK
        ]
    },
    'french': {
        'market': 'FR',
        'seed_artists': [
            '1URnnhqYAYcqOAhzQcmrQC',  # Daft Punk
            '4VMYDCV2IEDYJArk749S6m',  # David Guetta
            '3Q2j5apfdrbjsWcIXHVODZ',  # Christine and the Queens
            '4NHQUGzhtTLFvgF5SZesLK',  # Stromae
            '7GhRU8m1iMlMmPw7QLRUSR',  # Zaz
        ]
    },
    'portuguese': {
        'market': 'BR',
        'seed_artists': [
            '4NHQUGzhtTLFvgF5SZesLK',  # Anitta
            '7GuRQRmIpXcqkQeiv0qOhD',  # Caetano Veloso
            '4j7qoFhpRkdTxRsY4nRjfD',  # Marisa Monte
            '4JpKVNYnzcRt0un5mdDn0z',  # Seu Jorge
            '0oSGxhjXVqpkHRzMmBYNK6',  # Gilberto Gil
        ]
    }
}

mood_params = {
    'happy': {
        'target_valence': (0.7, 0.9),
        'target_energy': (0.7, 0.9),
        'target_tempo': (120, 140),
        'seed_genres': ['pop', 'rock', 'dance'],
        'bangla_keywords': ['khushi', 'anondo', 'happy', 'upbeat', 'dance']
    },
    'sad': {
        'target_valence': (0.1, 0.3),
        'target_energy': (0.2, 0.4),
        'target_tempo': (60, 90),
        'seed_genres': ['acoustic', 'sad', 'chill'],
        'bangla_keywords': ['koshto', 'bedona', 'sad', 'melancholy', 'emotional']
    },
    'angry': {
        'target_valence': (0.3, 0.5),
        'target_energy': (0.8, 1.0),
        'target_tempo': (140, 180),
        'seed_genres': ['rock', 'metal', 'punk'],
        'bangla_keywords': ['raag', 'josh', 'rock', 'metal', 'energetic']
    },
    'neutral': {
        'target_valence': (0.4, 0.6),
        'target_energy': (0.4, 0.6),
        'target_tempo': (90, 120),
        'seed_genres': ['pop', 'rock', 'alternative'],
        'bangla_keywords': ['modern', 'rock', 'pop', 'contemporary', 'fusion']
    }
}

async def find_bangla_artists(spotify: spotipy.Spotify, mood: str, limit: int = 5) -> List[str]:
    """
    Dynamically find Bangladeshi artists based on mood.
    Returns list of artist IDs.
    """
    artists = set()
    search_terms = [
        'bangladeshi rock',
        'bangla band',
        'bengali rock',
        f'bangladeshi {mood}',
        f'bangla {mood} band'
    ]
    
    try:
        for term in search_terms:
            results = spotify.search(q=term, type='artist', limit=limit, market='BD')
            for artist in results['artists']['items']:
                # Check if artist has sufficient popularity and followers
                if artist['popularity'] > 20 and artist['followers']['total'] > 1000:
                    artists.add(artist['id'])
                    
                    # Get related artists
                    try:
                        related = spotify.artist_related_artists(artist['id'])
                        for related_artist in related['artists'][:2]:  # Get top 2 related artists
                            if related_artist['popularity'] > 20:
                                artists.add(related_artist['id'])
                    except Exception as e:
                        logger.error(f"Error getting related artists: {str(e)}")
                        continue
                        
            if len(artists) >= limit:
                break
                
    except Exception as e:
        logger.error(f"Error searching for artists: {str(e)}")
        
    return list(artists)[:limit]

async def get_tracks_from_artists(spotify: spotipy.Spotify, artist_ids: List[str], limit: int, mood: str) -> List[SpotifyTrack]:
    """Get tracks from specific artists."""
    tracks = []
    for artist_id in artist_ids:
        try:
            # Get artist's top tracks
            results = spotify.artist_top_tracks(artist_id, country='BD')
            for item in results['tracks']:
                image_url = item['album']['images'][0]['url'] if item['album']['images'] else None
                track = SpotifyTrack(
                    id=item['id'],
                    name=item['name'],
                    artists=[
                        SpotifyArtist(
                            id=artist['id'],
                            name=artist['name']
                        ) for artist in item['artists']
                    ],
                    mood=mood,
                    uri=item['uri'],
                    image_url=image_url,
                    preview_url=item.get('preview_url')
                )
                tracks.append(track)
        except Exception as e:
            logger.error(f"Failed to get tracks for artist {artist_id}: {str(e)}")
            continue
    
    random.shuffle(tracks)
    return tracks[:limit]

async def search_bangla_tracks(spotify: spotipy.Spotify, keywords: List[str], limit: int, mood: str) -> List[SpotifyTrack]:
    """Search for Bangla tracks using keywords."""
    tracks = []
    for keyword in keywords:
        try:
            # Search with various combinations
            search_queries = [
                f"bangla {keyword} rock",
                f"bangladeshi {keyword}",
                f"bengali {keyword} music"
            ]
            
            for query in search_queries:
                results = spotify.search(q=query, type='track', limit=limit, market='BD')
                for item in results['tracks']['items']:
                    image_url = item['album']['images'][0]['url'] if item['album']['images'] else None
                    track = SpotifyTrack(
                        id=item['id'],
                        name=item['name'],
                        artists=[
                            SpotifyArtist(
                                id=artist['id'],
                                name=artist['name']
                            ) for artist in item['artists']
                        ],
                        mood=mood,
                        uri=item['uri'],
                        image_url=image_url,
                        preview_url=item.get('preview_url')
                    )
                    tracks.append(track)
        except Exception as e:
            logger.error(f"Failed to search with keyword {keyword}: {str(e)}")
            continue
    
    random.shuffle(tracks)
    return tracks[:limit]

async def get_recommendations(spotify: spotipy.Spotify, lang_config: dict, mood_config: dict, limit: int, mood: str) -> List[SpotifyTrack]:
    # Get tracks using Spotify's recommendation API.
    try:
        logger.info(f"Getting recommendations for mood: {mood}, language config: {lang_config['market']}")
        
        # Prepare parameters for the recommendations API
        params = {
            'limit': limit,
            'market': lang_config.get('market', 'US'),
        }
        
        # Add audio features based on mood
        for key, value in mood_config.items():
            if key != 'seed_genres':  # Handle seed_genres separately
                params[key] = value
                
        logger.debug(f"Audio feature parameters: {params}")
        
        # Prepare seed items (Spotify requires at least one seed type)
        seed_genres = mood_config.get('seed_genres', ['pop'])[:2]  # Use at most 2 seed genres
        seed_artists = []
        seed_tracks = []
        
        # Add seed artists if available
        if 'seed_artists' in lang_config and lang_config['seed_artists']:
            # Use 1-2 seed artists
            seed_artists = random.sample(lang_config['seed_artists'], 
                                       min(2, len(lang_config['seed_artists'])))
        
        # Add seed tracks if available
        if 'seed_tracks' in lang_config and lang_config['seed_tracks']:
            # Use 1-2 seed tracks
            seed_tracks = random.sample(lang_config['seed_tracks'], 
                                      min(2, len(lang_config['seed_tracks'])))
        
        # Ensure we don't exceed 5 seed items total (Spotify API limit)
        # and have at least one seed
        seed_count = len(seed_genres) + len(seed_artists) + len(seed_tracks)
        
        if seed_count > 5:
            # Prioritize different seed types based on availability
            if len(seed_genres) > 0 and len(seed_artists) > 0 and len(seed_tracks) > 0:
                # We have all three types, keep at least one of each
                remaining = 2
                seed_genres = seed_genres[:1]
                seed_artists = seed_artists[:1]
                seed_tracks = seed_tracks[:1]
                
                # Distribute remaining slots
                if remaining > 0 and len(lang_config.get('seed_tracks', [])) > 1:
                    seed_tracks.append(lang_config['seed_tracks'][1])
                    remaining -= 1
                if remaining > 0 and len(mood_config.get('seed_genres', [])) > 1:
                    seed_genres.append(mood_config['seed_genres'][1])
            else:
                # Reduce each category proportionally
                if len(seed_genres) > 2:
                    seed_genres = seed_genres[:2]
                if len(seed_artists) > 2:
                    seed_artists = seed_artists[:2]
                if len(seed_tracks) > 1:
                    seed_tracks = seed_tracks[:1]
        
        # If we have no seeds at all, use a default genre
        if len(seed_genres) + len(seed_artists) + len(seed_tracks) == 0:
            seed_genres = ['pop']
            
        # Add seeds to parameters
        if seed_genres:
            params['seed_genres'] = seed_genres
        if seed_artists:
            params['seed_artists'] = seed_artists
        if seed_tracks:
            params['seed_tracks'] = seed_tracks
            
        logger.info(f"Final recommendation parameters: seed_genres={seed_genres}, "
                   f"seed_artists={seed_artists}, seed_tracks={seed_tracks}")
            
        # Add audio feature targets
        if 'target_valence' in mood_config:
            params['target_valence'] = random.uniform(*mood_config['target_valence'])
        if 'target_energy' in mood_config:
            params['target_energy'] = random.uniform(*mood_config['target_energy'])
        # Make the API call
        logger.debug(f"Calling Spotify recommendations API with params: {params}")
        try:
            response = spotify.recommendations(**params)
            
            if not response or 'tracks' not in response:
                logger.error(f"Invalid response from Spotify recommendations API: {response}")
                return []
                
            # Log successful response
            logger.info(f"Received {len(response['tracks'])} tracks from Spotify recommendations API")
                
            tracks = []
            for item in response['tracks']:
                try:
                    # Extract image URL if available
                    image_url = None
                    if 'album' in item and 'images' in item['album'] and item['album']['images']:
                        image_url = item['album']['images'][0]['url']
                    
                    # Get preview URL
                    preview_url = item.get('preview_url')
                    
                    # If preview_url is None, try to get it from the track object
                    if preview_url is None and 'id' in item:
                        try:
                            track_info = spotify.track(item['id'])
                            if track_info and 'preview_url' in track_info:
                                preview_url = track_info['preview_url']
                        except Exception as e:
                            logger.warning(f"Failed to get track info for {item['id']}: {str(e)}")
                    
                    # Create SpotifyTrack object
                    track = SpotifyTrack(
                        id=item['id'],
                        name=item['name'],
                        artists=[
                            SpotifyArtist(
                                id=artist['id'],
                                name=artist['name']
                            ) for artist in item['artists']
                        ],
                        mood=mood,
                        uri=item['uri'],
                        image_url=image_url,
                        preview_url=preview_url
                    )
                    tracks.append(track)
                except Exception as e:
                    logger.warning(f"Failed to process track {item.get('id', 'unknown')}: {str(e)}")
                    continue
            
            # If we got fewer tracks than requested, try to get more with different parameters
            if len(tracks) < limit:
                logger.warning(f"Only got {len(tracks)} tracks, trying with different parameters")
                # Try with different seed genres
                alt_params = params.copy()
                alt_params['seed_genres'] = ['pop', 'rock', 'electronic'][:5 - len(params.get('seed_artists', [])) - len(params.get('seed_tracks', []))]
                if 'seed_artists' in alt_params:
                    del alt_params['seed_artists']
                if 'seed_tracks' in alt_params:
                    del alt_params['seed_tracks']
                
                try:
                    alt_response = spotify.recommendations(**alt_params)
                    if alt_response and 'tracks' in alt_response:
                        for item in alt_response['tracks']:
                            # Skip tracks we already have
                            if any(t.id == item['id'] for t in tracks):
                                continue
                                
                            try:
                                # Extract image URL if available
                                image_url = None
                                if 'album' in item and 'images' in item['album'] and item['album']['images']:
                                    image_url = item['album']['images'][0]['url']
                                
                                # Create SpotifyTrack object
                                track = SpotifyTrack(
                                    id=item['id'],
                                    name=item['name'],
                                    artists=[
                                        SpotifyArtist(
                                            id=artist['id'],
                                            name=artist['name']
                                        ) for artist in item['artists']
                                    ],
                                    mood=mood,
                                    uri=item['uri'],
                                    image_url=image_url,
                                    preview_url=item.get('preview_url')
                                )
                                tracks.append(track)
                                
                                # Stop if we have enough tracks
                                if len(tracks) >= limit:
                                    break
                            except Exception as e:
                                logger.warning(f"Failed to process alt track {item.get('id', 'unknown')}: {str(e)}")
                                continue
                except Exception as e:
                    logger.warning(f"Failed to get alternative recommendations: {str(e)}")
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error calling Spotify recommendations API: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            return []
        
    except Exception as e:
        logger.error(f"HTTP Error for GET to {spotify.recommendations.url} with Params: {params} returned {getattr(e, 'http_status', 'Unknown')} due to {getattr(e, 'msg', str(e))}")
        logger.error(f"Error getting recommendations: {str(e)}")
        return []

async def fetch_random_tracks(mood: str, limit: int = 10, language: str = None) -> List[SpotifyTrack]:
    """
    Fetch random tracks based on a mood and language using Spotify's recommendations API.
    If Spotify API fails, returns mock data.
    
    Args:
        mood (str): Mood to generate playlist for
        limit (int, optional): Maximum number of tracks to return. Defaults to 10.
        language (str, optional): Language preference for tracks. Defaults to None.
    
    Returns:
        List[SpotifyTrack]: List of tracks matching the mood
    """
    try:
        spotify = get_spotify_client()
        if not spotify:
            logger.warning("Spotify client not available, using mock data")
            return generate_mock_tracks(mood, limit)
            
        # Get language config
        lang_config = LANGUAGE_CONFIGS.get(language or 'english', LANGUAGE_CONFIGS['english'])
        mood_config = mood_params.get(mood.lower(), mood_params['neutral'])
        
        # Get tracks using Spotify's recommendation API
        try:
            # Directly call the async function and await it
            tracks = await get_recommendations(
                spotify,
                lang_config,
                mood_config,
                limit,
                mood
            )
            
            if tracks and len(tracks) > 0:
                return tracks
            else:
                logger.warning("Spotify returned no tracks, using mock data")
                return generate_mock_tracks(mood, limit)
                
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            logger.error(traceback.format_exc())
            return generate_mock_tracks(mood, limit)
        
    except Exception as e:
        logger.error(f"Error fetching random tracks: {str(e)}")
        logger.error(traceback.format_exc())
        return generate_mock_tracks(mood, limit)

def get_supported_languages() -> List[str]:
    """
    Get list of supported languages for song recommendations.
    
    :return: List of supported language codes
    """
    return list(LANGUAGE_CONFIGS.keys())

def validate_language(language: str | None) -> str | None:
    """
    Validate and normalize language input.
    
    :param language: Input language string
    :return: Normalized language or None if not supported
    """
    if not language:
        logger.info("No language provided, returning None")
        return None
    
    # Normalize language input
    language_map = {
        'eng': 'english',
        'en': 'english',
        'hin': 'hindi',
        'hi': 'hindi',
        'ben': 'bangla',
        'bn': 'bangla',
        'kor': 'korean',
        'ko': 'korean',
        'spa': 'spanish',
        'es': 'spanish',
        'jpn': 'japanese',
        'ja': 'japanese',
        'fra': 'french',
        'fr': 'french',
        'por': 'portuguese',
        'pt': 'portuguese'
    }
    
    # Try exact match first
    normalized_language = language.lower()
    if normalized_language in LANGUAGE_CONFIGS:
        logger.info(f"Language '{language}' matched exactly: {normalized_language}")
        return normalized_language
    
    # Try language code mapping
    mapped_language = language_map.get(normalized_language)
    if mapped_language and mapped_language in LANGUAGE_CONFIGS:
        logger.info(f"Language '{language}' mapped to: {mapped_language}")
        return mapped_language
    
    logger.warning(f"Unsupported language: {language}")
    return None

def generate_mock_tracks(mood: str, limit: int = 10) -> List[SpotifyTrack]:
    """
    Generate mock tracks for when Spotify API is unavailable.
    
    Args:
        mood (str): Mood to generate playlist for
        limit (int): Number of tracks to generate
        
    Returns:
        List[SpotifyTrack]: List of mock tracks
    """
    logger.info(f"Generating {limit} mock tracks for mood: {mood}")
    
    # Define mock artists for different moods
    mock_artists = {
        'happy': [
            {'id': 'happy1', 'name': 'Happy Vibes'},
            {'id': 'happy2', 'name': 'Sunshine Band'},
            {'id': 'happy3', 'name': 'Joyful Noise'}
        ],
        'sad': [
            {'id': 'sad1', 'name': 'Melancholy'},
            {'id': 'sad2', 'name': 'Blue Notes'},
            {'id': 'sad3', 'name': 'Teardrops'}
        ],
        'angry': [
            {'id': 'angry1', 'name': 'Rage Machine'},
            {'id': 'angry2', 'name': 'Fury'},
            {'id': 'angry3', 'name': 'Thunder'}
        ],
        'neutral': [
            {'id': 'neutral1', 'name': 'Ambient Sounds'},
            {'id': 'neutral2', 'name': 'Background Noise'},
            {'id': 'neutral3', 'name': 'Elevator Music'}
        ],
        'surprised': [
            {'id': 'surprised1', 'name': 'Unexpected'},
            {'id': 'surprised2', 'name': 'Shock Wave'},
            {'id': 'surprised3', 'name': 'Astonished'}
        ],
        'fearful': [
            {'id': 'fearful1', 'name': 'Haunted'},
            {'id': 'fearful2', 'name': 'Shadows'},
            {'id': 'fearful3', 'name': 'Suspense'}
        ],
        'disgusted': [
            {'id': 'disgusted1', 'name': 'Revulsion'},
            {'id': 'disgusted2', 'name': 'Distaste'},
            {'id': 'disgusted3', 'name': 'Aversion'}
        ]
    }
    
    # Use neutral as fallback for any unrecognized mood
    mood_key = mood.lower()
    if mood_key not in mock_artists:
        mood_key = 'neutral'
        
    # Song titles for different moods
    mock_titles = {
        'happy': [
            'Dancing in the Sun', 'Celebration', 'Good Vibes Only', 'Happy Day',
            'Upbeat Rhythm', 'Joyful Morning', 'Sunshine Smile', 'Positive Energy',
            'Bright Future', 'Cheerful Melody', 'Uplifting', 'Radiant Joy'
        ],
        'sad': [
            'Rainy Day', 'Lost Love', 'Melancholy Blues', 'Teardrops',
            'Lonely Night', 'Fading Memories', 'Silent Tears', 'Empty Room',
            'Broken Heart', 'Goodbye', 'Missing You', 'Distant Echo'
        ],
        'angry': [
            'Rage Against', 'Fury', 'Boiling Point', 'Breaking Point',
            'Explosive', 'Burning Inside', 'Unleashed', 'Shattered',
            'Eruption', 'Fierce', 'Intensity', 'Outburst'
        ],
        'neutral': [
            'Background Noise', 'Ambient Sounds', 'Middle Ground', 'Balance',
            'Harmony', 'Equilibrium', 'Steady Flow', 'Even Keel',
            'Moderate', 'Balanced', 'Centered', 'Stable'
        ],
        'surprised': [
            'Unexpected Turn', 'Sudden Shift', 'Plot Twist', 'Revelation',
            'Astonished', 'Shock Wave', 'Jaw Dropper', 'Surprise Party',
            'Out of Nowhere', 'Unforeseen', 'Startled', 'Amazed'
        ],
        'fearful': [
            'Shadows', 'Haunted', 'Dark Corner', 'Suspense',
            'Creeping Fear', 'Tension Rising', 'Apprehension', 'Dread',
            'Foreboding', 'Anxious Mind', 'Unease', 'Trepidation'
        ],
        'disgusted': [
            'Revulsion', 'Distaste', 'Aversion', 'Repulsed',
            'Turned Off', 'Nauseated', 'Repelled', 'Grossed Out',
            'Revolting', 'Sickening', 'Offensive', 'Unpalatable'
        ]
    }
    
    # Generate mock tracks
    tracks = []
    for i in range(limit):
        # Select random artist from the mood's artist list
        artist = random.choice(mock_artists[mood_key])
        artist_obj = SpotifyArtist(id=artist['id'], name=artist['name'])
        
        # Select random title from the mood's title list
        title = random.choice(mock_titles[mood_key])
        
        # Create a unique ID
        track_id = f"mock_{mood_key}_{i}_{random.randint(1000, 9999)}"
        
        # Create the track
        track = SpotifyTrack(
            id=track_id,
            name=f"{title} {i+1}",
            artists=[artist_obj],
            mood=mood_key,
            uri=f"spotify:track:{track_id}",
            image_url=None,
            preview_url=None
        )
        
        tracks.append(track)
    
    logger.info(f"Generated {len(tracks)} mock tracks successfully")
    return tracks

# Export the functions and classes
__all__ = ['Track', 'SpotifyTrack', 'generate_mood_playlist', 'search_tracks', 'fetch_random_tracks', 'get_supported_languages', 'validate_language', 'generate_mock_tracks']
