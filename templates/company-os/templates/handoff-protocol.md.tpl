# Company Agent Handoff Protocol — {{ company.name }}

This file defines how the company-agent system coordinates work without memory
contamination.

## Core Rule

Specialists do not need each other's memories. They need task packets.

```text
{{ company.owner_name }} / leadership -> {{ agents.orchestrator.display_name }} -> specialist profile -> result -> {{ agents.orchestrator.display_name }} / leadership
```

The orchestrator can keep the company-wide operating picture. Specialists stay
narrow and role-specific.

## Handoff Packet Format

Use this format when sending work to another profile:

```md
# Handoff

## From
{{ agents.orchestrator.display_name }} / leadership / <agent>

## To
techops / scout / assistant / sales

## Objective
What needs to be done.

## Relevant Context
Only the context required for this task.

## Constraints
Rules, limits, deadlines, approval requirements.

## Desired Output
What the specialist should return.

## Do Not Touch
Systems, memories, files, actions, or assumptions to avoid.

## Approval Rule
Draft only / recommend only / execute after approval / safe read-only check.
```

## Routing Table

| Request | Route |
|---|---|
| Server, gateways, integrations, credentials, systems, troubleshooting | {{ agents.techops.display_name }} |
| Skills, tools, new capabilities, workflow expansion research | {{ agents.scout.display_name }} |
| Calendar, reminders, assistant work, follow-up tasks, workspace support | {{ agents.assistant.display_name }} |
| Emails, outreach, sales copy, offers, objections, close plans | {{ agents.sales.display_name }} |
| Strategy, prioritization, orchestration, final review | {{ agents.orchestrator.display_name }} |

## Memory Rules

- Do not paste entire memories between profiles.
- Do not ask one specialist to become another specialist.
- If a lesson affects all agents, the orchestrator turns it into an operating rule.
- If a lesson is role-specific, save it only in that role's memory or skill.
- Secrets and credentials never belong in handoff packets.
