import React, { useRef, useCallback } from 'react';
import WebcamComponent from 'react-webcam';

interface WebcamProps {
  onCapture: (imageSrc: string) => void;
  onError: (error: string) => void;
  onReady: () => void;
}

export default function Webcam({ onCapture, onError, onReady }: WebcamProps) {
  const webcamRef = useRef<WebcamComponent>(null);

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
  }, [onCapture, onError]);

  return (
    <div className="relative rounded-2xl overflow-hidden">
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
        onUserMediaError={(error) => onError(error.message)}
        mirrored
        className="w-full aspect-video object-cover"
      />
      <button
        onClick={capture}
        className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white/90 hover:bg-white dark:bg-black/90 dark:hover:bg-black text-black dark:text-white px-6 py-2 rounded-full shadow-lg transition-all duration-200 flex items-center space-x-2"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span>Capture</span>
      </button>
    </div>
  );
}
