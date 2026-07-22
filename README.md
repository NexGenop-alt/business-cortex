# Business Cortex

**Business Cortex is a productized AI operating system for companies.**

It gives a business one unified assistant that can remember context, route work
to role-specific agents, and keep durable business state without stuffing every
conversation and document into every prompt.

Think: **Jarvis for a business** — but configurable per client and deployable on
their own infrastructure.

## What it does

Business Cortex connects four layers:

```text
Business request
    ↓
Cortex Router / Workflow Engine
    ↓
Durable business state + memory lookup
    ↓
Role-specific specialist agents
    ├── Sales
    ├── Marketing
    ├── Support
    ├── Operations
    └── Back Office
```

The goal is not to make one giant prompt. The goal is to send each specialist
only the small context packet it needs.

## Why it saves tokens

Most agent systems waste tokens by passing the whole business history to every
agent. Business Cortex uses a smaller pattern:

1. Classify the request.
2. Save or retrieve only the durable state needed.
3. Build a tiny role-specific handoff packet.
4. Require human approval before external side effects.
5. Store the result for the next workflow.

Example:

```text
"Follow up with Maria from Bright Plumbing in 5 business days."
```

Business Cortex turns that into:

- a Sales handoff with pain + offer + CTA requirements
- an Assistant handoff with calendar timing + memo
- a CRM activity stored in SQLite
- a next action requiring approval

## Quick start

```bash
git clone <business-cortex-repo-url>
cd business-cortex
python3 -m unittest discover -v
python3 -m cortex.cli run --config config/client.example.json \
  "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am." \
  --format json

# Preview the specialist handoffs without calling external agents
python3 -m cortex.cli run \
  "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am." \
  --config config/client.example.json \
  --dispatch dry-run \
  --format json
```

## Client configuration

Every client gets its own config. This keeps the product industry-agnostic.

```bash
python3 -m cortex.cli init-client config/plumbing-co.json \
  --name "Bright Plumbing" \
  --industry "home services"
```

Then edit:

```text
config/plumbing-co.json
```

Key sections:

| Section | Purpose |
|---|---|
| `organization` | Client name and industry |
| `offer` | What the client sells / what automations should optimize for |
| `agents` | Role-specific workers and their profiles |
| `storage` | Local SQLite state path |
| `integrations.google_workspace` | Gmail, Calendar, Drive, Docs, Sheets via GWS |
| `integrations.microsoft_azure` | Microsoft 365 / Graph via Azure app credentials |

## Current MVP workflows

### Lead follow-up workflow

Input:

```text
Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am.
```

Output:

```text
workflow: lead_followup
handoff: sales -> Sales Agent
handoff: assistant -> Assistant Agent
next_action: approve_sales_message
```

Persisted state:

- lead record
- lead intake activity
- follow-up reminder request
- stage update to `followup_drafted`

## Architecture

```text
cortex/
├── cli.py                    # product CLI
├── core/
│   ├── orchestrator.py        # router + workflow engine
│   ├── models.py              # handoff/result models
│   └── store.py               # embedded CRM/workflow SQLite store
├── skills/                    # role-specific skill documents
└── tools/                     # audit / support tools
```

## Existing integrations

The repo still includes planned integration design for:

| Component | Purpose |
|---|---|
| Khoj | indexed organizational memory/search |
| Graphify | semantic knowledge graph / relationship map |
| Voicebox | optional local TTS |
| Hermes Agent | multi-agent runtime + skills + gateways |

These are integration layers. The MVP core is intentionally usable before a
client commits to the full stack.

## Human approval gates

Business Cortex should draft and prepare. It should not send emails, create
calendar invites, or touch external systems without approval unless a client
explicitly configures that automation level.

## Product direction

Subscription target:

```text
$500-$2,500/month per client
```

Positioning:

> Business Cortex consolidates organizational memory, semantic knowledge, and
> role-specific agents into one business assistant. It helps small teams get the
> leverage of sales, marketing, support, and operations workflows without hiring
> a full $13k-$22k/month human team.

## Test

```bash
python3 -m unittest discover -v
```

## Client onboarding questionnaire

Use the onboarding questionnaire to capture how a client thinks, decides,
communicates, sells, handles risk, and defines success before configuring the
agent system:

```text
docs/client-onboarding-questionnaire.md
```

The completed answers should be converted into client config, operating rules,
workflow maps, approval policy, memory seeds, role-agent definitions, and a
first-30-days implementation plan.

## Company OS template

Use the reusable company-agent OS template to turn a client's config into an
operating folder with agent roles, memory boundaries, approval rules, and a
handoff protocol:

```bash
python3 templates/company-os/scripts/render-company-os.py \
  --config templates/company-os/company-config.example.yaml \
  --output /tmp/example-company-os
```

Template location:

```text
templates/company-os/
```

## Hermes runtime setup

Use the setup runbook to install Hermes on Linux, macOS, Windows, or WSL2 and apply the correct Business Cortex memory boundaries:

```text
docs/setup/hermes-install-and-runbook.md
```

Core rule: all specialist agents use the client Private Brain + Skill Tree as their primary knowledge layer instead of Hermes profile-local memory.

## Client account login plans

Business Cortex can print safe setup/login plans for client-owned Google
Workspace and Microsoft Azure/M365 accounts:

```bash
python3 -m cortex.cli auth login google_workspace --config config/client.example.json
python3 -m cortex.cli auth login microsoft_azure --config config/client.example.json
```

AWS login is intentionally not included yet; add it later only when the product
needs AWS infrastructure automation for clients.
