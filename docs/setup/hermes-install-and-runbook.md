# Hermes Install and Business Cortex Runbook

This runbook explains how to install Hermes Agent and run a Business Cortex-style company-agent system the right way for a client deployment.

Authoritative Hermes reference: <https://hermes-agent.nousresearch.com/docs/>

## 1. Target architecture

Business Cortex uses Hermes as the runtime and execution layer, but the client knowledge architecture is separate:

```text
Client Private Brain = durable shared company knowledge
Client Skill Tree    = approved workflows, tools, skills, and agent capabilities
Hermes Runtime       = CLI, profiles, gateways, tools, cron, dispatcher, and execution shell
Orchestrator         = coordinates the company-wide operating picture
Specialists          = role-specific agents with bounded context
```

## 2. Non-negotiable memory boundary

All specialist agents must use the **client Private Brain + Skill Tree** as their primary knowledge layer.

Specialist agents must not treat Hermes profile-local memory as the company brain.

Recommended Hermes-backed specialist profile settings:

```bash
hermes --profile <specialist-profile> config set memory.memory_enabled false
hermes --profile <specialist-profile> config set memory.user_profile_enabled false
hermes --profile <specialist-profile> config set memory.write_approval true
```

The orchestrator may keep Hermes runtime continuity if the deployment requires it, but it must still retrieve only task-relevant private-brain context and send minimal handoff packets.

Recommended orchestrator settings:

```bash
hermes config set memory.memory_enabled true
hermes config set memory.user_profile_enabled true
```

If the orchestrator also runs under a named profile, replace `hermes` with `hermes --profile <orchestrator-profile>`.

## 3. Install Hermes

### Option A — Desktop installer for macOS or Windows

For macOS or Windows users who want both the desktop app and CLI, use the Hermes Desktop installer from the official website:

```text
https://hermes-agent.nousresearch.com/docs/getting-started/installation
```

After installing, open a terminal and verify:

```bash
hermes doctor
hermes setup
```

### Option B — Linux, macOS, WSL2, or Android Termux CLI install

Official shell installer:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

If the shell cannot find `hermes` after install, add the user-local bin directory to PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For `zsh`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify:

```bash
hermes doctor
```

### Linux prerequisites when needed

The installer handles most dependencies, but minimal Linux images may need these first.

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y curl xz-utils git
```

For Hermes Desktop or native-module builds on Debian/Ubuntu:

```bash
sudo apt install -y build-essential
```

### Headless/server install without browser automation

For a server where browser automation is not needed:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-browser
```

### Option C — Native Windows CLI install

Run this in PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then verify in a new PowerShell window:

```powershell
hermes doctor
hermes setup
```

If the CLI is not found, close and reopen PowerShell so PATH changes reload.

### Option D — PyPI install for controlled Python environments

Use this only when you intentionally manage Python and dependencies yourself:

```bash
pip install hermes-agent
```

Or with `uv`:

```bash
uv pip install hermes-agent
```

Then run:

```bash
hermes doctor
hermes setup
```

## 4. First Hermes setup

Run the guided setup:

```bash
hermes setup
```

Or configure provider/model interactively:

```bash
hermes model
```

Useful checks:

```bash
hermes doctor
hermes status --all
hermes tools list
hermes skills list
```

Fastest official provider path, when using Nous Portal:

```bash
hermes setup --portal
```

## 5. Create Business Cortex profiles

Create one orchestrator and separate specialist profiles. Profile names should be client-safe and role-based.

Example:

```bash
hermes profile create orchestrator
hermes profile create techops
hermes profile create scout
hermes profile create assistant
hermes profile create sales
hermes profile create support
hermes profile create operations
```

Do not clone another client's memories into a new client's profiles.

If cloning a base profile for tools/config, review the clone result and remove tenant-specific data before use.

## 6. Apply Business Cortex memory boundaries

Set specialist profiles to use Private Brain + Skill Tree instead of Hermes profile memory:

```bash
for profile in techops scout assistant sales support operations; do
  hermes --profile "$profile" config set memory.memory_enabled false
  hermes --profile "$profile" config set memory.user_profile_enabled false
  hermes --profile "$profile" config set memory.write_approval true
done
```

Keep the orchestrator as the coordination layer:

