import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.mood import mood_router
from src.api.spotify import spotify_router
from src.api.emotion import emotion_router
from src.api.music import music_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('moodify.log', encoding='utf-8')  # Output to file
    ]
)

app = FastAPI(
    title="Moodify",
    description="Personalized Music Recommendation Platform",
    version="0.1.0"
)

# CORS Middleware
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specific methods
    allow_headers=["Content-Type", "Authorization"],  # Specific headers
)

# Mount routers
app.include_router(emotion_router, prefix="/api/emotion", tags=["emotion"])
app.include_router(mood_router, prefix="/api/mood", tags=["mood"])
app.include_router(spotify_router, prefix="/api/spotify", tags=["spotify"])
app.include_router(music_router, prefix="/api/music", tags=["music"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Moodify - Your Emotional Music Companion",
        "status": "🎵 Listening to your mood 🎧"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
