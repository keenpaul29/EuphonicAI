import React, { useState } from 'react';
import { Send, Sparkles, MessageSquare } from 'lucide-react';
import { motion } from 'framer-motion';

interface TextInputProps {
  onSubmit: (text: string) => void;
  isLoading: boolean;
}

const TextInput: React.FC<TextInputProps> = ({ onSubmit, isLoading }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text.trim());
    }
  };

  return (
    <div className="w-full h-full flex flex-col justify-center">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative group">
          <div className="absolute -top-3 left-4 px-2 bg-white dark:bg-zinc-900 text-xs font-bold text-indigo-600 dark:text-indigo-400 z-10 flex items-center gap-1">
            <MessageSquare className="w-3 h-3" />
            EXPRESS YOURSELF
          </div>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full px-6 py-6 bg-zinc-50 dark:bg-zinc-950 border-2 border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100 rounded-3xl shadow-sm focus:outline-none focus:ring-4 focus:ring-indigo-600/10 focus:border-indigo-600 transition-all resize-none min-h-[160px] placeholder:text-zinc-400"
            placeholder="I'm feeling a bit energetic today and want something to keep me going while I work..."
            disabled={isLoading}
          />
          <div className="absolute bottom-4 right-4 flex items-center space-x-2">
             <span className={`text-[10px] font-bold ${text.length > 200 ? 'text-red-500' : 'text-zinc-400'}`}>
              {text.length} characters
             </span>
          </div>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          type="submit"
          disabled={isLoading || !text.trim()}
          className={`w-full py-4 rounded-2xl font-bold shadow-lg transition-all flex items-center justify-center space-x-2 
            ${isLoading || !text.trim() 
              ? 'bg-zinc-100 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed shadow-none' 
              : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-indigo-200 dark:shadow-none'
            }`}
        >
          {isLoading ? (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Analyzing Sentiment...</span>
            </div>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Generate Mood Playlist</span>
            </>
          )}
        </motion.button>
        
        <p className="text-center text-xs text-zinc-400">
          Our AI analyzes the sentiment of your text to find the perfect musical match.
        </p>
      </form>
    </div>
  );
};

export default TextInput;
