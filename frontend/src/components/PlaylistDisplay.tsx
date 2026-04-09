import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { SpotifyTrack, Mood, EmotionScores } from '@/lib/api';
import ApiClient from '@/lib/api';
import { Play, Pause, Heart, ExternalLink, Music, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

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
  recommendedPlaylists,
}: PlaylistDisplayProps) {
  const [favorites, setFavorites] = useState<SpotifyTrack[]>([]);
  const [playingTrack, setPlayingTrack] = useState<string | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    return () => {
      if (audio) {
        audio.pause();
        audio.src = '';
      }
    };
  }, [audio]);

  const togglePlay = (track: SpotifyTrack) => {
    if (!track.preview_url) return;

    if (playingTrack === track.id) {
      audio?.pause();
      setPlayingTrack(null);
    } else {
      if (audio) {
        audio.pause();
      }
      const newAudio = new Audio(track.preview_url);
      newAudio.play();
      newAudio.onended = () => setPlayingTrack(null);
      setAudio(newAudio);
      setPlayingTrack(track.id);
    }
  };

  useEffect(() => {
    try {
      const raw = localStorage.getItem('favorites');
      setFavorites(raw ? JSON.parse(raw) : []);
    } catch {}
  }, []);

  const isFavorite = (id: string) => favorites.some(t => t.id === id);
  const toggleFavorite = (track: SpotifyTrack) => {
    const next = isFavorite(track.id)
      ? favorites.filter(t => t.id !== track.id)
      : [...favorites, track];
    setFavorites(next);
    try { localStorage.setItem('favorites', JSON.stringify(next)); } catch {}
  };

  const getMoodConfig = (mood: string) => {
    const configs: { [key: string]: { emoji: string; color: string; gradient: string } } = {
      happy: {
        emoji: '😊',
        color: 'text-yellow-500',
        gradient: 'from-yellow-400 to-orange-500'
      },
      sad: {
        emoji: '😢',
        color: 'text-blue-500',
        gradient: 'from-blue-400 to-indigo-500'
      },
      angry: {
        emoji: '😠',
        color: 'text-red-500',
        gradient: 'from-red-400 to-pink-500'
      },
      neutral: {
        emoji: '😐',
        color: 'text-zinc-500',
        gradient: 'from-zinc-400 to-slate-500'
      },
      surprised: {
        emoji: '😮',
        color: 'text-purple-500',
        gradient: 'from-purple-400 to-fuchsia-500'
      },
      fearful: {
        emoji: '😨',
        color: 'text-indigo-500',
        gradient: 'from-indigo-400 to-purple-500'
      },
      disgusted: {
        emoji: '🤢',
        color: 'text-green-500',
        gradient: 'from-green-400 to-emerald-500'
      }
    };
    return configs[mood] || {
      emoji: '🎵',
      color: 'text-indigo-500',
      gradient: 'from-indigo-400 to-purple-500'
    };
  };

  const config = getMoodConfig(mood);

  return (
    <div className="space-y-8">
      {/* Enhanced Header Info */}
      <div className="relative overflow-hidden rounded-3xl p-6 border border-zinc-200 dark:border-zinc-800">
        <div className={`absolute inset-0 bg-gradient-to-br ${config.gradient} opacity-5 dark:opacity-10`} />

        <div className="relative flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className={`w-16 h-16 rounded-2xl bg-white dark:bg-zinc-800 shadow-xl flex items-center justify-center text-3xl`}
            >
              {config.emoji}
            </motion.div>
            <div>
              <h3 className="text-2xl font-black capitalize tracking-tight">{mood} Vibe</h3>
              <p className="text-sm text-zinc-500 font-medium">
                {confidence ? `Detected with ${(confidence * 100).toFixed(0)}% confidence` : 'Based on your input'}
              </p>
            </div>
          </div>

          {emotionScores && (
            <div className="hidden md:flex items-center gap-4">
              {Object.entries(emotionScores)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 3)
                .map(([name, score], i) => (
                  <motion.div
                    key={name}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="flex flex-col items-center"
                  >
                    <div className="text-xl font-black text-indigo-600 dark:text-indigo-400">
                      {(score * 100).toFixed(0)}%
                    </div>
                    <span className="text-[10px] uppercase tracking-widest text-zinc-400 font-black">{name}</span>
                  </motion.div>
                ))}
            </div>
          )}
        </div>
      </div>

      {/* Track Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {playlist.map((track, index) => (
          <motion.div
            key={track.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="group relative bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-3xl p-4 flex items-center gap-4 hover:shadow-xl hover:shadow-indigo-500/10 hover:border-indigo-500/50 transition-all duration-300"
          >
            <div className="relative w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 shadow-lg group-hover:shadow-indigo-500/20 transition-all">
              {track.album_art_url ? (
                <Image
                  src={track.album_art_url}
                  alt={track.name}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
              ) : (
                <div className="w-full h-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                  <Music className="w-8 h-8 text-zinc-400" />
                </div>
              )}

              {/* Play Overlay */}
              {track.preview_url && (
                <div
                  className={`absolute inset-0 bg-black/40 flex items-center justify-center transition-all duration-300 ${playingTrack === track.id ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    togglePlay(track);
                  }}
                >
                  <motion.div
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-indigo-600 shadow-xl cursor-pointer"
                  >
                    {playingTrack === track.id ? (
                      <Pause className="w-5 h-5 fill-current" />
                    ) : (
                      <Play className="w-5 h-5 fill-current ml-1" />
                    )}
                  </motion.div>
                </div>
              )}
            </div>

            <div className="flex-grow min-w-0">
              <h4 className="font-bold text-base truncate mb-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                {track.name}
              </h4>
              <p className="text-sm text-zinc-500 font-medium truncate mb-1">{track.artist}</p>
              {track.album_name && (
                <div className="flex items-center text-xs text-zinc-400">
                  <span className="truncate">{track.album_name}</span>
                </div>
              )}
            </div>

            <div className="flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => toggleFavorite(track)}
                className={`p-2 rounded-xl transition-colors ${
                  isFavorite(track.id)
                    ? 'bg-red-50 text-red-500 dark:bg-red-900/20'
                    : 'bg-zinc-50 text-zinc-400 hover:text-red-500 dark:bg-zinc-800'
                }`}
              >
                <Heart className={`w-4 h-4 ${isFavorite(track.id) ? 'fill-current' : ''}`} />
              </motion.button>

              <motion.a
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                href={track.external_url || `https://open.spotify.com/track/${track.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 bg-zinc-50 text-zinc-400 hover:text-indigo-600 dark:bg-zinc-800 rounded-xl transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </motion.a>
            </div>
          </motion.div>
        ))}
      </div>

      {playlist.length === 0 && (
        <div className="text-center py-12">
          <p className="text-zinc-500">No tracks found for this mood.</p>
        </div>
      )}

      {/* Recommended Playlists Section */}
      {recommendedPlaylists && recommendedPlaylists.length > 0 && (
        <div className="pt-8 border-t border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-500" />
              Featured Playlists
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendedPlaylists?.map((pl, idx) => (
              <motion.a
                key={pl.external_url}
                href={pl.external_url}
                target="_blank"
                rel="noopener noreferrer"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.1 }}
                className="group relative bg-white dark:bg-zinc-900 rounded-3xl overflow-hidden border border-zinc-100 dark:border-zinc-800 hover:shadow-2xl hover:shadow-indigo-500/10 transition-all duration-500"
              >
                <div className="relative aspect-square">
                  {pl.image_url ? (
                    <Image
                      src={pl.image_url}
                      alt={pl.name}
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-700"
                    />
                  ) : (
                    <div className="w-full h-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                      <Music className="w-12 h-12 text-zinc-400" />
                    </div>
                  )}
                  <div className="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors" />
                  <div className="absolute bottom-4 right-4 w-12 h-12 bg-white rounded-full flex items-center justify-center text-indigo-600 shadow-2xl opacity-0 translate-y-4 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300">
                    <ExternalLink className="w-6 h-6" />
                  </div>
                </div>
                <div className="p-5">
                  <h4 className="font-bold text-lg mb-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors line-clamp-1">
                    {pl.name}
                  </h4>
                  {pl.description && (
                    <p className="text-sm text-zinc-500 line-clamp-2">{pl.description}</p>
                  )}
                </div>
              </motion.a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
