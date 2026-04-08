'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Webcam from '@/components/Webcam';
import PlaylistDisplay from '@/components/PlaylistDisplay';
import TextInput from '@/components/TextInput';
import SearchBar from '@/components/SearchBar';
import HistoryDisplay from '@/components/HistoryDisplay';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Hero from '@/components/Hero';
import ApiClient, { EmotionDetectionResponse, TextAnalysisResponse, Mood } from '@/lib/api';
import { HistoryService } from '@/lib/history';
import { SignedIn, SignedOut, SignInButton, SignUpButton, useUser } from '@clerk/nextjs';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Camera, Type, History, RefreshCw, Share2, Search, Info, Music } from 'lucide-react';

export default function Home() {
  // const { user } = useUser();
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [detectedMood, setDetectedMood] = useState<EmotionDetectionResponse | TextAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('en');
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);
  const [lastRefreshTime, setLastRefreshTime] = useState<number>(Date.now());
  const [inputMode, setInputMode] = useState<'image' | 'text'>('image');
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<'discover' | 'search' | 'history'>('discover');

  // Fetch supported languages on mount
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const languages = await ApiClient.getSupportedLanguages();
        setSupportedLanguages(languages);
        if (languages.length > 0) {
          setSelectedLanguage(languages[0]);
        }
      } catch (error) {
        console.error('Failed to fetch languages:', error);
        setSupportedLanguages(['english']);
        setSelectedLanguage('english');
      }
    };
    fetchLanguages();
  }, []);

  // Refresh playlist logic
  useEffect(() => {
    const refreshPlaylist = async () => {
      const playlist = (detectedMood as any)?.playlist || (detectedMood as any)?.recommendations;
      if (playlist && playlist.length > 0) {
        // Only refresh if mood is present
        const moodStr = (detectedMood as any).emotion || (detectedMood as any).mood;
        if (!moodStr) return;

        try {
          setIsLoading(true);
          let response;
          if (inputMode === 'image' && capturedImage) {
            response = await ApiClient.detectEmotion(
              capturedImage.split(',')[1] || '',
              selectedLanguage === 'english' ? 'en' : selectedLanguage
            );
          } else if (inputMode === 'text') {
            response = await ApiClient.analyzeText(
              moodStr,
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

    let refreshInterval: NodeJS.Timeout | null = null;
    if (autoRefreshEnabled) {
      refreshInterval = setInterval(() => {
        setLastRefreshTime(Date.now());
      }, 5 * 60 * 1000);
    }

    // Use lastRefreshTime to trigger refresh
    if (lastRefreshTime > 0 && detectedMood) {
      refreshPlaylist();
    }

    return () => { if (refreshInterval) clearInterval(refreshInterval); };
  }, [lastRefreshTime]);

  const handleCapture = async (imageSrc: string) => {
    try {
      setIsLoading(true);
      setError(null);
      setCapturedImage(imageSrc);

      const response = await ApiClient.detectEmotion(
        imageSrc,
        selectedLanguage === 'english' ? 'en' : selectedLanguage
      );
      
      if (response && response.emotion) {
        setDetectedMood(response);
        setLastRefreshTime(Date.now());
        
        // Save to history
        HistoryService.addEntry({
          mood: response.emotion as Mood,
          confidence: response.confidence,
          tracks: (response as any).playlist || (response as any).recommendations || []
        });
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

        // Save to history
        HistoryService.addEntry({
          mood: (response as any).mood as Mood,
          tracks: (response as any).playlist || (response as any).recommendations || []
        });
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

  const handleShare = () => {
    if (detectedMood) {
      const mood = (detectedMood as any).emotion || (detectedMood as any).mood;
      const playlist = (detectedMood as any).playlist || (detectedMood as any).recommendations || [];
      const ids = playlist.map((t: any) => t.id);
      const url = `${window.location.origin}/share?mood=${encodeURIComponent(mood)}&ids=${encodeURIComponent(ids.join(','))}`;
      navigator.clipboard.writeText(url);
      alert('Share link copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
      <Navbar />
      
      <main className="flex-grow">
        <SignedOut>
          <Hero />
          
          <section id="features" className="py-24 bg-zinc-50 dark:bg-zinc-900/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
              <h2 className="text-3xl font-bold mb-16 text-zinc-900 dark:text-zinc-100">Everything you need to find your vibe</h2>
              <div className="grid md:grid-cols-3 gap-12">
                <div className="space-y-4">
                  <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center mx-auto text-white">
                    <Camera className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-bold">Emotion Sensing</h3>
                  <p className="text-zinc-500">Our advanced AI analyzes your facial expressions to detect subtle mood shifts.</p>
                </div>
                <div className="space-y-4">
                  <div className="w-12 h-12 bg-purple-600 rounded-xl flex items-center justify-center mx-auto text-white">
                    <Type className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-bold">Sentiment Analysis</h3>
                  <p className="text-zinc-500">Not feeling like using the camera? Just type your thoughts and let us handle the rest.</p>
                </div>
                <div className="space-y-4">
                  <div className="w-12 h-12 bg-pink-600 rounded-xl flex items-center justify-center mx-auto text-white">
                    <Sparkles className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-bold">Curated Playlists</h3>
                  <p className="text-zinc-500">Get instant access to millions of songs perfectly matched to your current state.</p>
                </div>
              </div>
            </div>
          </section>

          <div className="max-w-4xl mx-auto px-4 py-24 text-center">
            <div className="bg-indigo-600 rounded-3xl p-12 text-white shadow-2xl shadow-indigo-200 dark:shadow-none relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-10">
                <Music className="w-48 h-48" />
              </div>
              <h2 className="text-4xl font-bold mb-6 relative z-10">Ready to start your journey?</h2>
              <p className="text-indigo-100 text-lg mb-8 relative z-10">Join thousands of users who are discovering music in a whole new way.</p>
              <div className="flex flex-col sm:flex-row justify-center gap-4 relative z-10">
                <SignUpButton mode="modal">
                  <button className="bg-white text-indigo-600 px-8 py-3 rounded-xl font-bold hover:bg-zinc-100 transition-colors">
                    Sign Up for Free
                  </button>
                </SignUpButton>
                <SignInButton mode="modal">
                  <button className="bg-indigo-500 text-white border border-indigo-400 px-8 py-3 rounded-xl font-bold hover:bg-indigo-400 transition-colors">
                    Sign In
                  </button>
                </SignInButton>
              </div>
            </div>
          </div>
        </SignedOut>

        <SignedIn>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex flex-col lg:flex-row gap-8">
              {/* Sidebar Navigation */}
              <aside className="lg:w-64 space-y-2">
                <button
                  onClick={() => setActiveTab('discover')}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                    activeTab === 'discover' 
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none' 
                      : 'hover:bg-zinc-100 dark:hover:bg-zinc-900'
                  }`}
                >
                  <Sparkles className="w-5 h-5" />
                  <span className="font-medium">Discover</span>
                </button>
                <button
                  onClick={() => setActiveTab('search')}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                    activeTab === 'search' 
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none' 
                      : 'hover:bg-zinc-100 dark:hover:bg-zinc-900'
                  }`}
                >
                  <Search className="w-5 h-5" />
                  <span className="font-medium">Search</span>
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${
                    activeTab === 'history' 
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none' 
                      : 'hover:bg-zinc-100 dark:hover:bg-zinc-900'
                  }`}
                >
                  <History className="w-5 h-5" />
                  <span className="font-medium">History</span>
                </button>
                <div className="pt-8 pb-4 px-4">
                  <p className="text-xs font-bold text-zinc-400 uppercase tracking-widest">Preferences</p>
                </div>
                <div className="px-4 space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-zinc-500">Language</label>
                    <select
                      value={selectedLanguage}
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                      className="w-full bg-zinc-100 dark:bg-zinc-900 border-none rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-600"
                    >
                      {supportedLanguages.map((lang) => (
                        <option key={lang} value={lang}>
                          {lang.charAt(0).toUpperCase() + lang.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>
                  <label className="flex items-center space-x-3 cursor-pointer group">
                    <div className={`w-10 h-6 rounded-full relative transition-colors ${autoRefreshEnabled ? 'bg-indigo-600' : 'bg-zinc-300 dark:bg-zinc-700'}`}>
                      <input
                        type="checkbox"
                        className="hidden"
                        checked={autoRefreshEnabled}
                        onChange={(e) => setAutoRefreshEnabled(e.target.checked)}
                      />
                      <div className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${autoRefreshEnabled ? 'translate-x-4' : ''}`} />
                    </div>
                    <span className="text-sm font-medium text-zinc-600 dark:text-zinc-400">Auto-refresh</span>
                  </label>
                </div>
              </aside>

              {/* Main Content Area */}
              <div className="flex-grow space-y-8">
                {activeTab === 'discover' && (
                  <div className="grid lg:grid-cols-2 gap-8">
                    {/* Input Card */}
                    <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-6 shadow-sm">
                      <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold flex items-center gap-2">
                          <Camera className="w-5 h-5 text-indigo-600" />
                          Mood Input
                        </h2>
                        <div className="flex bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl">
                          <button
                            onClick={() => setInputMode('image')}
                            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                              inputMode === 'image' ? 'bg-white dark:bg-zinc-700 shadow-sm' : 'text-zinc-500 text-zinc-400'
                            }`}
                          >
                            Camera
                          </button>
                          <button
                            onClick={() => setInputMode('text')}
                            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                              inputMode === 'text' ? 'bg-white dark:bg-zinc-700 shadow-sm' : 'text-zinc-500 text-zinc-400'
                            }`}
                          >
                            Text
                          </button>
                        </div>
                      </div>

                      <div className="relative rounded-2xl overflow-hidden bg-zinc-50 dark:bg-zinc-950 aspect-video flex items-center justify-center border-2 border-dashed border-zinc-200 dark:border-zinc-800">
                        <AnimatePresence mode="wait">
                          {inputMode === 'image' ? (
                            <motion.div
                              key="camera"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              exit={{ opacity: 0 }}
                              className="w-full h-full"
                            >
                              {capturedImage ? (
                                <div className="relative w-full h-full">
                                  <Image
                                    src={capturedImage}
                                    alt="Captured"
                                    fill
                                    className="object-cover"
                                  />
                                  <button
                                    onClick={handleRetry}
                                    className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white/90 hover:bg-white text-zinc-900 px-6 py-2 rounded-full font-bold shadow-xl transition-all"
                                  >
                                    Retake
                                  </button>
                                </div>
                              ) : (
                                <Webcam
                                  onCapture={handleCapture}
                                  onError={setError}
                                  onReady={() => {}}
                                />
                              )}
                            </motion.div>
                          ) : (
                            <motion.div
                              key="text"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              exit={{ opacity: 0 }}
                              className="w-full p-6"
                            >
                              <TextInput
                                onSubmit={handleTextSubmit}
                                isLoading={isLoading}
                              />
                            </motion.div>
                          )}
                        </AnimatePresence>
                        
                        {isLoading && (
                          <div className="absolute inset-0 bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm flex items-center justify-center z-10">
                            <div className="flex flex-col items-center gap-4">
                              <RefreshCw className="w-8 h-8 text-indigo-600 animate-spin" />
                              <p className="font-medium animate-pulse">Analyzing your vibe...</p>
                            </div>
                          </div>
                        )}
                      </div>

                      {error && (
                        <div className="mt-4 p-4 bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400 rounded-xl text-sm border border-orange-100 dark:border-orange-900/30 flex items-start gap-3">
                          <Info className="w-5 h-5 flex-shrink-0 mt-0.5" />
                          <div>
                            <p className="font-semibold mb-1">Oops, we couldn&apos;t read your vibe.</p>
                            <p className="opacity-90">{error === 'Failed to fetch' ? 'Our servers are currently taking a breather. Please try again in a moment.' : error}</p>
                            <button
                              onClick={() => setInputMode('text')}
                              className="mt-2 text-orange-700 dark:text-orange-300 font-medium hover:underline focus:outline-none"
                            >
                              Try typing your mood instead?
                            </button>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Results Card */}
                    <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-6 shadow-sm flex flex-col">
                      <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold flex items-center gap-2">
                          <Music className="w-5 h-5 text-indigo-600" />
                          Your Playlist
                        </h2>
                        {detectedMood && (
                          <div className="flex gap-2">
                            <button
                              onClick={handleShare}
                              className="p-2 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition-colors text-zinc-500"
                              title="Share Playlist"
                            >
                              <Share2 className="w-5 h-5" />
                            </button>
                            <button
                              onClick={() => setLastRefreshTime(Date.now())}
                              className={`p-2 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition-colors text-zinc-500 ${isLoading ? 'animate-spin text-indigo-600' : ''}`}
                              title="Refresh"
                            >
                              <RefreshCw className="w-5 h-5" />
                            </button>
                          </div>
                        )}
                      </div>

                      <div className="flex-grow">
                        {detectedMood ? (
                          <PlaylistDisplay
                            mood={(detectedMood as any).emotion || (detectedMood as any).mood}
                            playlist={(detectedMood as any).playlist || (detectedMood as any).recommendations || []}
                            confidence={(detectedMood as any).confidence}
                            emotionScores={(detectedMood as any).emotion_scores}
                            recommendedPlaylists={(detectedMood as any).recommended_playlists}
                          />
                        ) : (
                          <div className="h-full flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-zinc-100 dark:border-zinc-800 rounded-2xl">
                            <div className="w-16 h-16 bg-zinc-50 dark:bg-zinc-800 rounded-full flex items-center justify-center mb-4 text-zinc-400">
                              <Music className="w-8 h-8" />
                            </div>
                            <h3 className="font-bold mb-2">No Playlist Yet</h3>
                            <p className="text-sm text-zinc-500 max-w-xs">
                              Use the camera or type how you feel to generate your first emotional playlist.
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'search' && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-8 shadow-sm"
                  >
                    <div className="mb-8">
                      <h2 className="text-2xl font-bold mb-2">Global Search</h2>
                      <p className="text-zinc-500">Find any song, artist, or album across the Spotify library.</p>
                    </div>
                    <SearchBar language={selectedLanguage} />
                  </motion.div>
                )}

                {activeTab === 'history' && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-8 shadow-sm"
                  >
                    <HistoryDisplay />
                  </motion.div>
                )}
              </div>
            </div>
          </div>
        </SignedIn>
      </main>

      <Footer />
    </div>
  );
}
