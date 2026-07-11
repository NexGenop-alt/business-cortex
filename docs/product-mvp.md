# Product MVP: Business Cortex as a sellable machine

This document defines the non-Jay-specific machine that can be sold to many
businesses before being adapted to NexGen's internal agents.

## Product promise

Business Cortex gives a client one business assistant that:

1. remembers useful business context,
2. routes work to specialist agents,
3. stores the durable state of leads/tasks/follow-ups,
4. asks for approval before external side effects,
5. improves workflows over time.

## Core pattern

```text
request → classify → retrieve/save state → create role handoffs → approval → execute → learn
```

## Role map

| Role | Owns | Does not own |
|---|---|---|
| Orchestrator | planning, routing, next action | writing every artifact |
| Sales | ICP, outreach, proposals, objections | calendar execution |
| Assistant | reminders, calendar prep, admin memos | rewriting sales strategy |
| Support | support tickets/customer issues | new sales outreach |
| Operations | onboarding, SOPs, internal process | deal closing |
| Back Office | invoices, records, billing admin | sales copy |

## MVP workflow spine

The first finished workflow is **Lead → Sales Message → Follow-Up Reminder → Pipeline State**.

Why this first:

- it is easy for any business owner to understand,
- it directly touches revenue,
- it proves router + storage + handoff + approval gates,
- it maps to many industries.

## Client-agnostic rules

- Never hardcode Jay, NexGen, Memo, Revenue Chief, or Ace into product code.
- Client-specific names belong in config.
- External sending/scheduling is gated by approval by default.
- Specialist handoffs should be small enough to keep token cost low.
- Memory/search systems are optional integrations; durable state must still work locally.

## Done definition for machine v1

- [x] client config file
- [x] embedded workflow/CRM database
- [x] lead follow-up workflow
- [x] role-specific handoff payloads
- [x] dry-run and Hermes CLI dispatch layer
- [x] tests proving routing, state, token-minimal payloads, dispatch, and client-agnostic output
- [ ] live Hermes profile dispatch validation against real client profiles
- [ ] Khoj memory adapter
- [ ] Graphify adapter
- [x] Google Workspace adapter payloads/commands behind approval gates
- [x] Microsoft Azure / Graph adapter payloads behind approval gates
- [ ] live Google Workspace execution after approval
- [ ] live Microsoft Graph execution after approval
- [ ] web dashboard or simple operator UI
