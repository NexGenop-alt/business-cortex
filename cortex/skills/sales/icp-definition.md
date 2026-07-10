---
name: icp-definition
title: ICP Definition Agent
description: Defines and refines Ideal Customer Profiles per vertical — firmographics, pain patterns, buying triggers. Uses your existing deals and market intel to identify who actually buys.
tags: [sales, targeting, lead-gen, strategy]
triggers:
  - User asks about ideal customer profile
  - User wants to improve targeting
  - User mentions "who should we sell to"
---

# ICP Definition Agent

Creates and refines Ideal Customer Profiles using real data from your business.

## What It Does

Reads your existing deals, churn, pricing pages, and market context to produce:
- **Firmographic profile** (size, industry, location filters)
- **Pain pattern mapping** (what problems they actually have)
- **Buying trigger signals** (events that precede a purchase)
- **Exclusion criteria** (who you never want to sell to)

## Required Context

- Your existing customer list or deal history (CSV, CRM export, or manually pasted)
- Your pricing tiers
- Your target markets (industries/geographies)

## Output

`/output/icp-[vertical].md` — structured ICP document ready for the Lead Sourcing skill.

## How to Run

```bash
/skill icp-definition
# or
hermes -s icp-definition -q "Define ICP for [vertical]"
```

## Example

**Input:**
> Our closed deals in the last 12 months

**Output:**
> ## ICP: Mid-Market E-commerce Brands\n> Firmographics: $10M-100M ARR, Shopify+, Paid Ads spend >$100k/mo\n> Pain: Cart abandonment, retention, LTV\n> Triggers: Holiday season, funding rounds, retention team hires