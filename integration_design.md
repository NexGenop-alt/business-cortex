# Hermes Agent Integration Design: Graphify + Khoj

## Overview

This document describes how Hermes Agent orchestrates between **Graphify** (memory graph) and **Khoj** (search) to provide unified, cross-platform content retrieval for agent skills like `sales-agent`.

**Vision**: "Find conversation with Example Contact on 4/13/26" returns content regardless of source (PDF, markdown, database, previous conversations).

---

## 1. Architecture: Hermes Orchestration

### 1.1 High-Level Flow

```
User Query
    ↓
Hermes Router (`/memory` toolset)
    ↓
┌────────────────────────────────────────┐
│     Query Intent Classifier              │
│  - What am I looking for?                │
│  - Date/person/project filter?          │
│  - Which backend to prioritize?         │
└────────────────────────────────────────┘
    ↓
Parallel/Distributed Calls:
    ├── Graphify API → Knowledge Graph Search
    │   - `/graph/query` — semantic graph queries
    │   - `/graph/path` — relationship paths
    │   - Returns: structured nodes/edges with confidence scores
    │
    └── Khoj API → Document Search
        - `/api/content/search` — full-text/semantic search
        - `/api/memories` — conversation history
        - `/api/chat/history` — chat transcripts
        - Returns: ranked documents with snippets
    ↓
Result Merger → Confidence-weighted ranking
    ↓
Unified Response to Calling Skill
```

### 1.2 Hermes Memory Toolset

Hermes natively supports a `memory` toolset that integrates external memory systems:

- **Built-in backends**: SQLite (default), Mem0, Honcho
- **MCP Integration**: Graphify/Khoj exposed as MCP servers
- **Skill API**: Skills call `memory.search(query, filters)` and get unified results

### 1.3 Confidence Scoring

Each backend assigns confidence:

| Source | Confidence Labels | Hermes Interpretation |
|--------|-------------------|----------------------|
| Graphify | EXTRACTED, INFERRED, AMBIGUOUS | EXTRACTED = highest weight, INFERRED = medium, AMBIGUOUS = low |
| Khoj | relevance score (0-1) + source type | High similarity = boost, PDF/MD chat = normalize |

---

## 2. Skill Integration: Sales-Agent Example

### 2.1 Use Case: "Find conversation with Example Contact on 4/13/26"

**Skill Implementation Pattern**:

```python
# skills/sales/retrieve-past-conversations.md

def retrieve_past_conversations(person: str, date: str, topic: str = None):
    """
    Sales Agent retrieves historical context before outreach.
    Uses Hermes memory toolset which queries both Graphify and Khoj.
    """
    
    # 1. Normalize date (handles "4/13/26" → "2026-04-13")
    normalized_date = normalize_date(date)
    
    # 2. Build search query
    query = f"conversation with {person}"
    if topic:
        query += f" about {topic}"
    
    # 3. Call Hermes memory tool
    results = memory.search(
        query=query,
        filters={
            "date_after": normalized_date,
            "date_before": add_days(normalized_date, 1),
            "source_types": ["pdf", "markdown", "chat", "email"]
        }
    )
    
    # 4. Return unified, ranked results
    return format_conversation_results(results)
```

### 2.2 How It Works

```
Sales Agent triggers memory.search("Example Contact", date="2026-04-13")
    ↓
Hermes memory router dispatches to:
    ├── Graphify: Check if "Example Contact" exists in indexed graph nodes
    │           Returns: nodes with conversations, linked via EXTRACTED edges
    │
    └── Khoj: Search content + conversation stores
            Returns: ranked snippets from chat history, documents
    ↓
Both results merged:
    - Sources from Khoj chat logs (conversations)
    - PDF/md files mentioning "Example Contact" from both systems
    - Graph relationships showing context connections
    ↓
Ranked output with source attribution:
    1. [khoj chat] "2026-04-13 conversation with Example Contact about Q2 pipeline..."
    2. [graphify pdf] "contract-jose-2026-04-13.pdf - page 2..."
    3. [khoj doc] "jose-notes.md - meeting summary..."
```

---

## 3. APIs & Endpoints to Connect

### 3.1 Graphify Endpoints (via MCP)

| Endpoint | Method | Purpose | Notes |
|----------|--------|---------|-------|
| `/graph/query` | POST | Semantic graph queries | MCP tool: `mcp_graphify_query` |
| `/graph/path` | POST | Find paths between nodes | MCP tool: `mcp_graphify_path` |
| `/graph/explain` | POST | Explain a concept/node | MCP tool: `mcp_graphify_explain` |
| `/graph/nodes` | GET | List all nodes | Filter by type, source file |
| `/graph/edges` | GET | List relationships | Includes confidence labels |
| `/mcp` | stdio | MCP server mode | Native Hermes integration |

