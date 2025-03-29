import { useState, useEffect } from 'react'

function App() {
  const [apiStatus, setApiStatus] = useState('Loading...')

  useEffect(() => {
    // Check if API is running
    fetch('http://localhost:8000/health')
      .then(response => response.json())
      .then(data => {
        setApiStatus(data.status === 'healthy' ? 'Connected to API' : 'API Error')
      })
      .catch(error => {
        console.error('Error connecting to API:', error)
        setApiStatus('Failed to connect to API')
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gradient-to-r from-green-400 to-blue-500 shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-white">Spotify Zone Control</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-8">
            <p className="text-2xl font-semibold text-gray-700 mb-4">Welcome to your Spotify Zone Control App</p>
            <p className="text-gray-600 mb-4">
              This app will help you control Spotify playback and manage Snap zone selection from multiple devices.
            </p>
            <div className="mt-8 p-4 bg-white rounded shadow">
              <p className="text-lg">Backend Status: 
                <span 
                  className={`ml-2 font-semibold ${
                    apiStatus === 'Connected to API' 
                      ? 'text-green-600' 
                      : 'text-red-600'
                  }`}
                >
                  {apiStatus}
                </span>
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App