version: 1
company:
  name: "{{ company.name }}"
  slug: "{{ company.slug }}"
  owner_name: "{{ company.owner_name }}"
  industry: "{{ company.industry }}"
  mission: "{{ company.mission }}"
  primary_goal: "{{ company.primary_goal }}"

system:
  name: "{{ system.name }}"
  principle: "{{ system.principle }}"

agents:
  orchestrator:
    profile: "{{ agents.orchestrator.profile }}"
    display_name: "{{ agents.orchestrator.display_name }}"
    title: "{{ agents.orchestrator.title }}"
    reports_to: "{{ agents.orchestrator.reports_to }}"
    scope: {{ agents.orchestrator.scope | yaml_inline }}
    memory_access:
      runtime_primary: "{{ memory_architecture.orchestrator.runtime_primary }}"
      private_brain_access: {{ memory_architecture.orchestrator.can_access_private_brain | bool_lower }}
      skill_tree_access: {{ memory_architecture.orchestrator.can_access_skill_tree | bool_lower }}
      profile_memory_enabled: {{ memory_architecture.orchestrator.hermes_memory_enabled | bool_lower }}
      may_merge_specialist_memory: false

  techops:
    profile: "{{ agents.techops.profile }}"
    display_name: "{{ agents.techops.display_name }}"
    title: "{{ agents.techops.title }}"
    scope: {{ agents.techops.scope | yaml_inline }}
    memory_access:
      private_brain_primary: {{ memory_architecture.specialists.private_brain_primary | bool_lower }}
      skill_tree_primary: {{ memory_architecture.specialists.skill_tree_primary | bool_lower }}
      profile_memory_enabled: {{ memory_architecture.specialists.hermes_memory_enabled | bool_lower }}
      user_profile_enabled: {{ memory_architecture.specialists.hermes_user_profile_enabled | bool_lower }}
      write_approval: {{ memory_architecture.specialists.write_approval | bool_lower }}
      may_read_other_profiles: false
      may_merge_memory: false

  scout:
    profile: "{{ agents.scout.profile }}"
    display_name: "{{ agents.scout.display_name }}"
    title: "{{ agents.scout.title }}"
    scope: {{ agents.scout.scope | yaml_inline }}
    memory_access:
      private_brain_primary: {{ memory_architecture.specialists.private_brain_primary | bool_lower }}
      skill_tree_primary: {{ memory_architecture.specialists.skill_tree_primary | bool_lower }}
      profile_memory_enabled: {{ memory_architecture.specialists.hermes_memory_enabled | bool_lower }}
      user_profile_enabled: {{ memory_architecture.specialists.hermes_user_profile_enabled | bool_lower }}
      write_approval: {{ memory_architecture.specialists.write_approval | bool_lower }}
      may_read_other_profiles: false
      may_merge_memory: false

  assistant:
    profile: "{{ agents.assistant.profile }}"
    display_name: "{{ agents.assistant.display_name }}"
    title: "{{ agents.assistant.title }}"
    scope: {{ agents.assistant.scope | yaml_inline }}
    memory_access:
      private_brain_primary: {{ memory_architecture.specialists.private_brain_primary | bool_lower }}
      skill_tree_primary: {{ memory_architecture.specialists.skill_tree_primary | bool_lower }}
      profile_memory_enabled: {{ memory_architecture.specialists.hermes_memory_enabled | bool_lower }}
      user_profile_enabled: {{ memory_architecture.specialists.hermes_user_profile_enabled | bool_lower }}
      write_approval: {{ memory_architecture.specialists.write_approval | bool_lower }}
      may_read_other_profiles: false
      may_merge_memory: false

  sales:
    profile: "{{ agents.sales.profile }}"
    display_name: "{{ agents.sales.display_name }}"
    title: "{{ agents.sales.title }}"
    scope: {{ agents.sales.scope | yaml_inline }}
    memory_access:
      private_brain_primary: {{ memory_architecture.specialists.private_brain_primary | bool_lower }}
      skill_tree_primary: {{ memory_architecture.specialists.skill_tree_primary | bool_lower }}
      profile_memory_enabled: {{ memory_architecture.specialists.hermes_memory_enabled | bool_lower }}
      user_profile_enabled: {{ memory_architecture.specialists.hermes_user_profile_enabled | bool_lower }}
      write_approval: {{ memory_architecture.specialists.write_approval | bool_lower }}
      may_read_other_profiles: false
      may_merge_memory: false

handoff_policy:
  default: minimal_context_only
  include:
    - objective
    - relevant_context
    - constraints
    - desired_output
    - approval_requirements
    - what_not_to_touch
  exclude:
    - unrelated_memory
    - raw_profile_history
    - secrets
    - private_context_from_other_agents

approval_policy:
  drafts_allowed: {{ approval_policy.drafts_allowed | bool_lower }}
  external_send_requires_approval: {{ approval_policy.external_send_requires_approval | bool_lower }}
  calendar_changes_require_approval: {{ approval_policy.calendar_changes_require_approval | bool_lower }}
  destructive_system_changes_require_approval: {{ approval_policy.destructive_system_changes_require_approval | bool_lower }}
  memory_merges_require_approval: {{ approval_policy.memory_merges_require_approval | bool_lower }}

integrations:
  google_workspace:
    enabled: {{ integrations.google_workspace.enabled | bool_lower }}
  microsoft_365:
    enabled: {{ integrations.microsoft_365.enabled | bool_lower }}
  crm:
    enabled: {{ integrations.crm.enabled | bool_lower }}
    name: "{{ integrations.crm.name }}"
