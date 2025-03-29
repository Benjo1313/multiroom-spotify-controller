#!/bin/bash

# Start backend and frontend in parallel
echo "Starting development servers..."

# Start FastAPI in the background
cd /workspace/backend
poetry run python -m app.main &
BACKEND_PID=$!

# Start React in the background
cd /workspace/frontend
npm run dev &
FRONTEND_PID=$!

# Function to handle exit
cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID $FRONTEND_PID
  exit 0
}

# Handle SIGINT (Ctrl+C)
trap cleanup SIGINT

# Keep script running
echo "Development servers are running. Press Ctrl+C to stop."
wait