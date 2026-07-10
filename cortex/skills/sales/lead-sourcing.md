---
name: lead-sourcing
title: Lead Sourcing Agent
description: Sources and enriches prospect lists per your ICP. Scrapes LinkedIn, job boards, and company feeds. Scores fit and writes personalized outreach lines.
tags: [sales, lead-gen, enrichment, scraping]
triggers:
  - User asks to find leads
  - User wants prospect lists
  - User mentions "how do we find customers"
---

# Lead Sourcing Agent

Turns ICP into actionable prospect lists with enrichment and scoring.

## What It Does

- Scrapes LinkedIn/company feeds for firms matching ICP
- Enriches contacts (emails, roles, recent activity)
- Scores each prospect against your ICP
- Writes 3-line personalized opening hooks per prospect
- Outputs a lead list ready for outreach campaigns

## Required APIs (optional but recommended)

- EXA_API_KEY (company intel)
- APIFY_API_KEY (LinkedIn scraping)
- FIRECRAWL_API_KEY (website analysis)

## Output

`/output/prospects-[vertical]-[date].csv` — ranked list with enrichment fields.

## How to Run

```bash
/skill lead-sourcing
# or
hermes -s lead-sourcing -q "Source leads for ICP: [paste ICP here]"
```

## Output Format

| Company | Contact | Role | Email | Score | Hook |
|---------|---------|------|-------|-------|------|
| Acme Inc | Jane Doe | VP Growth | ... | 85 | "Saw your 30% MoM growth..." |