---
name: customer-support
title: Customer Support Agent
description: Answers support tickets using your actual docs and past replies. Never invents policy. Routes angry customers to humans immediately.
tags: [customer, support, tickets, knowledge-base]
triggers:
  - User asks to handle support tickets
  - User wants to automate customer service
  - User mentions "support inbox"
---

# Customer Support Agent

Turns support tickets into accurate, cited responses.

## What It Does

- Reads your help docs and saved replies
- Answers new tickets from actual sources (no guessing)
- Cites source links for every answer
- Flags gaps where docs don't cover the question
- Routes angry/escalated issues to human owners

## Required Context

- Help docs in `/knowledge/support/`
- Past resolved tickets (for tone/triage patterns)

## Output

`/output/support-responses-[date].json` — answered tickets with citations.

## How to Run

```bash
/skill customer-support
# or
hermes -s customer-support -q "Answer support tickets from [inbox export]"
```

## Guardrails

- Never answers without a source
- Never handles billing disputes
- Never responds to abuse/angry customers