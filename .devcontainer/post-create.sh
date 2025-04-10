#!/bin/bash
set -e

# Run dependencies script
bash .devcontainer/dependencies.sh

# Navigate to the backend directory
cd /workspace/backend

# Install Python dependencies if needed
if [ -f "pyproject.toml" ]; then
    poetry install --no-root
fi

# Navigate to the frontend directory
cd /workspace/frontend

# Install npm dependencies if needed
if [ -f "package.json" ]; then
    npm install
fi

echo "Dev container setup complete!"