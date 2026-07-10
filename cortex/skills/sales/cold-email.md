---
name: cold-email
title: Cold Email Agent
description: Writes personalized cold email sequences that get replies. Uses prospect intel and your ICP. Generates 3-email cadences with A/B hooks.
tags: [sales, outreach, copywriting, sequences]
triggers:
  - User asks to write cold emails
  - User wants outreach campaigns
  - User mentions "cold email sequence"
---

# Cold Email Agent

Generates persona-aligned cold email sequences with proven hooks.

## What It Does

- Reads prospect intel and ICP
- Writes 3-email cadence (research → value → CTA)
- Creates multiple hook variants for A/B testing
- Personalizes each email to the specific prospect's context
- Outputs ready-to-import .csv for Instantly, HubSpot, etc.

## Output

`/output/cold-email-[prospect-name]-[date].md` — formatted sequence.

## How to Run

```bash
/skill cold-email
# or
hermes -s cold-email -q "Write sequence for [prospect] targeting [vertical]"
```

## Example Output

```
Subject: Quick question on [company]'s retention

Hi [FirstName],

I noticed [specific signal] — 30% MoM growth in subscriptions.

We helped [similar company] solve [specific problem] with [your solution].

Want me to show you how we'd approach [company]?

[Signature]
```