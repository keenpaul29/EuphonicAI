import { useState, useEffect, useCallback } from 'react';
import ApiClient, { DetectionResponse, getMoodFromDetection, getPlaylistFromDetection, Mood } from '@/lib/api';
import { HistoryService } from '@/lib/history';

export const useMoodifyState = () => {
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [detectedMood, setDetectedMood] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('en');
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);
  const [lastRefreshTime, setLastRefreshTime] = useState<number>(Date.now());
  const [inputMode, setInputMode] = useState<'image' | 'text'>('image');
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<'discover' | 'search' | 'history'>('discover');

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

  const refreshPlaylist = useCallback(async () => {
    const playlist = getPlaylistFromDetection(detectedMood);
    if (playlist && playlist.length > 0) {
      const moodStr = getMoodFromDetection(detectedMood);
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
  }, [detectedMood, inputMode, capturedImage, selectedLanguage]);

  useEffect(() => {
    let refreshInterval: NodeJS.Timeout | null = null;
    if (autoRefreshEnabled) {
      refreshInterval = setInterval(() => {
        setLastRefreshTime(Date.now());
      }, 5 * 60 * 1000);
    }

    if (lastRefreshTime > 0 && detectedMood) {
      refreshPlaylist();
    }

    return () => { if (refreshInterval) clearInterval(refreshInterval); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastRefreshTime, autoRefreshEnabled]);

  const handleCapture = async (imageSrc: string) => {
    try {
      setIsLoading(true);
      setError(null);
      setCapturedImage(imageSrc);

      const response = await ApiClient.detectEmotion(
        imageSrc,
        selectedLanguage === 'english' ? 'en' : selectedLanguage
      );

      if (response && getMoodFromDetection(response)) {
        setDetectedMood(response);
        setLastRefreshTime(Date.now());

        HistoryService.addEntry({
          mood: getMoodFromDetection(response) as Mood,
          confidence: (response as any).confidence,
          tracks: getPlaylistFromDetection(response)
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

        HistoryService.addEntry({
          mood: getMoodFromDetection(response) as Mood,
          tracks: getPlaylistFromDetection(response)
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

  return {
    state: {
      capturedImage,
      detectedMood,
      error,
      isLoading,
      selectedLanguage,
      supportedLanguages,
      inputMode,
      autoRefreshEnabled,
      activeTab,
      lastRefreshTime,
    },
    actions: {
      setCapturedImage,
      setDetectedMood,
      setError,
      setIsLoading,
      setSelectedLanguage,
      setInputMode,
      setAutoRefreshEnabled,
      setActiveTab,
      setLastRefreshTime,
      handleCapture,
      handleTextSubmit,
      handleRetry,
    }
  };
};