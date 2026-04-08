import { Mood, SpotifyTrack } from './api';
import ApiClient from './api';

export interface HistoryEntry {
  mood: Mood;
  confidence?: number;
  tracks: SpotifyTrack[];
}

export interface BackendHistoryEntry extends HistoryEntry {
  id: number;
  created_at: string;
}

export class HistoryService {
  static async addEntry(entry: HistoryEntry): Promise<void> {
    try {
      await ApiClient['client'].post('/api/history/', entry);
    } catch (error) {
      console.error('Failed to save history to backend', error);
      // Fallback to local storage if backend fails
      const current = this.getEntriesLocal();
      const updated = [entry, ...current].slice(0, 50);
      try {
        localStorage.setItem('moodify_history', JSON.stringify(updated));
      } catch (e) {
        console.error('Failed to save history locally', e);
      }
    }
  }

  static async getEntries(): Promise<HistoryEntry[]> {
    try {
      const response = await ApiClient['client'].get<BackendHistoryEntry[]>('/api/history/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch history from backend', error);
      return this.getEntriesLocal();
    }
  }

  private static getEntriesLocal(): HistoryEntry[] {
    if (typeof window === 'undefined') return [];

    try {
      const stored = localStorage.getItem('moodify_history');
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Failed to parse history', error);
      return [];
    }
  }

  static async clearHistory(): Promise<void> {
    try {
      await ApiClient['client'].delete('/api/history/');
    } catch (error) {
      console.error('Failed to clear history from backend', error);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('moodify_history');
      }
    }
  }

  static async removeEntry(id: string | number): Promise<void> {
    try {
      await ApiClient['client'].delete(`/api/history/${id}`);
    } catch (error) {
      console.error('Failed to delete history entry from backend', error);
    }
  }
}
