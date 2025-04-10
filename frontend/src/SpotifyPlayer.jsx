import React, { useState, useEffect } from 'react';
import { Play, Pause, SkipBack, SkipForward, List } from 'lucide-react';
import { useSpotify } from './hooks/useSpotify';

const SpotifyPlayer = () => {
  const { currentTrack, isPlaying, progress, play, pause, next, previous, getQueue } = useSpotify();
  const [showQueue, setShowQueue] = useState(false);
  const [queue, setQueue] = useState([]);
  
  const togglePlay = () => {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  };
  
  const viewQueue = async () => {
    const queueData = await getQueue();
    setQueue(queueData);
    setShowQueue(!showQueue);
  };

  return (
    <div className="flex items-center justify-center w-full h-screen bg-gray-900">
      <div className="w-full max-w-3xl bg-black rounded-lg p-4 text-white shadow-2xl">
        <div className="flex items-center space-x-4">
          {/* Album Cover */}
          <div className="flex-shrink-0">
            <div className="w-16 h-16 bg-gray-700 rounded overflow-hidden">
              <img 
                src="/api/placeholder/64/64" 
                alt="Album cover" 
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          {/* Song Info & Controls */}
          <div className="flex-grow">
            <div className="mb-2">
              <h3 className="font-semibold text-sm">Song Title</h3>
              <p className="text-gray-400 text-xs">Artist Name</p>
            </div>

            {/* Progress Bar */}
            <div className="mb-2">
              <div className="h-1 w-full bg-gray-700 rounded-full">
                <div 
                  className="h-1 bg-green-500 rounded-full" 
                  style={{ width: `${progress}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>1:24</span>
                <span>3:45</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-center space-x-6 mt-2">
              <button className="text-gray-400 hover:text-white transition">
                <SkipBack size={20} />
              </button>
              
              <button 
                class="bg-white rounded-full p-2 text-black hover:scale-105 transition"
                onClick={togglePlay}
              >
                {isPlaying ? <Pause size={20} /> : <Play size={20} />}
              </button>
              
              <button className="text-gray-400 hover:text-white transition">
                <SkipForward size={20} />
              </button>
              
              <button className="text-gray-400 hover:text-white transition ml-6">
                <List size={20} />
              </button>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
};

export default SpotifyPlayer;