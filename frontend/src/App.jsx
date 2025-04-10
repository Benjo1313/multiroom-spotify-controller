import { useState, useEffect } from 'react';
import SpotifyPlayer from './SpotifyPlayer'; // Make sure the path is correct

function App() {
  const [apiStatus, setApiStatus] = useState('Loading...'); // Keep this if you plan to display it somewhere

  useEffect(() => {
    // Check if API is running
    fetch('http://localhost:8000/health')
      .then(response => response.ok ? response.json() : Promise.reject(`HTTP error! status: ${response.status}`)) // Add basic check for ok response
      .then(data => {
        setApiStatus(data.status === 'healthy' ? 'Connected to API' : 'API Error: ' + (data.status || 'Unknown status'));
      })
      .catch(error => {
        console.error('Error connecting to API:', error);
        setApiStatus(`Failed to connect to API: ${error}`);
      });
  }, []);

  // Directly return the JSX you want to render
  return (
    <div className="min-h-screen bg-gray-900">
      <div className="test-bg">Test</div>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white mb-6">Spotify Zone Control</h1>
        <SpotifyPlayer />
      </div>
    </div>
  );
}

export default App;