#!/bin/bash
# This can be used as a replacement for start-dev later on when deploying the prod container
# Save as setup-project.sh in your project root

echo "Setting up Spotify Zone Control project..."

# Create required directories
mkdir -p frontend/src/components
mkdir -p frontend/src/hooks
mkdir -p backend/app

# Create SpotifyPlayer component
cat > frontend/src/components/SpotifyPlayer.jsx << 'EOL'
import React, { useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, List } from 'lucide-react';

// SpotifyPlayer component code here
// Paste the full component code
EOL

# Create useSpotify hook
cat > frontend/src/hooks/useSpotify.js << 'EOL'
import { useState, useEffect } from 'react';

export const useSpotify = () => {
  // useSpotify hook code here
  // Paste the full hook code
};
EOL

# Update App.jsx to use the SpotifyPlayer
cat > frontend/src/App.jsx << 'EOL'
import React from 'react';
import SpotifyPlayer from './components/SpotifyPlayer';

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white mb-6">Spotify Zone Control</h1>
        <SpotifyPlayer />
      </div>
    </div>
  );
}

export default App;
EOL

echo "Project setup complete! You can now build and run the Docker container."