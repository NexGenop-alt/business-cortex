---
name: intelligence-research
title: Market Intelligence Agent
description: Watches target accounts/companies for signals (hiring, funding, product launches). Scores relevance and suggests plays.
tags: [intelligence, research, signals, monitoring]
triggers:
  - User asks about market intel
  - User wants to track companies
  - User mentions "buying signals"
---

# Market Intelligence Agent

Turns target lists into live signal streams.

## What It Does

- Monitors job boards, news, social for target accounts
- Detects: funding rounds, hiring sprees, leadership moves
- Scores signals 1-10 against your ICP
- Suggests outreach plays per signal
- Runs on schedule (weekly, bi-weekly, monthly)

## Required APIs (optional)

- EXA_API_KEY (news search)
- APIFY_API_KEY (LinkedIn/company feeds)
- FIRECRAWL_API_KEY (website change detection)

## Output

`/output/signals-[period].json` — ranked signals with timing.

## How to Run

```bash
/skill intelligence-research
# or
hermes -s intelligence-research -q "Monitor targets: [paste list]"
```

## Example Signal

```
Acme Inc: Hiring 12 engineers in AI/ML (Jun 2026)
Signal Score: 8 (aligns with ICP expansion pattern)
Suggested Play: "Congrats on the hiring — scaling fast? We helped SimilarCo 2x their AI team productivity..."
```