**MCP Config**:
```yaml
mcp_servers:
  graphify:
    command: "uvx"
    args: ["graphifyy", "--mcp"]
    env:
      OPENAI_API_KEY: "sk-..."  # For extraction if needed
```

### 3.2 Khoj Endpoints (via HTTP API)

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/content/search` | POST | Search indexed documents | Yes (Bearer token) |
| `/api/memories` | GET | List user memories | Yes |
| `/api/memories/{id}` | GET | Get specific memory | Yes |
| `/api/chat/history` | GET | Conversation history | Yes |
| `/api/chat/message` | POST | Add to conversation log | Yes |
| `/api/content` | PUT/PATCH | Index new content | Yes |

**Authentication**:
- JWT token via `/api/auth` endpoint
- Or API key header: `Authorization: Bearer sk-xxx`

**HTTP MCP Config**:
```yaml
mcp_servers:
  khoj:
    url: "http://localhost:5000/mcp"
    headers:
      Authorization: "Bearer ${KHOJ_API_KEY}"
```

---

## 4. Installation & Configuration

### 4.1 Prerequisites

| Component | Version | Install |
|-----------|---------|---------|
| Python | 3.10+ | System package |
| Node.js | 18+ | Required for npx-based MCP servers |
| Hermes Agent | Latest | `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \| bash` |

### 4.2 Graphify Setup

```bash
# Install Graphify (currently named graphifyy on PyPI)
pip install graphifyy

# Install into Hermes (optional, for direct integration)
hermes skills install graphify-integration

# Or via MCP
cat >> ~/.hermes/config.yaml << EOF
mcp_servers:
  graphify:
    command: "uvx"
    args: ["graphifyy", "--mcp"]
    timeout: 180
EOF
```

### 4.3 Khoj Setup

**Option A: Docker (Recommended)**
```bash
docker run -d \
  --name khoj \
  -p 5000:5000 \
  -v ~/.khoj:/root/.khoj \
  khojai/khoj:latest
```

**Option B: Python**
```bash
pip install khoj
khoj start --port 5000
```

**Environment Variables**:
```bash
# ~/.hermes/.env
KHOJ_API_KEY=sk-khoj-local-xxxx
KHOJ_BASE_URL=http://localhost:5000
GRAPHIFY_API_KEY=sk-openai-xxxx  # Only if Graphify needs extraction
```

### 4.4 Hermes Configuration

```yaml
# ~/.hermes/config.yaml

# Enable memory toolset
toolsets:
  - memory

# Configure providers
memory:
  provider: mcp  # Use MCP-based memory
  graphity_path: "~/.hermes/graphify-out/graph.json"
  khoj_url: "http://localhost:5000"

# MCP servers
mcp_servers:
  graphify:
    command: "uvx"
    args: ["graphifyy", "--mcp"]
    timeout: 180
    
  khoj:
    url: "http://localhost:5000/mcp"
    headers:
      Authorization: "Bearer ${KHOJ_API_KEY}"
```

### 4.5 Skill Registration

Add memory tools to sales-agent skill:

```markdown
---
name: sales-agent
triggers:
  - "/sales"
  - "find conversation"
  - "past discussion"
---

# Sales Agent

Before outreach, use `memory.search()` to gather context.

## Memory Integration

