# Business Cortex — Production Integration Layer

A unified AI operating system combining semantic graphs, organizational memory, and business skills.

---

## 🚀 What This Repo Contains

This is the **integration layer only** — clean, minimal, production-ready.

| Layer | Purpose | Source Repo |
|---|---|---|
| Cortex Orchestrator | Query router and API glue | This repo |
| Skills | Business automation agents | `/cortex/skills/` |
| Tools | Utilities and auditors | `/cortex/tools/` |

---

## 📦 Full Sources

Khoj and Graphify are integrated as **git submodules** for lightweight updates:

```bash
git clone --recursive https://github.com/NexGenop-alt/business-cortex
# or after clone:
git submodule update --init --recursive
```

---

## 🛠️ Installation

```bash
# 1. Clone with submodules
git clone --recursive https://github.com/NexGenop-alt/business-cortex
cd business-cortex

# 2. Install services (Khoj + Graphify)
./bin/install-services.sh

# 3. Install Python deps
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env with your API keys

# 5. Start
./bin/start-all.sh
```

---

## 🔍 Query Examples

```python
from cortex.orchestrator import cortex

# Memory queries
cortex.query("Find conversation with Jose on 4/13/26")

# Code queries  
cortex.query("Show code that handles payments")

# Business operations
cortex.query("Source leads matching my ICP")
```

---

## 📁 Structure

```
business-cortex/
├── .gitmodules       # Khoj + Graphify as submodules
├── bin/
│   ├── install-services.sh
│   └── start-all.sh
├── cortex/
│   ├── core/orchestrator.py
│   ├── skills/       # 7 business agent skills
│   └── tools/
├── requirements.txt
└── integration_design.md
```