import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Types
export type Mood = 'happy' | 'sad' | 'angry' | 'neutral' | 'surprised' | 'fearful' | 'disgusted';

export interface EmotionScores {
  [key: string]: number;  // Maps emotion name to confidence score
}

export interface SpotifyArtist {
  id: string;
  name: string;
}

export interface SpotifyTrack {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  mood: string;
  uri: string;
  image_url?: string;
  preview_url?: string;
}

export interface EmotionDetectionResponse {
  emotion: Mood;
  confidence: number;
  emotion_scores: EmotionScores;
  playlist: SpotifyTrack[];
  recommended_playlists?: {
    name: string;
    description?: string;
    image_url?: string;
    external_url: string;
    tracks: SpotifyTrack[];
  }[];
}

export interface SentimentScores {
  neg: number;
  neu: number;
  pos: number;
  compound: number;
}

export interface TextAnalysisResponse {
  sentiment_scores: SentimentScores;
  mood: Mood;
  recommendations: SpotifyTrack[];
}

// API Client
class ApiClient {
  private static client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  static async detectEmotion(imageBase64: string, language?: string): Promise<EmotionDetectionResponse> {
    try {
      console.log('Detecting emotion with language:', language);
      // Handle data URL format
      const base64Data = imageBase64.includes('base64,') 
        ? imageBase64.split('base64,')[1] 
        : imageBase64;

      const response = await this.client.post<EmotionDetectionResponse>('/api/emotion/detect', {
        image: base64Data,
        language,
        include_playlists: true, // Request playlist recommendations
      });
      console.log('Emotion detection response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error detecting emotion:', error);
      if (axios.isAxiosError(error)) {
        console.error('Response data:', error.response?.data);
        throw new Error(error.response?.data?.detail || 'Failed to detect emotion');
      }
      throw error;
    }
  }

  static async getSupportedLanguages(): Promise<string[]> {
    try {
      const response = await this.client.get<string[]>('/api/emotion/languages');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch supported languages:', error);
      return ['english']; // Fallback to English
    }
  }

  static async analyzeText(text: string, language?: string, limit: number = 10): Promise<TextAnalysisResponse> {
    try {
      console.log('Analyzing text with language:', language);
      const response = await this.client.post<TextAnalysisResponse>('/api/mood/text/analyze', {
        text,
        language,
        limit,
      });
      console.log('Text analysis response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error analyzing text:', error);
      if (axios.isAxiosError(error)) {
        console.error('Response data:', error.response?.data);
        throw new Error(error.response?.data?.detail || 'Failed to analyze text');
      }
      throw error;
    }
  }

  static async getSpotifyPlaylists(mood: Mood): Promise<SpotifyTrack[]> {
    try {
      const response = await this.client.get(`/api/spotify/playlists`, {
        params: { mood }
      });
      return response.data.tracks;
    } catch (error) {
      console.error('Error fetching Spotify playlists:', error);
      return [];
    }
  }
}

export default ApiClient;
