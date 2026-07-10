---
name: voicebox
triggers:
  - "/voicebox"
  - "say"
  - "speak"
  - "text to speech"
  - "tts"
requires:
  - voicebox_local  # Optional - checks if running before using
---

# Voicebox TTS Skill

Text-to-speech using locally-running Voicebox server.

## Usage
```
/voicebox "Hello, this is my message" --profile 18b742da
/voicebox --text "Good morning" --voice colombian
/tts "Make this an audio message"
```

## Configuration

Expected local setup:
- **Docker container**: running on port 17493
- **Voice profiles**: Kokoro + Whisper models loaded
- **Default voice**: Colombian female (id: 18b742da)

## Commands

| Command | Usage |
|---------|-------|
| `/voicebox "<text>"` | Convert text to speech |
| `/voicebox --file <path>` | Convert file contents to audio |
| `/voicebox voices` | List available voice profiles |

## Implementation

```python
# Skills check if Voicebox is running before use
import httpx

VOICEBOX_URL = "http://localhost:17493"
DEFAULT_VOICE_ID = "18b742da"

def generate_audio(text: str, voice_id: str = DEFAULT_VOICE_ID) -> str:
    """Generate TTS audio via Voicebox"""
    
    # Check if Voicebox is running
    try:
        response = httpx.get(f"{VOICEBOX_URL}/health", timeout=2)
        if response.status_code != 200:
            return "Voicebox not available - ensure Docker container is running"
    except:
        return "Voicebox server not reachable on port 17493"
    
    # Generate speech
    response = httpx.post(
        f"{VOICEBOX_URL}/speak",
        json={"text": text, "voice_id": voice_id},
        timeout=30
    )
    
    if response.status_code == 200:
        # Returns audio file path or URL
        return f"Audio generated: {response.json().get('audio_url', 'local file')}"
    else:
        return f"Voicebox error: {response.status_code}"
```

## Notes

- This skill assumes Voicebox is running locally
- No installation required if using existing setup
- Falls back gracefully if Voicebox unavailable
- Integrates with Hermes TTS tool for seamless delivery