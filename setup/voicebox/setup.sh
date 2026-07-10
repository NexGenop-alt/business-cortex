#!/bin/bash
# Optional Voicebox TTS Setup for Business Cortex
# Run this script to install Voicebox locally - skips if already installed

set -e

VOICEBOX_DIR="$HOME/opt/voicebox"
VOICEBOX_PORT=17493
CONTAINER_NAME="voicebox-tts"

# Check if already running
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✓ Voicebox already running on port $VOICEBOX_PORT"
    exit 0
fi

# Check if /opt/voicebox exists locally
if [ -d "$VOICEBOX_DIR" ]; then
    echo "✓ Voicebox source found at $VOICEBOX_DIR - starting container..."
else
    echo "Cloning Voicebox repository..."
    git clone https://github.com/jamiepine/voicebox "$VOICEBOX_DIR"
fi

cd "$VOICEBOX_DIR"

# Build and run Docker container
echo "Building Voicebox container..."
docker build -t voicebox-local -f docker/Dockerfile . || docker build -t voicebox-local . || {
    echo "❌ Voicebox build failed - check Docker availability"
    exit 1
}

echo "Starting Voicebox on port $VOICEBOX_PORT..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$VOICEBOX_PORT:$VOICEBOX_PORT" \
    -v "$VOICEBOX_DIR/data:/app/data" \
    voicebox-local

echo "✓ Voicebox installed and running"
echo "  API endpoint: http://localhost:$VOICEBOX_PORT"
echo "  Test: curl http://localhost:$VOICEBOX_PORT/health"