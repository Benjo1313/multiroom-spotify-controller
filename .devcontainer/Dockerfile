# Use a base image with Python and Node.js dependencies
FROM python:3.13-slim-bullseye

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 
RUN  apt-get install -y gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_23.x -o nodesource_setup.sh \
    && bash nodesource_setup.sh \
    && apt-get update \
    && apt-get install -y nodejs

# Install poetry for Python package management
RUN pip3 install poetry

# Set working directory for the backend
WORKDIR /app/backend

# Copy poetry files
COPY backend/pyproject.toml backend/poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# Copy the backend application
COPY backend/app ./app

# Expose backend port
EXPOSE 8000

# Set working directory for the frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json ./

RUN rm -rf package-lock.json node_modules

# Install npm dependencies
RUN npm i

# Copy the frontend application
COPY frontend/ ./

# Expose frontend port
EXPOSE 3000

# Script to run both backend and frontend
COPY .devcontainer/run-dev.sh /app/run-dev.sh
RUN chmod +x /app/run-dev.sh

# Start the application
CMD ["/app/run-dev.sh"]