# Moodify Backend

The backend server for Moodify - an AI-powered mood-based music recommendation platform that analyzes user emotions and provides personalized music recommendations.

## 🚀 Features

- **Emotion Analysis**: Processes images to detect user emotions using deep learning models
- **Mood-Based Recommendations**: Generates music recommendations based on detected emotions
- **Spotify Integration**: Connects with Spotify API to fetch and recommend music
- **RESTful API**: Well-structured API endpoints for frontend communication
- **Authentication**: Secure user authentication system

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Machine Learning**: TensorFlow, OpenCV, DeepFace
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL)
- **Authentication**: JWT with Python-Jose
- **External APIs**: Spotify API via Spotipy
- **Sentiment Analysis**: TextBlob

## 📋 Prerequisites

- Python 3.8+
- Pip (Python package manager)
- Spotify Developer Account (for API access)
- Virtual environment tool (recommended)

## 🔧 Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd moodify-new/backend
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the backend directory with the following variables:

```
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/spotify/callback

# Security
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///moodify.db
```

## 🚀 Running the Server

### Using the batch file (Windows)

```bash
start_server.bat
```

### Using Python directly

```bash
python main.py
```

### Using Uvicorn

```bash
uvicorn src.main:app --reload
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- **Health Check**: `GET /health`
- **Mood API**: `GET/POST /api/mood/*`
- **Spotify API**: `GET/POST /api/spotify/*`
- **Emotion API**: `GET/POST /api/emotion/*`

## 📁 Project Structure

```
backend/
├── .env                    # Environment variables
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
├── start_server.bat        # Windows startup script
├── emotion_model.h5        # Pre-trained emotion detection model
├── moodify.db              # SQLite database
├── datasets/               # Training and test datasets
├── scripts/                # Utility scripts
└── src/                    # Source code
    ├── api/                # API routes and endpoints
    │   ├── mood.py         # Mood-related endpoints
    │   ├── spotify.py      # Spotify integration endpoints
    │   ├── emotion.py      # Emotion detection endpoints
    │   └── ...
    ├── ml_models/          # Machine learning model implementations
    ├── services/           # Business logic and services
    └── utils/              # Utility functions and helpers
```

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

## 🔄 Development Workflow

1. Make changes to the codebase
2. Run tests to ensure functionality
3. Start the server with the reload flag for automatic reloading
4. Test API endpoints using Swagger UI or your frontend

## 🔒 Security Notes

- Never commit your `.env` file or any sensitive credentials
- The default SQLite database is suitable for development but consider PostgreSQL for production
- JWT tokens are used for authentication with configurable expiration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For any questions or issues, please open an issue in the repository or contact the project maintainers.
