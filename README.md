# EuphonicAI: Emotional Music Companion 🎵🧠

## Overview
EuphonicAI is an innovative music recommendation platform that curates personalized playlists based on your current emotional state. By leveraging cutting-edge machine learning and multi-modal mood detection, we provide a unique, emotionally intelligent music experience.

## 🌟 Key Features
- **Mood Detection**
  - Facial Expression Analysis
  - Text Sentiment Analysis
- **Personalized Music Recommendations**
- **Spotify Integration**
- **User Authentication**

## 🛠 Tech Stack
- **Frontend**: Next.js 15, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Machine Learning**: DeepFace, TensorFlow
- **Authentication**: JWT
- **External APIs**: Spotify API

## 📦 Prerequisites
- Node.js 18+
- Python 3.11+
- Spotify Developer Account
- OpenAI API Key (optional)

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Connecting Frontend to Backend
The frontend is configured to connect to the backend at `http://localhost:8000` by default. You can change this by setting the `NEXT_PUBLIC_API_BASE_URL` environment variable in the frontend's `.env.local` file.

## 🔐 Environment Variables
Create `.env` files in both `frontend` and `backend` directories with:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `JWT_SECRET`

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License
MIT License

## 🎨 Created by
Puspal Paul - https://www.linkedin.com/in/puspal-paul
🎧 Music is the universal language that brings us together. 
