# Business Cortex

**One AI agent that summons specialists: lead generation, sales, support, TTS.**

## Quick Start

```bash
# Required components
git clone https://github.com/NexGenop-alt/business-cortex
cd business-cortex
git submodule update --init --recursive

# Optional: Voicebox TTS (your existing local install)
./setup/setup.sh --include-voicebox

# Skills are auto-loaded by Hermes Agent
```

## Architecture

```
User Query
    ↓
Cortex Router
    ├── Khoj (memory/search) ← optional
    ├── Graphify (semantic graph) ← optional  
    ├── Skills (business ops)
    └── Voicebox TTS ← optional
```

## Optional Components

| Component | What | Install |
|-----------|------|---------|
| **Khoj** | Search conversations, notes | `docker run -p 4200:4200 khojai/khoj` |
| **Graphify** | Code/relationship graphs | `pip install graphifyy` |
| **Voicebox** | Text-to-speech | `./setup/setup.sh --include-voicebox` |

**All optional** - Cortex works without any of these. Skills gracefully skip missing components.

## Skills Included

- `sales-agent` - lead sourcing, ICP, cold email
- `marketing-agent` - content creation, campaigns  
- `back-office-agent` - invoicing, billing
- `support-agent` - tickets, customer queries
- `voicebox` - TTS via local Voicebox

## Usage

```
/sales icp definition
/sales source leads san diego
/invoice create for client-x
/voicebox "Hello world" --voice colombian
```