#!/bin/bash
set -e

echo "Setting up development environment..."

# Backend setup
cd /workspace/backend
poetry init -n --name spotify-control-backend --author "Your Name" --python ">=3.8,<4.0"
poetry add fastapi uvicorn python-dotenv httpx spotipy pydantic-settings

# Add development dependencies
poetry add --group dev pytest pytest-asyncio black isort mypy pylint

# Frontend setup
cd /workspace/frontend
npm init -y
npm install react react-dom react-router-dom
npm install @heroicons/react axios
npm install tailwindcss postcss autoprefixer
npm install --save-dev vite @vitejs/plugin-react typescript @types/react @types/react-dom

# Initialize Tailwind CSS
npx tailwindcss init -p

echo "Development environment setup complete!"