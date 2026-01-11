import { motion } from 'framer-motion';
import { Play, Sparkles, Music, Camera } from 'lucide-react';

export default function Hero() {
  return (
    <div className="relative overflow-hidden pt-16 pb-24 lg:pt-24 lg:pb-32">
      {/* Background decoration */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/30 dark:bg-indigo-900/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-200/30 dark:bg-purple-900/20 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="inline-flex items-center space-x-2 bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 px-4 py-1.5 rounded-full text-sm font-medium mb-8 border border-indigo-100 dark:border-indigo-900/50">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Music Personalization</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold text-zinc-900 dark:text-zinc-50 tracking-tight mb-8">
            Your Music, <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
              Synced with Your Soul
            </span>
          </h1>
          
          <p className="max-w-2xl mx-auto text-xl text-zinc-600 dark:text-zinc-400 mb-10 leading-relaxed">
            EuphonicAI detects your mood through facial expressions and sentiment analysis to curate the perfect soundtrack for every moment.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="w-full sm:w-auto bg-indigo-600 text-white px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-indigo-700 transition-all shadow-xl shadow-indigo-200 dark:shadow-none flex items-center justify-center space-x-2 group">
              <Play className="w-5 h-5 fill-current group-hover:scale-110 transition-transform" />
              <span>Get Started Now</span>
            </button>
            <button className="w-full sm:w-auto bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 px-8 py-4 rounded-2xl font-semibold text-lg border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-750 transition-all flex items-center justify-center space-x-2">
              <span>View Demo</span>
            </button>
          </div>
        </motion.div>

        {/* Feature Highlights */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-8"
        >
          <div className="p-6 rounded-2xl bg-white/50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800 backdrop-blur-sm">
            <div className="bg-blue-100 dark:bg-blue-900/30 w-12 h-12 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Camera className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-lg font-bold mb-2">Face Recognition</h3>
            <p className="text-zinc-500 text-sm">Real-time emotion detection through your webcam.</p>
          </div>
          
          <div className="p-6 rounded-2xl bg-white/50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800 backdrop-blur-sm">
            <div className="bg-purple-100 dark:bg-purple-900/30 w-12 h-12 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Sparkles className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-lg font-bold mb-2">Sentiment Analysis</h3>
            <p className="text-zinc-500 text-sm">Tell us how you feel, and we'll understand the rest.</p>
          </div>
          
          <div className="p-6 rounded-2xl bg-white/50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800 backdrop-blur-sm">
            <div className="bg-indigo-100 dark:bg-indigo-900/30 w-12 h-12 rounded-xl flex items-center justify-center mb-4 mx-auto">
              <Music className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 className="text-lg font-bold mb-2">Spotify Integration</h3>
            <p className="text-zinc-500 text-sm">Seamlessly play your personalized playlists on Spotify.</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
