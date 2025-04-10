import { useState, useEffect } from 'react';

export const useSpotify = () => {
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  
  // Function to get the current playing track
  const getCurrentTrack = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/spotify/now-playing');
      const data = await response.json();
      if (data.item) {
        setCurrentTrack(data);
        setIsPlaying(data.is_playing);
        setProgress((data.progress_ms / data.item.duration_ms) * 100);
      }
    } catch (error) {
      console.error('Error fetching current track:', error);
    }
  };
  
  // Function to control playback
  const controlPlayback = async (action) => {
    try {
      await fetch(`http://localhost:8000/api/spotify/${action}`, { method: 'POST' });
      // After action, update the current track
      getCurrentTrack();
    } catch (error) {
      console.error(`Error with ${action}:`, error);
    }
  };
  
  // Poll for updates every 3 seconds
  useEffect(() => {
    getCurrentTrack();
    const interval = setInterval(getCurrentTrack, 3000);
    return () => clearInterval(interval);
  }, []);
  
  return {
    currentTrack,
    isPlaying,
    progress,
    play: () => controlPlayback('play'),
    pause: () => controlPlayback('pause'),
    next: () => controlPlayback('next'),
    previous: () => controlPlayback('previous'),
    getQueue: async () => {
      try {
        const response = await fetch('http://localhost:8000/api/spotify/queue');
        return await response.json();
      } catch (error) {
        console.error('Error fetching queue:', error);
        return [];
      }
    }
  };
};