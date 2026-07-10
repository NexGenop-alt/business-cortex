---
name: backoffice-billing
title: Billing Manager Agent
description: Generates branded invoices, tracks payments, and chases overdue accounts. Syncs with Stripe/QuickBooks or works offline.
tags: [back-office, finance, billing, automation]
triggers:
  - User asks about invoicing
  - User wants to track payments
  - User mentions "overdue invoices"
---

# Billing Manager Agent

Owns "deal closed" to "money in bank".

## What It Does

- Generates branded invoices from deal records
- Tracks payment status (Stripe live or manual)
- Chases overdue accounts on schedule
- Flags delinquent accounts for human escalation
- Produces monthly collections report

## Required APIs (optional)

- STRIPE_API_KEY (live payment status)
- QUICKBOOKS_API_KEY (accounting sync)

## Output

`/output/invoices-[month].pdf` + `/output/collections-[month].md`

## How to Run

```bash
/skill backoffice-billing
# or
hermes -s backoffice-billing -q "Invoice [Client] for [Amount]"
```

## Guardrails

- Never sends invoice without human review
- Respects payment terms exactly
- Escalates >90 days overdue to humans