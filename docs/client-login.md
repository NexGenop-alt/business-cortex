# Client login setup: Google Workspace and Microsoft Azure

Business Cortex needs a repeatable way to connect each client's own business
accounts. This repo now includes **login plan builders** for Google Workspace and
Microsoft Azure/Microsoft 365.

AWS is intentionally **not enabled yet**. It can be added later when the product
needs cloud infrastructure automation, but for the current business workflow we
keep the login surface smaller and safer.

## Print a Google Workspace login plan

```bash
python3 -m cortex.cli auth login google_workspace \
  --config config/client.example.json
```

The plan uses the client's configured home directory and prints commands like:

```bash
mkdir -p /opt/business-cortex/clients/acme-home-services/home/.config/gws
cp $GOOGLE_CLIENT_SECRET_JSON /opt/business-cortex/clients/acme-home-services/home/.config/gws/client_secret.json
HOME=/opt/business-cortex/clients/acme-home-services/home gws auth login --services gmail,calendar,drive,sheets,docs
HOME=/opt/business-cortex/clients/acme-home-services/home gws auth status
```

Credential rule:

- The OAuth JSON file path may be provided by `GOOGLE_CLIENT_SECRET_JSON` or by a
  client config path.
- The actual JSON secret file and OAuth token files must never be committed.

## Print a Microsoft Azure / Microsoft 365 login plan

```bash
python3 -m cortex.cli auth login microsoft_azure \
  --config config/client.example.json
```

The plan uses environment variable names, not secret values:

```bash
az login --service-principal --tenant $AZURE_TENANT_ID --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET
az account show
az rest --method GET --url https://graph.microsoft.com/v1.0/me
```

Credential rule:

- `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` are set in the
  deployment environment or secrets manager.
- Do not store Azure secrets in `config/*.json`.

## JSON output

For installers or dashboards:

```bash
python3 -m cortex.cli auth login google_workspace \
  --config config/client.example.json \
  --format json
```

This returns a serializable login plan with:

- provider
- auth kind
- commands
- prerequisites
- env var names
- safety notes
