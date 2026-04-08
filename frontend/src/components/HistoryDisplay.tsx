import React, { useState, useEffect } from 'react';
import { HistoryService, HistoryEntry } from '@/lib/history';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, Trash2, ChevronRight, Music, Calendar } from 'lucide-react';
import Image from 'next/image';
import { } from '@/lib/api';

export default function HistoryDisplay() {
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  useEffect(() => {
    setHistory(HistoryService.getHistory());
  }, []);

  const handleClear = () => {
    if (confirm('Are you sure you want to clear your emotional history?')) {
      HistoryService.clearHistory();
      setHistory([]);
    }
  };

  const removeEntry = (id: string) => {
    HistoryService.removeEntry(id);
    setHistory(prev => prev.filter(e => e.id !== id));
  };

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString(undefined, { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
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
    return emojis[mood.toLowerCase()] || '🎵';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <Clock className="w-5 h-5 text-indigo-500" />
          Your Emotional Journey
        </h3>
        {history.length > 0 && (
          <button
            onClick={handleClear}
            className="text-sm text-red-500 hover:text-red-600 flex items-center gap-1 font-medium transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="text-center py-16 bg-zinc-50 dark:bg-zinc-900/50 rounded-3xl border border-dashed border-zinc-200 dark:border-zinc-800">
          <div className="w-16 h-16 bg-zinc-100 dark:bg-zinc-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Calendar className="w-8 h-8 text-zinc-400" />
          </div>
          <p className="text-zinc-500 font-medium">Your history is empty.</p>
          <p className="text-sm text-zinc-400">Start discovering music to track your moods!</p>
        </div>
      ) : (
        <div className="space-y-4">
          <AnimatePresence mode="popLayout">
            {history.map((entry) => (
              <motion.div
                key={entry.id}
                layout
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="group bg-white dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 rounded-3xl p-5 hover:shadow-xl hover:shadow-indigo-500/5 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-4">
                    <div className="text-3xl bg-zinc-50 dark:bg-zinc-800 w-12 h-12 rounded-2xl flex items-center justify-center shadow-inner">
                      {getMoodEmoji(entry.mood)}
                    </div>
                    <div>
                      <h4 className="font-bold capitalize text-lg">{entry.mood}</h4>
                      <div className="flex items-center gap-2 text-xs text-zinc-400 font-medium">
                        <Calendar className="w-3 h-3" />
                        {formatDate(entry.timestamp)}
                        {entry.confidence && (
                          <span className="bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 px-1.5 py-0.5 rounded text-[10px] uppercase tracking-wider">
                            {(entry.confidence * 100).toFixed(0)}% Match
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => removeEntry(entry.id)}
                    className="p-2 text-zinc-300 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-all"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
                  {entry.tracks.slice(0, 5).map((track) => (
                    <div key={track.id} className="flex-shrink-0 w-24">
                      <div className="relative w-24 h-24 rounded-xl overflow-hidden mb-2 shadow-sm">
                        {track.album_art_url ? (
                          <Image
                            src={track.album_art_url}
                            alt={track.name}
                            fill
                            className="object-cover"
                          />
                        ) : (
                          <div className="w-full h-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                            <Music className="w-6 h-6 text-zinc-400" />
                          </div>
                        )}
                      </div>
                      <p className="text-[10px] font-bold truncate text-zinc-700 dark:text-zinc-300">{track.name}</p>
                      <p className="text-[9px] text-zinc-400 truncate">{track.artist}</p>
                    </div>
                  ))}
                  {entry.tracks.length > 5 && (
                    <div className="flex-shrink-0 w-24 h-24 bg-zinc-50 dark:bg-zinc-800 rounded-xl flex flex-col items-center justify-center gap-1 text-zinc-400">
                      <span className="text-xs font-bold">+{entry.tracks.length - 5}</span>
                      <span className="text-[9px] uppercase tracking-widest font-black">More</span>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
