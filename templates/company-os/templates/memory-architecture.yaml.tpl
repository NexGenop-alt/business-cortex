version: 1
company: "{{ company.name }}"
system: "{{ system.name }}"

principle: >
  The company private brain is the shared source of truth for durable business knowledge.
  The skill tree is the source of truth for available workflows and capabilities.
  Agent profile memory is not the client knowledge base.

source_of_truth:
  private_brain:
    type: "{{ memory_architecture.source_of_truth.type }}"
    label: "{{ memory_architecture.source_of_truth.label }}"
    purpose: "{{ memory_architecture.source_of_truth.purpose }}"
    local_url: "{{ memory_architecture.source_of_truth.local_url }}"
    public_route: "{{ memory_architecture.source_of_truth.public_route }}"
    stores_client_data: {{ memory_architecture.source_of_truth.stores_client_data | bool_lower }}
  skill_tree:
    label: "{{ memory_architecture.skill_tree.label }}"
    purpose: "{{ memory_architecture.skill_tree.purpose }}"

orchestrator_policy:
  runtime_primary: "{{ memory_architecture.orchestrator.runtime_primary }}"
  can_access_private_brain: {{ memory_architecture.orchestrator.can_access_private_brain | bool_lower }}
  can_access_skill_tree: {{ memory_architecture.orchestrator.can_access_skill_tree | bool_lower }}
  hermes_memory_enabled: {{ memory_architecture.orchestrator.hermes_memory_enabled | bool_lower }}
  rule: "{{ memory_architecture.orchestrator.rule }}"

specialist_policy:
  private_brain_primary: {{ memory_architecture.specialists.private_brain_primary | bool_lower }}
  skill_tree_primary: {{ memory_architecture.specialists.skill_tree_primary | bool_lower }}
  hermes_memory_enabled: {{ memory_architecture.specialists.hermes_memory_enabled | bool_lower }}
  hermes_user_profile_enabled: {{ memory_architecture.specialists.hermes_user_profile_enabled | bool_lower }}
  write_approval: {{ memory_architecture.specialists.write_approval | bool_lower }}
  rule: "{{ memory_architecture.specialists.rule }}"

memory_boundaries:
  do:
    - Retrieve only task-relevant context from the private brain.
    - Use the skill tree to discover available workflows and tools.
    - Keep role-specific handoff packets small and auditable.
    - Require approval before ingesting new client documents into the private brain.
  do_not:
    - Do not upload internal template-provider data into a client brain.
    - Do not store secrets, tokens, passwords, or OAuth material in the private brain.
    - Do not merge one specialist's role context into another specialist's profile memory.
    - Do not treat profile-local memory files as the company's source of truth.

ingestion_policy:
  raw_profile_memory_upload_allowed: {{ memory_architecture.ingestion_policy.raw_profile_memory_upload_allowed | bool_lower }}
  client_approved_documents_only: {{ memory_architecture.ingestion_policy.client_approved_documents_only | bool_lower }}
  preserve_role_boundaries: {{ memory_architecture.ingestion_policy.preserve_role_boundaries | bool_lower }}
  secrets_allowed: {{ memory_architecture.ingestion_policy.secrets_allowed | bool_lower }}
