# Spotify Zone Control

A system for controlling Spotify playback and managing Snap zone selection from multiple devices.

## Project Overview
- Control Spotify playback from multiple devices
- Manage Snap zone selection
- Cross-platform web application

## Development Setup

### Prerequisites
- Docker and Docker Compose
- VS Code with Remote Containers extension

### Quick Start
1. Clone this repository
2. Run the setup script: `bash setup-project.sh`
3. Create a `.env` file with your Spotify credentials:

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