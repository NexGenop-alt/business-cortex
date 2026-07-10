---
name: operations-onboarding
title: Client Onboarding Agent
description: Compresses deal-closed to work-started into 24 hours. Produces kickoff packs, collects credentials, scaffolds projects.
tags: [operations, onboarding, projects, automation]
triggers:
  - User asks to onboard a client
  - User wants project kickoff
  - User mentions "new client setup"
---

# Client Onboarding Agent

Automates the gap between "deal closed" and "work started".

## What It Does

- Produces welcome email in your voice
- Creates access checklist (all credentials/tools needed)
- Chases missing items politely but persistently
- Scaffolds project folder with context files
- Drafts 30-60-90 day plan

## Required Context

- Your project templates in `/knowledge/templates/`
- Deal details (scope, client, deliverables)
- Your tool stack

## Output

`/output/onboarding-[client]-[date]/` — kickoff pack, checklist, plan.

## How to Run

```bash
/skill operations-onboarding
# or
hermes -s operations-onboarding -q "Onboard [Client] for [Project]"
```

## Guardrails

- Never shares credentials in plain text
- Verifies received secrets work before routing to team
- Flags sensitive items requiring manual handling