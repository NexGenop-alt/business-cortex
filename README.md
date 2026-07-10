# Business Cortex

**One AI agent that summons specialists: lead generation, sales, support, TTS.**

## Quick Start

```bash
# Required components
git clone https://github.com/NexGenop-alt/business-cortex
cd business-cortex
git submodule update --init --recursive

# REQUIRED: Khoj + Graphify (memory/semantic layer)
docker run -d -p 4200:4200 khojai/khoj
pip install graphifyy

# Optional: Voicebox TTS (local install)
./setup/setup.sh --include-voicebox

# Skills are auto-loaded by Hermes Agent
```

## Architecture

```
User Query
    ↓
Cortex Router
    ├── Khoj (memory/search) ← REQUIRED
    ├── Graphify (semantic graph) ← REQUIRED
    ├── Skills (business ops) 
    └── Voicebox TTS ← optional
```

**Workflow example:**
- User: *"Find conversation with Maribel from Valor on 3/2/24"*
- Cortex routes to **both Khoj + Graphify** simultaneously
- Graphify finds the conversation faster (semantic filtering)
- Khoj provides the full content
- Skills layer builds the follow-up email
- Voicebox TTS (optional) can read it aloud

## Components

| Component | Required | What |
|-----------|----------|------|
| **Khoj** | Required | Indexed memory/search across all content |
| **Graphify** | Required | Semantic relationships, faster context filtering |
| **Voicebox** | Optional | TTS - skip if not needed |

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
/voicebox "Hello world" --voice <profile>
```