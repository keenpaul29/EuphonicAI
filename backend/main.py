import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from src.api.mood import mood_router
from src.api.spotify import spotify_router
from src.api.emotion import emotion_router

# Create FastAPI app
app = FastAPI(
    title="Moodify",
    description="AI-powered mood-based music recommendation platform",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend development server
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
    # Add your production frontend URL here when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mood_router, prefix="/api/mood", tags=["Mood"])
app.include_router(spotify_router, prefix="/api/spotify", tags=["Spotify"])
app.include_router(emotion_router, prefix="/api/emotion", tags=["Emotion"])

# Optional: Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Optional: Configure startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("Application is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")

# This allows running the app directly with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