```bash
hermes --profile orchestrator config set memory.memory_enabled true
hermes --profile orchestrator config set memory.user_profile_enabled true
```

Verify:

```bash
for profile in orchestrator techops scout assistant sales support operations; do
  echo "== $profile =="
  hermes --profile "$profile" config get memory.memory_enabled
  hermes --profile "$profile" config get memory.user_profile_enabled
  hermes --profile "$profile" config get memory.write_approval
done
```

Expected pattern:

```text
orchestrator memory_enabled=true, user_profile_enabled=true
specialists  memory_enabled=false, user_profile_enabled=false, write_approval=true
```

## 7. Private Brain and Skill Tree rules

The private brain should ingest only client-approved knowledge:

- SOPs;
- client onboarding answers;
- CRM exports approved by the client;
- meeting notes/transcripts approved by the client;
- company docs, policies, offers, FAQs, and workflows;
- generated operating artifacts approved for reuse.

Never ingest:

- passwords, tokens, API keys, OAuth files, cookies, or session strings;
- another tenant's data;
- raw template-provider internal memory;
- unrelated agent conversation history;
- private data that the client did not approve for indexing.

The Skill Tree should track capabilities, workflows, and agent skills — not secrets or raw private memory.

## 8. Handoff protocol

The orchestrator sends specialists minimal packets:

```md
# Handoff

## Objective
What needs to be done.

## Relevant Context
Only task-relevant private-brain retrieval or client-provided context.

## Constraints
Rules, limits, deadlines, and approvals.

## Desired Output
What the specialist should return.

## Do Not Touch
Systems, memories, files, accounts, or assumptions to avoid.

## Approval Rule
Draft only / recommend only / execute after approval / safe read-only check.
```

Do not send the full private brain, another specialist's memory, raw profile logs, or secrets.

## 9. Run Hermes locally

Interactive chat:

```bash
hermes
```

Single command:

```bash
hermes chat -q "Summarize the Business Cortex memory boundary policy."
```

Run under a specific profile:

```bash
hermes --profile sales chat -q "Draft a follow-up message from this approved handoff packet: ..."
```

Load a skill:

```bash
hermes --profile orchestrator --skills business-cortex chat
```

## 10. Run messaging gateways

Configure messaging platforms:

```bash
hermes --profile orchestrator gateway setup
```

Install gateway as a background service where supported:

```bash
hermes --profile orchestrator gateway install
hermes --profile orchestrator gateway start
hermes --profile orchestrator gateway status
```

Repeat for specialist profiles only when the deployment intentionally exposes those specialists to a channel.

For most client deployments, prefer:

```text
human/user -> orchestrator channel -> role-scoped specialist handoff
```

instead of letting every specialist freely answer everywhere.

## 11. Verification checklist

Run these before calling a deployment ready:

```bash
hermes doctor
hermes profile list
hermes status --all
```

Check specialist memory flags:

```bash
for profile in techops scout assistant sales support operations; do
  echo "== $profile =="
  hermes --profile "$profile" config get memory.memory_enabled
  hermes --profile "$profile" config get memory.user_profile_enabled
done
```

Check gateway status if gateways are enabled:

```bash
hermes --profile orchestrator gateway status
```

Test a safe dry-run handoff before connecting real email/calendar/CRM adapters.

## 12. Approval gates

Human approval is required before:

- sending emails or messages externally;
- creating, deleting, or changing calendar events;
- changing credentials, access policies, DNS, servers, or infrastructure;
- deleting files or data;
- publishing code, public posts, or client-facing content;
- ingesting sensitive or broad memory exports;
- merging role memories or changing memory-source policy.

## 13. Update and troubleshoot

Update Hermes:

```bash
hermes update
```

Config diagnostics:

```bash
hermes config check
hermes config migrate
hermes doctor
```

Common first fixes:

```bash
hermes setup
hermes model
hermes tools
```

If config changes do not apply, start a new CLI session or restart the gateway:

```bash
hermes --profile orchestrator gateway restart
```

## 14. Product-template rule

This runbook is a reusable deployment template. Keep it generic.

Do not commit:

- real client private-brain data;
- internal demo-company memory;
- real bot usernames;
- phone numbers, chat IDs, or platform IDs;
- tokens, passwords, API keys, or OAuth files;
- private domains or local home-directory paths.
