#!/bin/bash
set -e

echo "Starting backend..."
cd /workspace/backend

if [ -f "pyproject.toml" ]; then
    poetry install --no-root
fi

export PATH="$(poetry env info --path)/bin:$PATH"
echo "Using Poetry environment at $(poetry env info --path)"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

echo "Starting frontend..."
cd /workspace/frontend

if [ -f "package.json" ]; then
    npm install
fi

npm run dev &

echo "Servers started!"
tail -f /dev/null
