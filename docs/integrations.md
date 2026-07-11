# Integrations: Google Workspace and Microsoft Azure

Business Cortex supports both Google-first and Microsoft-first clients. The
core workflow stays the same; the integration adapter changes per client.

## Design rules

- Keep integrations tenant-agnostic.
- Never hardcode operator names, company names, or a specific client.
- Build approval payloads first; execute only after approval.
- Store credentials outside git in environment variables or provider-specific
  OAuth stores.
- Keep generated payloads small so agents do not receive unnecessary history.

## Google Workspace

Use when a client runs on Gmail, Google Calendar, Drive, Docs, or Sheets.

Config example:

```json
{
  "integrations": {
    "google_workspace": {
      "enabled": true,
      "home": "/opt/business-cortex/clients/acme/home",
      "services": ["gmail", "calendar", "drive", "sheets", "docs"]
    }
  }
}
```

Credential model:

- OAuth Desktop/Web client per deployment or managed provider account.
- Token files live under the client's configured `home`, not in the repo.
- Actions are generated as approval payloads or GWS CLI commands.

Supported adapter helpers:

- `GWSCalendarAdapter.build_create_event_command(...)`
- `GWSCalendarAdapter.build_create_event_payload(...)`
- `GWSEmailAdapter.build_send_payload(...)`
- `GWSEmailAdapter.build_send_command(...)`

## Microsoft Azure / Microsoft Graph

Use when a client runs on Microsoft 365, Outlook, Teams, SharePoint, or Entra ID.

Config example:

```json
{
  "integrations": {
    "microsoft_azure": {
      "enabled": true,
      "tenant_id_env": "AZURE_TENANT_ID",
      "client_id_env": "AZURE_CLIENT_ID",
      "client_secret_env": "AZURE_CLIENT_SECRET",
      "scopes": ["https://graph.microsoft.com/.default"]
    }
  }
}
```

Credential model:

- Client creates an Azure App Registration.
- Secrets are passed by environment variables.
- Graph API execution should happen only after Business Cortex approval.

Common Microsoft Graph permissions to evaluate per client:

| Capability | Delegated/Application permissions to review |
|---|---|
| Send mail | `Mail.Send` |
| Read mail | `Mail.Read` |
| Calendar events | `Calendars.ReadWrite` |
| Files/SharePoint | `Files.ReadWrite.All`, `Sites.ReadWrite.All` |
| Users/org directory | `User.Read.All` |

Supported adapter helpers:

- `AzureGraphCalendarAdapter.build_create_event_payload(...)`
- `AzureGraphCalendarAdapter.build_approval_payload(...)`
- `AzureGraphEmailAdapter.build_send_mail_payload(...)`
- `AzureGraphEmailAdapter.build_approval_payload(...)`

## Next execution layer

The current adapters build safe commands/payloads. The next layer should add:

1. approval records in the database,
2. `cortex approve <run_id>`,
3. Google execution adapter,
4. Microsoft Graph token acquisition + execution adapter,
5. audit log for every external side effect.
