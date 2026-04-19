import React, { useRef, useCallback, useState, useEffect } from 'react';
import WebcamComponent from 'react-webcam';
import { Camera, RefreshCw, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface WebcamProps {
  onCapture: (imageSrc: string) => void;
  onError: (error: string) => void;
  onReady: () => void;
}

export default function Webcam({ onCapture, onError, onReady }: WebcamProps) {
  const webcamRef = useRef<WebcamComponent>(null);
  const [isCountingDown, setIsCountingDown] = useState(false);
  const [countdown, setCountdown] = useState(3);

  const handleUserMedia = useCallback(() => {
    onReady();
  }, [onReady]);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      onCapture(imageSrc);
    } else {
      onError('Failed to capture image');
    }
    setIsCountingDown(false);
    setCountdown(3);
  }, [onCapture, onError]);

  const startCountdown = () => {
    setIsCountingDown(true);
    setCountdown(3);
  };

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isCountingDown && countdown > 0) {
      timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    } else if (isCountingDown && countdown === 0) {
      capture();
    }
    return () => clearTimeout(timer);
  }, [isCountingDown, countdown, capture]);

  return (
    <div className="relative w-full h-full group overflow-hidden bg-zinc-950">
      <WebcamComponent
        ref={webcamRef}
        audio={false}
        screenshotFormat="image/jpeg"
        screenshotQuality={0.92}
        videoConstraints={{
          width: 1280,
          height: 720,
          facingMode: "user",
          aspectRatio: 16/9,
        }}
        onUserMedia={handleUserMedia}
        onUserMediaError={(error: any) => onError(typeof error === 'string' ? error : error?.message || 'Webcam error')}
        mirrored
        className="w-full h-full object-cover"
      />

      {/* Scanner Overlay */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 border-[20px] border-black/20" />
        <div className="absolute top-10 left-10 w-20 h-20 border-t-4 border-l-4 border-white/50 rounded-tl-3xl" />
        <div className="absolute top-10 right-10 w-20 h-20 border-t-4 border-r-4 border-white/50 rounded-tr-3xl" />
        <div className="absolute bottom-10 left-10 w-20 h-20 border-b-4 border-l-4 border-white/50 rounded-bl-3xl" />
        <div className="absolute bottom-10 right-10 w-20 h-20 border-b-4 border-r-4 border-white/50 rounded-br-3xl" />
        
        <motion.div 
          animate={{ top: ['10%', '90%', '10%'] }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          className="absolute left-10 right-10 h-0.5 bg-gradient-to-r from-transparent via-indigo-500 to-transparent shadow-[0_0_15px_rgba(99,102,241,0.8)]"
        />
      </div>

      {/* Controls */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex items-center space-x-4">
        <button
          onClick={startCountdown}
          disabled={isCountingDown}
          className={`relative overflow-hidden bg-white text-zinc-900 px-8 py-3 rounded-2xl font-bold shadow-2xl transition-all hover:scale-105 active:scale-95 flex items-center space-x-3 ${isCountingDown ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isCountingDown ? (
            <RefreshCw className="w-5 h-5 animate-spin" />
          ) : (
            <Camera className="w-5 h-5" />
          )}
          <span>{isCountingDown ? 'Analyzing...' : 'Detect Emotion'}</span>
        </button>
      </div>

      {/* Countdown Overlay */}
      <AnimatePresence>
        {isCountingDown && countdown > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.5 }}
            className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-[2px]"
          >
            <span className="text-8xl font-black text-white drop-shadow-2xl">
              {countdown}
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Hint */}
      {!isCountingDown && (
        <div className="absolute top-6 left-1/2 -translate-x-1/2 bg-black/50 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span className="text-white text-xs font-medium">Show us your beautiful face</span>
        </div>
      )}
    </div>
  );
}
