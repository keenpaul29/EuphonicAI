import sys
import os
import asyncio

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, 'backend', '.env'))

from backend.src.services.spotify_service import generate_mood_playlist

async def main():
    # Test different moods
    moods = ['happy', 'sad', 'neutral', 'angry', 'surprise', 'fear', 'disgust']
    
    for mood in moods:
        print(f"\n--- Generating {mood.upper()} Playlist ---")
        try:
            playlist = await generate_mood_playlist(mood, limit=5)
            
            # Print playlist details
            for i, track in enumerate(playlist, 1):
                print(f"{i}. Track ID: {track.id}, Name: {track.name}, Artist: {track.artists[0].name}")
        except Exception as e:
            print(f"Error generating {mood} playlist: {e}")

if __name__ == "__main__":
    asyncio.run(main())
