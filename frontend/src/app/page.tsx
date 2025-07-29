'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Webcam from '@/components/Webcam';
import PlaylistDisplay from '@/components/PlaylistDisplay';
import TextInput from '@/components/TextInput';
import ApiClient, { EmotionDetectionResponse, TextAnalysisResponse, Mood } from '@/lib/api';

export default function Home() {
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [detectedMood, setDetectedMood] = useState<EmotionDetectionResponse | TextAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isWebcamReady, setIsWebcamReady] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('en');
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);
  const [lastRefreshTime, setLastRefreshTime] = useState<number>(Date.now());
  const [inputMode, setInputMode] = useState<'image' | 'text'>('image');

  // Fetch supported languages on mount
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const languages = await ApiClient.getSupportedLanguages();
        setSupportedLanguages(languages);
        // Set default language if available
        if (languages.length > 0) {
          setSelectedLanguage(languages[0]);
        }
      } catch (error) {
        console.error('Failed to fetch languages:', error);
        setSupportedLanguages(['english']); // Fallback to English
        setSelectedLanguage('english');
      }
    };
    fetchLanguages();
  }, []);

  // Refresh playlist when mood is detected or page is loaded
  useEffect(() => {
    const refreshPlaylist = async () => {
      if (detectedMood?.emotion || detectedMood?.mood) {
        try {
          setIsLoading(true);
          let response;
          if (inputMode === 'image') {
            response = await ApiClient.detectEmotion(
              capturedImage?.split(',')[1] || '',
              selectedLanguage === 'english' ? 'en' : selectedLanguage
            );
          } else {
            response = await ApiClient.analyzeText(
              typeof detectedMood.mood === 'string' ? detectedMood.mood : detectedMood.emotion,
              selectedLanguage === 'english' ? 'en' : selectedLanguage
            );
          }
          if (response) {
            setDetectedMood(response);
          }
        } catch (err) {
          console.error('Error refreshing playlist:', err);
        } finally {
          setIsLoading(false);
        }
      }
    };

    // Set up auto-refresh interval (every 5 minutes)
    const refreshInterval = setInterval(() => {
      setLastRefreshTime(Date.now());
    }, 5 * 60 * 1000);

    // Only refresh when the lastRefreshTime changes manually (from button click)
    // or when the language changes
    if (lastRefreshTime > 0) {
      refreshPlaylist();
    }

    // Cleanup interval on unmount
    return () => clearInterval(refreshInterval);
  }, [lastRefreshTime, selectedLanguage]);

  const handleCapture = async (imageSrc: string) => {
    try {
      setIsLoading(true);
      setError(null);
      setCapturedImage(imageSrc);

      // Send the full data URL
      const response = await ApiClient.detectEmotion(
        imageSrc,
        selectedLanguage === 'english' ? 'en' : selectedLanguage
      );
      
      if (response && response.emotion) {
        setDetectedMood(response);
        // Trigger a refresh when mood is detected
        setLastRefreshTime(Date.now());
      } else {
        throw new Error('Invalid response from emotion detection');
      }
    } catch (err) {
      console.error('Error detecting mood:', err);
      setError(err instanceof Error ? err.message : 'Failed to detect mood');
      setCapturedImage(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextSubmit = async (text: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await ApiClient.analyzeText(
        text,
        selectedLanguage === 'english' ? 'en' : selectedLanguage
      );
      
      if (response) {
        setDetectedMood(response);
        setLastRefreshTime(Date.now());
      }
    } catch (err) {
      console.error('Error analyzing text:', err);
      setError(err instanceof Error ? err.message : 'Failed to analyze text');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setCapturedImage(null);
    setDetectedMood(null);
    setError(null);
  };

  const handleRefreshClick = () => {
    setLastRefreshTime(Date.now());
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-400 dark:to-indigo-400">
            EuphonicAI
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Discover music that matches your mood using AI
          </p>
        </header>

        {/* Main Content */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Camera Section */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl space-y-6">
            <div className="space-y-2">
              <h2 className="text-2xl font-semibold">Capture Your Mood</h2>
              <p className="text-gray-600 dark:text-gray-400">
                Take a photo or type how you feel to analyze your emotional state
              </p>
            </div>

            {/* Language Selection */}
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full p-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {supportedLanguages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang.charAt(0).toUpperCase() + lang.slice(1)}
                </option>
              ))}
            </select>

            {/* Input Mode Selection */}
            <div className="flex justify-center space-x-4 mb-8">
              <button
                onClick={() => setInputMode('image')}
                className={`px-4 py-2 rounded-md ${
                  inputMode === 'image' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Use Camera
              </button>
              <button
                onClick={() => setInputMode('text')}
                className={`px-4 py-2 rounded-md ${
                  inputMode === 'text' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Use Text
              </button>
            </div>

            {/* Webcam/Captured Image */}
            {inputMode === 'image' ? (
              <div className="relative">
                {capturedImage ? (
                  <div className="relative rounded-2xl overflow-hidden">
                    <Image
                      src={capturedImage}
                      alt="Captured"
                      width={1280}
                      height={720}
                      className="w-full aspect-video object-cover"
                    />
                    <button
                      onClick={handleRetry}
                      className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white/90 hover:bg-white dark:bg-black/90 dark:hover:bg-black text-black dark:text-white px-6 py-2 rounded-full shadow-lg transition-all duration-200"
                    >
                      Retake Photo
                    </button>
                  </div>
                ) : (
                  <Webcam
                    onCapture={handleCapture}
                    onError={setError}
                    onReady={() => setIsWebcamReady(true)}
                  />
                )}
              </div>
            ) : (
              <TextInput
                onSubmit={handleTextSubmit}
                isLoading={isLoading}
              />
            )}

            {/* Error Display */}
            {error && (
              <div className="p-4 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-xl">
                {error}
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className="absolute inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center">
                <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-xl">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                </div>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl">
            {detectedMood && detectedMood.playlist && detectedMood.playlist.length > 0 ? (
              <div className="w-full max-w-4xl mx-auto mt-8">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-2xl font-bold">
                    {(detectedMood as EmotionDetectionResponse).emotion ? (detectedMood as EmotionDetectionResponse).emotion.charAt(0).toUpperCase() + (detectedMood as EmotionDetectionResponse).emotion.slice(1) : (detectedMood as TextAnalysisResponse).mood.charAt(0).toUpperCase() + (detectedMood as TextAnalysisResponse).mood.slice(1)} Mood Playlist
                  </h2>
                  <button
                    onClick={handleRefreshClick}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Refreshing...' : 'Refresh Playlist'}
                  </button>
                </div>
                <PlaylistDisplay
                  mood={(detectedMood as EmotionDetectionResponse).emotion ? (detectedMood as EmotionDetectionResponse).emotion : (detectedMood as TextAnalysisResponse).mood}
                  playlist={detectedMood.playlist}
                  confidence={(detectedMood as EmotionDetectionResponse).confidence}
                  emotionScores={(detectedMood as EmotionDetectionResponse).emotion_scores}
                  recommendedPlaylists={(detectedMood as EmotionDetectionResponse).recommended_playlists}
                />
              </div>
            ) : detectedMood ? (
              <div className="w-full max-w-4xl mx-auto mt-8 p-4 bg-white/80 dark:bg-gray-800/80 rounded-lg text-center">
                <p className="text-lg text-gray-600 dark:text-gray-300">
                  No songs found for the current mood. Please try refreshing or selecting a different language.
                </p>
                <button
                  onClick={handleRefreshClick}
                  className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                  disabled={isLoading}
                >
                  {isLoading ? 'Refreshing...' : 'Try Again'}
                </button>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </main>
  );
}