- `memory.search("name", filters={"date": "X"})` — query both systems
- `memory.get_context("topic")` — get related concepts from graph
- `memory.add_conversation(text, participants)` — save to Khoj
```

---

## 5. Security Recommendations

### 5.1 Graphify Security Audit

| Aspect | Finding | Recommendation |
|--------|---------|----------------|
| **License** | MIT ✅ | Approved for commercial use |
| **Owner Type** | Organization ✅ | Verified GitHub org |
| **Stars** | 81,518 ⭐ | Healthy community adoption |
| **Security Policy** | Yes (SECURITY.md) ✅ | Good vulnerability reporting |
| **Eval/Exec Patterns** | None found ✅ | Safe from code injection |
| **Network Calls** | Minimal (URL fetch only) ✅ | Limited attack surface |
| **Path Traversal** | Blocked in security.py ✅ | Uses `validate_graph_path()` |
| **SSRF Protection** | `validate_url()` + redirect blocking ✅ | Only http/https allowed |

**Key Security Features**:
- No `shell=True` in subprocess (explicit in SECURITY.md)
- Content streaming with 50MB cap
- HTML sanitization on node labels
- Symlink traversal blocked

### 5.2 Khoj Security Audit

| Aspect | Finding | Recommendation |
|--------|---------|----------------|
| **License** | AGPL-3.0 ⚠️ | Copyleft - be aware of derivative distribution requirements |
| **Owner Type** | Organization ✅ | Verified khoj-ai org |
| **Stars** | 35,614 ⭐ | Good adoption |
| **Security Policy** | No dedicated SECURITY.md | Recommend adding security.md |
| **Eval/Exec Patterns** | Check runners.py for code execution ⚠️ | Has `run_code` tool - restrict in production |

**Key Security Considerations**:
- AGPL license may require open-sourcing modifications
- Code execution tool (`run_code`) exists - disable for untrusted users
- All endpoints require authentication
- Runs as FastAPI server - expose only to localhost

### 5.3 Integration Security

| Concern | Mitigation |
|---------|------------|
| **Credential Leakage** | Use Hermes env filtering - only explicitly passed env vars reach MCP servers |
| **Cross-System Injection** | Both systems sanitize input; Hermes adds LLM-side validation |
| **Data Exposure** | Khoj requires auth per-user; Graphify files stored locally |
| **Network Exposure** | Khoj server binds to localhost by default; use reverse proxy with auth for remote |

**Recommended `.env` Setup**:
```bash
# File: ~/.hermes/.env
# Restrict permissions
chmod 600 ~/.hermes/.env

# API keys
KHOJ_API_KEY=sk-local-xxxx  # Generate via khoj config
OPENAI_API_KEY=sk-openai-xxxx  # Only if using Graphify extraction

# Security
KHOJ_BASE_URL=http://127.0.0.1:5000  # Never 0.0.0.0
```

### 5.4 Production Hardening

```yaml
# ~/.hermes/config.yaml

security:
  tirith_enabled: true  # Content filtering
  website_blocklist:
    - "pastebin.com"
    - "github.com/gist"  # Prevent data leakage to public pastebins

memory:
  # Restrict Khoj code execution features
  khoj_disable_tools:
    - "run_code"
    - "shell_command"
```

---

## 6. Deployment Checklist

- [ ] Install Hermes Agent with `pip install mcp` for MCP support
- [ ] Install Khoj: `docker run -d -p 4200:4200 khojai/khoj` (REQUIRED)
- [ ] Install Graphify: `pip install graphifyy` (REQUIRED)
- [ ] Configure `.env` with API keys
- [ ] Add MCP servers to `~/.hermes/config.yaml`
- [ ] Restart Hermes gateway: `hermes gateway restart`
- [ ] Verify tools: `hermes tools list | grep mcp`
- [ ] Test query: `/memory search "test"`
- [ ] Install sales-agent skill: `cp skills/sales/*.md ~/.hermes/skills/`
- [ ] **Optional**: Verify Voicebox running on port 17493, test `/voicebox "hello"`

### Component Requirements

| Component | Required | Notes |
|-----------|----------|-------|
| Khoj | **Required** | Memory/search layer, no Khoj = no memory queries |
| Graphify | **Required** | Semantic filtering, speeds up context retrieval |
| Voicebox | Optional | TTS - only if you need audio output |

**Workflow**: User query → Cortex checks both Khoj + Graphify availability → Routes to skills layer

### Optional Integrations

| Component | Optional | Setup |
|-----------|----------|-------|
| Voicebox TTS | Yes | Ensure Docker container on port 17493 |
| Graphify | Yes | `pip install graphifyy` or skip MCP config |
| Khoj | Yes | Skip if using alternative memory store |

All skills gracefully skip optional components if unavailable.

---

## Appendix: Quick Reference

### Confidence Score Mapping

| Source | Label | Hermes Weight |
|--------|-------|---------------|
| Graphify | EXTRACTED | 0.9 |
| Graphify | INFERRED | 0.6 |
| Graphify | AMBIGUOUS | 0.3 |
| Khoj | similarity > 0.8 | 0.8 |
| Khoj | similarity > 0.5 | 0.5 |
| Khoj | similarity <= 0.5 | 0.2 |

### Example Query Flow

```
User: "Find Example Contact conversation from April"
    ↓
Hermes: memory.search("Example Contact", date_range="2026-04")
    ↓
Graphify: Query graph for "Example Contact" nodes → found in metadata.md
Khoj: Search chat logs → found 3 conversations with Example Contact
    ↓
Merged: [
  {source: "khoj/chat", date: "2026-04-13", confidence: 0.85, snippet: "..."},
  {source: "graphify/md", date: "2026-04-10", confidence: 0.6, excerpt: "..."}
]
```