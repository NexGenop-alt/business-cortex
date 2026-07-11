# {{ company.name }} Company OS

This folder defines the company-agent operating layer for **{{ company.name }}**.

## Purpose

{{ system.name }} supports {{ company.name }} by coordinating role-specific agents
without mixing their memories.

## Company Direction

- **Industry:** {{ company.industry }}
- **Mission:** {{ company.mission }}
- **Primary goal:** {{ company.primary_goal }}
- **Owner / executive contact:** {{ company.owner_name }}

## Agent Structure

| Agent | Profile | Title |
|---|---|---|
| {{ agents.orchestrator.display_name }} | `{{ agents.orchestrator.profile }}` | {{ agents.orchestrator.title }} |
| {{ agents.techops.display_name }} | `{{ agents.techops.profile }}` | {{ agents.techops.title }} |
| {{ agents.scout.display_name }} | `{{ agents.scout.profile }}` | {{ agents.scout.title }} |
| {{ agents.assistant.display_name }} | `{{ agents.assistant.profile }}` | {{ agents.assistant.title }} |
| {{ agents.sales.display_name }} | `{{ agents.sales.profile }}` | {{ agents.sales.title }} |

## Critical Memory Rule

Specialists do not absorb each other's memories. The orchestrator sends small,
task-specific handoff packets and receives results back.

## First Setup Steps

1. Review `agent-map.yaml`.
2. Review each file in `souls/`.
3. Create Hermes profiles or map these roles to existing worker agents.
4. Connect only the integrations required for the first workflow.
5. Start with one workflow, preferably lead follow-up or internal reminders.
