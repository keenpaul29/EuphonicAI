'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import ApiClient, { SpotifyTrack, Mood } from '@/lib/api';
import PlaylistDisplay from '@/components/PlaylistDisplay';

export default function SharePage() {
  const params = useSearchParams();
  const [tracks, setTracks] = useState<SpotifyTrack[]>([]);
  const mood = (params.get('mood') || 'neutral') as Mood;

  useEffect(() => {
    const idsParam = params.get('ids');
    if (!idsParam) return;
    const ids = idsParam.split(',').map(s => s.trim()).filter(Boolean);
    const load = async () => {
      const res = await ApiClient.getTracksByIds(ids);
      setTracks(res);
    };
    load();
  }, [params]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold">Shared Playlist</h1>
          <p className="text-gray-600 dark:text-gray-300">Enjoy this playlist</p>
        </header>
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl">
          {tracks.length > 0 ? (
            <PlaylistDisplay mood={mood} playlist={tracks} />
          ) : (
            <p className="text-center text-gray-600 dark:text-gray-300">Loading playlist...</p>
          )}
        </div>
      </div>
    </main>
  );
}
