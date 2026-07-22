# Business Cortex Memory Boundaries

This document defines the client-safe memory architecture for a Business Cortex deployment.
It is a reusable product template and must not include the template provider's internal data,
agent memories, private URLs, bot names, IDs, or credentials.

## Core model

```text
Client Private Brain = durable shared company knowledge
Client Skill Tree    = map of available workflows, tools, and agent capabilities
Hermes/runtime       = execution shell, gateway, tools, profiles, and orchestration
Specialist agents    = role-specific workers with bounded context
```

## Source-of-truth rule

For a client deployment, the **private brain** is the source of truth for durable business
knowledge. The **skill tree** is the source of truth for capability discovery. Specialist
profile memory is not the company brain.

## Orchestrator policy

The orchestrator may keep runtime/session continuity and company-wide coordination notes if
the deployment runtime supports it. The orchestrator may access the private brain and skill
tree, but it should still build small role-specific handoff packets instead of sending the
entire brain to every specialist.

## Specialist policy

All specialist agents should treat the private brain and skill tree as their primary knowledge
layer. In runtimes that support profile-local durable memory, specialist profile memory should
be disabled or treated as ephemeral unless the client explicitly opts in.

This rule applies to every specialist role in the deployment, including sales, assistant,
tech operations, support, operations, finance, legal, QA, knowledge, and CRM/contact roles.

Recommended specialist flags for a Hermes-backed deployment:

```yaml
memory:
  memory_enabled: false
  user_profile_enabled: false
  write_approval: true
```

## Ingestion policy

Only client-approved documents, notes, CRM exports, SOPs, transcripts, and operating artifacts
belong in the client's private brain. Do not upload template-provider internal data or raw
agent profile memory into a client deployment.

Never ingest:

- passwords, tokens, API keys, OAuth files, cookies, or session strings;
- unrelated internal company memories;
- another tenant's data;
- raw profile-memory dumps unless the client approves and they have been sanitized.

## Handoff boundary

Specialists receive task packets, not full memory dumps.

A handoff packet may include:

1. objective;
2. task-relevant retrieved context;
3. constraints;
4. desired output;
5. approval requirements;
6. what not to touch.

A handoff packet must not include unrelated memory, raw profile history, secrets, or private
context from other roles.

## Demo boundary

Internal deployments can be used as a proof-of-work demo, but the product repo must only
contain the reusable boundary pattern. Do not commit internal data from the demo company.
