# Company OS Template

This template turns the internal company-agent structure into a reusable blueprint
for another business.

It creates a client-specific operating folder with:

- `agent-map.yaml` — agent departments, scopes, memory boundaries, and approval policy.
- `handoff-protocol.md` — how the orchestrator delegates without memory contamination.
- `souls/` — starter role instructions for each agent profile.
- `README.md` — client-specific overview.

## Important Principle

The orchestrator can coordinate the company-wide operating picture. Specialists
keep isolated profile memory and only receive task-specific handoff packets.

This avoids the failure mode where every agent remembers every other agent's
context and later uses the wrong information.

## Usage

Copy the example config:

```bash
cp templates/company-os/company-config.example.yaml /tmp/acme-company.yaml
```

Edit the company name, slug, goals, agent names, and integrations.

Render the company OS:

```bash
python3 templates/company-os/scripts/render-company-os.py \
  --config /tmp/acme-company.yaml \
  --output /tmp/acme-company-os
```

For a real local deployment, set output somewhere like:

```text
/opt/business-cortex/clients/<client_slug>/company-os
```

## Generated Files

```text
README.md
agent-map.yaml
handoff-protocol.md
souls/orchestrator.md
souls/techops.md
souls/scout.md
souls/assistant.md
souls/sales.md
```

## What This Is Not

This does not train a model. It creates the operating rules, memory boundaries,
and delegation structure around the model so the system starts aligned with the
company and improves as it learns from real work.
