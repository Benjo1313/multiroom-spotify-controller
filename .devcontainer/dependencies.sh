#!/bin/bash

# Frontend dependencies
FRONTEND_PACKAGES=(
  "lucide-react"
  "axios"
  "tailwindcss"
  "postcss"
  # Add any other npm packages here
)

# Backend dependencies
BACKEND_PACKAGES=(
  "uvicorn"
  "spotipy"
  # Add any other Python packages here P
)

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd /workspace/frontend
for package in "${FRONTEND_PACKAGES[@]}"; do
  npm install --save $package
done

# Install backend dependencies
echo "Installing backend dependencies..."
cd /workspace/backend
for package in "${BACKEND_PACKAGES[@]}"; do
  poetry add $package
done

echo "All dependencies installed successfully!"