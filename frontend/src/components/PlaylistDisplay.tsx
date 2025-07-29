import React, { useState } from 'react';
import Image from 'next/image';
import { SpotifyTrack, Mood, EmotionScores } from '@/lib/api';

interface PlaylistDisplayProps {
  mood: Mood;
  playlist: SpotifyTrack[];
  confidence?: number;
  emotionScores?: EmotionScores;
  recommendedPlaylists?: {
    name: string;
    description?: string;
    image_url?: string;
    external_url: string;
    tracks: SpotifyTrack[];
  }[];
}

export default function PlaylistDisplay({ 
  mood, 
  playlist, 
  confidence,
  emotionScores,
  
}: PlaylistDisplayProps) {
  const [showAllEmotions, setShowAllEmotions] = useState(false);
  const [currentTrack, setCurrentTrack] = useState<SpotifyTrack | null>(null);

  const getMoodColor = (mood: Mood) => {
    const colors = {
      happy: 'bg-yellow-500',
      sad: 'bg-blue-500',
      angry: 'bg-red-500',
      neutral: 'bg-gray-500',
      surprised: 'bg-purple-500',
      fearful: 'bg-indigo-500',
      disgusted: 'bg-green-500'
    };
    return colors[mood] || 'bg-gray-500';
  };

  const getMoodEmoji = (mood: string) => {
    const emojis: { [key: string]: string } = {
      happy: '😊',
      sad: '😢',
      angry: '😠',
      neutral: '😐',
      surprised: '😮',
      fearful: '😨',
      disgusted: '🤢'
    };
    return emojis[mood] || '🎵';
  };

  const openInSpotify = (uri: string) => {
    window.open(`https://open.spotify.com/track/${uri.split(':')[2]}`, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Emotion Scores Section */}
      <div className="bg-white/50 dark:bg-black/50 rounded-xl p-4 space-y-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className={`w-16 h-16 rounded-xl ${getMoodColor(mood)} flex items-center justify-center`}>
              <span className="text-2xl" role="img" aria-label={mood}>
                {getMoodEmoji(mood)}
              </span>
            </div>
            <div>
              <h3 className="text-xl font-semibold capitalize">
                {mood} Mood
              </h3>
              {confidence && (
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Confidence: {(confidence * 100).toFixed(1)}%
                </p>
              )}
            </div>
          </div>
          <button
            onClick={() => setShowAllEmotions(!showAllEmotions)}
            className="text-sm px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            {showAllEmotions ? 'Hide Details' : 'Show Details'}
          </button>
        </div>

        {/* All Emotion Scores */}
        {showAllEmotions && emotionScores && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mt-4">
            {Object.entries(emotionScores).map(([emotion, score]) => (
              <div
                key={emotion}
                className="bg-white/50 dark:bg-gray-800/50 rounded-lg p-3 flex items-center space-x-3"
              >
                <span className="text-xl" role="img" aria-label={emotion}>
                  {getMoodEmoji(emotion)}
                </span>
                <div>
                  <p className="text-sm font-medium capitalize">{emotion}</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {(score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Song Recommendations Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Recommended Songs for Your Mood</h2>
        <div className="text-sm text-gray-600 dark:text-gray-400">
          {playlist.length} songs found
        </div>
      </div>

      {/* Featured Track Player (if a track is selected) */}
      {currentTrack && (
        <div className="bg-gradient-to-r from-purple-700/20 to-blue-700/20 rounded-xl p-6 shadow-lg">
          <div className="flex flex-col md:flex-row gap-6 items-center">
            {currentTrack.image_url ? (
              <div className="flex-shrink-0 w-48 h-48 relative rounded-lg overflow-hidden shadow-md">
                <Image
                  src={currentTrack.image_url}
                  alt={currentTrack.name}
                  fill
                  className="object-cover"
                />
              </div>
            ) : (
              <div className="flex-shrink-0 w-48 h-48 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                <span className="text-4xl">{getMoodEmoji(mood)}</span>
              </div>
            )}
            
            <div className="flex-grow space-y-4 text-center md:text-left">
              <div>
                <h3 className="text-2xl font-bold">{currentTrack.name}</h3>
                <p className="text-lg text-gray-700 dark:text-gray-300">
                  {currentTrack.artists.map(a => a.name).join(', ')}
                </p>
              </div>
              
              {currentTrack.preview_url ? (
                <div className="w-full max-w-md">
                  <audio
                    controls
                    autoPlay
                    className="w-full"
                  >
                    <source src={currentTrack.preview_url} type="audio/mpeg" />
                  </audio>
                </div>
              ) : (
                <p className="text-gray-500 italic">No preview available</p>
              )}
              
              <button
                onClick={() => openInSpotify(currentTrack.uri)}
                className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-full transition-colors flex items-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.669 11.538a.498.498 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686zm.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858zm.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288z"/>
                </svg>
                Open in Spotify
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Song Recommendations Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {playlist.map((track) => (
          <div
            key={track.id}
            className={`bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer ${currentTrack?.id === track.id ? 'ring-2 ring-purple-500 scale-102' : ''}`}
            onClick={() => setCurrentTrack(track)}
          >
            <div className="flex space-x-4">
              {track.image_url ? (
                <div className="flex-shrink-0">
                  <Image
                    src={track.image_url}
                    alt={track.name}
                    width={64}
                    height={64}
                    className="rounded-md"
                  />
                </div>
              ) : (
                <div className="flex-shrink-0 w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded-md flex items-center justify-center">
                  <span className="text-xl">{getMoodEmoji(mood)}</span>
                </div>
              )}
              <div className="flex-grow min-w-0">
                <h4 className="font-semibold truncate">{track.name}</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
                  {track.artists.map(a => a.name).join(', ')}
                </p>
                <div className="mt-2 flex items-center gap-2">
                  <button 
                    className="text-xs px-2 py-1 rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100"
                    onClick={(e) => {
                      e.stopPropagation();
                      openInSpotify(track.uri);
                    }}
                  >
                    Spotify
                  </button>
                  {track.preview_url && (
                    <button 
                      className="text-xs px-2 py-1 rounded-full bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-100"
                      onClick={(e) => {
                        e.stopPropagation();
                        setCurrentTrack(track);
                      }}
                    >
                      Preview
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Music Mood Tips */}
      <div className="mt-8 bg-white/50 dark:bg-gray-800/50 rounded-xl p-6">
        <h3 className="text-xl font-semibold mb-3">Why Music Affects Your Mood</h3>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Music has a profound effect on our emotions. The songs recommended above are specifically chosen to complement or enhance your current {mood} mood.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white/70 dark:bg-gray-700/70 p-4 rounded-lg">
            <h4 className="font-medium mb-2">Music Science</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Research shows that listening to music releases dopamine, the &quot;feel good&quot; neurochemical, which can improve your mood and reduce anxiety.
            </p>
          </div>
          <div className="bg-white/70 dark:bg-gray-700/70 p-4 rounded-lg">
            <h4 className="font-medium mb-2">Mood Enhancement</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {mood === 'happy' ? 'Upbeat songs can amplify your positive feelings and energy levels.' :
               mood === 'sad' ? 'Melancholic music can help process emotions and provide comfort.' :
               mood === 'angry' ? 'Energetic music can help channel and release tension.' :
               mood === 'neutral' ? 'Balanced music can help maintain focus and calm.' :
               mood === 'surprised' ? 'Dynamic music can complement your heightened awareness.' :
               mood === 'fearful' ? 'Soothing music can help reduce anxiety and stress.' :
               'Music tailored to your emotional state can provide a personalized listening experience.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
