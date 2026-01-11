import React, { useState, useEffect } from 'react';
import ApiClient, { SpotifyTrack } from '@/lib/api';
import Image from 'next/image';
import { Search, Music, ExternalLink, Play, Pause, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SearchBar({ language }: { language?: string }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SpotifyTrack[]>([]);
  const [isLoading, setIsLoading] = useState(false);
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

  const onSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const tracks = await ApiClient.searchTracks(query.trim(), 12, language);
      setResults(tracks);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <form onSubmit={onSearch} className="relative group">
        <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
          <Search className="w-5 h-5 text-zinc-400 group-focus-within:text-indigo-500 transition-colors" />
        </div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-12 pr-32 py-4 bg-zinc-50 dark:bg-zinc-800 border-none rounded-2xl text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-500 focus:ring-2 focus:ring-indigo-500 transition-all shadow-inner"
          placeholder="Search for any song or artist..."
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-2 inset-y-2 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-zinc-300 dark:disabled:bg-zinc-700 text-white rounded-xl font-bold transition-all flex items-center gap-2 shadow-lg shadow-indigo-500/20"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            'Search'
          )}
        </button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AnimatePresence mode="popLayout">
          {results.map((track, index) => (
            <motion.div
              key={track.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              className="group relative bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-3xl p-4 flex items-center gap-4 hover:shadow-xl hover:shadow-indigo-500/10 hover:border-indigo-500/50 transition-all duration-300"
            >
              <div className="relative w-16 h-16 rounded-2xl overflow-hidden flex-shrink-0 shadow-lg">
                {track.album_art_url ? (
                  <Image
                    src={track.album_art_url}
                    alt={track.name}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                ) : (
                  <div className="w-full h-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                    <Music className="w-6 h-6 text-zinc-400" />
                  </div>
                )}
                
                {/* Play Overlay */}
                {track.preview_url && (
                  <div 
                    className={`absolute inset-0 bg-black/40 flex items-center justify-center transition-all duration-300 ${playingTrack === track.id ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}
                    onClick={() => togglePlay(track)}
                  >
                    <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center text-indigo-600 shadow-xl cursor-pointer">
                      {playingTrack === track.id ? (
                        <Pause className="w-4 h-4 fill-current" />
                      ) : (
                        <Play className="w-4 h-4 fill-current ml-0.5" />
                      )}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex-grow min-w-0">
                <h4 className="font-bold text-sm truncate mb-0.5 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                  {track.name}
                </h4>
                <p className="text-xs text-zinc-500 font-medium truncate">{track.artist}</p>
              </div>

              <motion.a
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                href={track.external_url || `https://open.spotify.com/track/${track.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 bg-zinc-50 dark:bg-zinc-800 text-zinc-400 hover:text-indigo-600 rounded-xl transition-colors opacity-0 group-hover:opacity-100"
              >
                <ExternalLink className="w-4 h-4" />
              </motion.a>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {!isLoading && query && results.length === 0 && (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-zinc-50 dark:bg-zinc-800 rounded-2xl flex items-center justify-center mx-auto mb-4 text-zinc-400">
            <Search className="w-8 h-8" />
          </div>
          <p className="text-zinc-500 font-medium">No tracks found for "{query}"</p>
        </div>
      )}
    </div>
  );
}
