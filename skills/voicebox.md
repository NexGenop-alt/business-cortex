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
/voicebox "Hello, this is my message" --voice colombian
/voicebox --text "Good morning"
/tts "Make this an audio message"
```

## Configuration

Expected local setup:
- **Docker container**: running on port 17493
- **Voice profiles**: Kokoro + Whisper models (configure via UI or env)
- **Default voice**: Configurable - set `VOICEBOX_DEFAULT_VOICE` env var

## Commands

| Command | Usage |
|---------|-------|
| `/voicebox "<text>"` | Convert text to speech |
| `/voicebox --text "<text>" --voice <profile>` | Specify voice profile |
| `/voicebox --file <path>` | Convert file contents to audio |
| `/voicebox voices` | List available voice profiles |

## Implementation

```python
# Skills check if Voicebox is running before use
import httpx
import os

VOICEBOX_URL = os.getenv("VOICEBOX_URL", "http://localhost:17493")
DEFAULT_VOICE_ID = os.getenv("VOICEBOX_DEFAULT_VOICE", "colombian")

def generate_audio(text: str, voice_id: str = DEFAULT_VOICE_ID) -> str:
    """Generate TTS audio via Voicebox"""
    
    # Check if Voicebox is running (optional - skip if not)
    try:
        response = httpx.get(f"{VOICEBOX_URL}/health", timeout=2)
        if response.status_code != 200:
            return "Voicebox TTS unavailable (optional component)"
    except:
        return "Voicebox TTS unavailable (optional component)"
    
    # Generate speech
    response = httpx.post(
        f"{VOICEBOX_URL}/speak",
        json={"text": text, "voice_id": voice_id},
        timeout=30
    )
    
    if response.status_code == 200:
        return f"Audio generated: {response.json().get('audio_url', 'local file')}"
    else:
        return f"Voicebox error: {response.status_code}"
```

## Notes

- This is an **optional component** - Cortex works without it
- Voice configured via `VOICEBOX_DEFAULT_VOICE` environment variable
- Falls back gracefully if Voicebox unavailable
- Integrates with Hermes TTS tool for seamless delivery