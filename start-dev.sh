#!/bin/bash

# Make sure the run-dev script is executable
chmod +x .devcontainer/run-dev.sh
chmod +x .devcontainer/post-create.sh

# Navigate to backend directory and start services
cd /workspace
bash /usr/local/bin/run-dev.sh