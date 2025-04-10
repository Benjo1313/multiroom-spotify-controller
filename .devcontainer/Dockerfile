# Use a base image with Python and Node.js dependencies
FROM python:3.13-slim-bullseye

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    gnupg \
    # Add these for VS Code DevContainer user
    sudo \
    # End of additions
    && rm -rf /var/lib/apt/lists/*

# Create the vscode user
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m vscode \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_23.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs

# Install poetry for Python package management
RUN pip3 install poetry

RUN apt-get install -y net-tools

# Set working directory
WORKDIR /workspace

# Copy the startup script to a location that won't be overwritten
COPY .devcontainer/run-dev.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run-dev.sh

RUN echo '#!/bin/bash\ntail -f /dev/null' > /usr/local/bin/keep-running.sh
RUN chmod +x /usr/local/bin/keep-running.sh

# Default command to keep container running
CMD ["/usr/local/bin/run-dev.sh"]
