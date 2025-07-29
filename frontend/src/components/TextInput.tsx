import React, { useState } from 'react';

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
    <div className="w-full max-w-lg mx-auto p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="text-input" className="block text-sm font-medium text-white mb-2">
            How are you feeling today?
          </label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 text-black rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={4}
            placeholder="Tell me about your mood..."
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !text.trim()}
          className={`w-full px-4 py-2 text-white font-semibold rounded-md shadow-sm 
            ${isLoading || !text.trim() 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
            }`}
        >
          {isLoading ? 'Analyzing...' : 'Get Music Recommendations'}
        </button>
      </form>
    </div>
  );
};

export default TextInput;
