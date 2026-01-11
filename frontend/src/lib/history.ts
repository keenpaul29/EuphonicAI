import { Mood, SpotifyTrack } from './api';

export interface HistoryEntry {
  id: string;
  mood: Mood;
  confidence?: number;
  timestamp: number;
  tracks: SpotifyTrack[];
}

const HISTORY_KEY = 'euphonic_history';
const MAX_HISTORY = 50;

export const HistoryService = {
  getHistory(): HistoryEntry[] {
    if (typeof window === 'undefined') return [];
    try {
      const raw = localStorage.getItem(HISTORY_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (error) {
      console.error('Failed to load history:', error);
      return [];
    }
  },

  addEntry(entry: Omit<HistoryEntry, 'id' | 'timestamp'>): HistoryEntry {
    const history = this.getHistory();
    const newEntry: HistoryEntry = {
      ...entry,
      id: Math.random().toString(36).substr(2, 9),
      timestamp: Date.now(),
    };

    const updatedHistory = [newEntry, ...history].slice(0, MAX_HISTORY);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(updatedHistory));
    } catch (error) {
      console.error('Failed to save history:', error);
    }
    return newEntry;
  },

  clearHistory(): void {
    try {
      localStorage.removeItem(HISTORY_KEY);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  },

  removeEntry(id: string): void {
    const history = this.getHistory();
    const updatedHistory = history.filter(entry => entry.id !== id);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(updatedHistory));
    } catch (error) {
      console.error('Failed to remove history entry:', error);
    }
  }
};
