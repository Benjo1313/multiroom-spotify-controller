# Spotify Zone Control

A system for controlling Spotify playback and managing Snap zone selection from multiple devices.

## Project Overview
- Control Spotify playback from multiple devices
- Manage Snap zone selection
- Cross-platform web application

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Visual Studio Code
- VS Code Remote - Containers extension

### Getting Started
1. Clone this repository
2. Open the project in VS Code
3. When prompted to "Reopen in Container", click "Reopen in Container"
   (or use the Command Palette: "Remote-Containers: Reopen in Container")
4. VS Code will build the dev container and open the project inside it

### Development Workflow
- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:3000
- API docs available at http://localhost:8000/docs

## Architecture
- Backend: FastAPI (Python)
- Frontend: React with Tailwind CSS
- Deployment: Docker containers

## Project Structure
```
spotify-control-app/
│
├── backend/             # FastAPI Backend
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── poetry.lock
│
├── frontend/            # React Frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── .devcontainer/       # Development container configuration
├── docker-compose.yml
├── .gitignore
└── README.md
```