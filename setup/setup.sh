#!/bin/bash
# Business Cortex Setup - All Optional Components
# Usage: ./setup.sh [--include-voicebox]

set -e

echo "🔧 Business Cortex Setup"

# Parse arguments
INCLUDE_VOICEBOX=false
for arg in "$@"; do
    case $arg in
        --include-voicebox) INCLUDE_VOICEBOX=true ;;
        *) echo "Unknown arg: $arg" && exit 1 ;;
    esac
done

# Required: Update submodules
echo "📦 Updating submodules..."
git submodule update --init --recursive

# Optional: Voicebox TTS
if [ "$INCLUDE_VOICEBOX" = true ]; then
    echo "🔊 Setting up Voicebox (optional)..."
    bash setup/voicebox/setup.sh || echo "⚠️ Voicebox setup failed - continuing without it"
else
    echo "📝 Skipping Voicebox (add --include-voicebox if needed)"
fi

# Optional: Graphify
if command -v uvx &> /dev/null; then
    echo "📊 Graphify already available via uvx"
else
    echo "⚠️ Graphify not found - run 'pip install graphifyy' if needed"
fi

# Optional: Khoj
if docker ps | grep -q khoj; then
    echo "🧠 Khoj already running"
else
    echo "⚠️ Khoj not detected - run 'docker run khojai/khoj' if needed"
fi

echo "✅ Setup complete"
echo ""
echo "Optional services status:"
echo "  Voicebox: $(docker ps | grep -q voicebox && echo 'Running' || echo 'Not installed')"
echo "  Khoj: $(docker ps | grep -q khoj && echo 'Running' || echo 'Not installed')"
echo "  Graphify: $(command -v graphifyy &> /dev/null && echo 'Available' || echo 'Not installed')"