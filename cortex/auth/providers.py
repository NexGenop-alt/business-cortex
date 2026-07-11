"""Secret-safe login plan builders for external providers.

Business Cortex should help each client connect their own Google Workspace and
Microsoft Azure/M365 accounts without committing credentials to git.
This module builds human/operator-readable login plans using file paths and
environment variable names only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class AuthLoginPlan:
    provider: str
    kind: str
    commands: list[str]
    prerequisites: list[str] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AuthLoginBuilder:
    def __init__(self, config: Mapping[str, Any]):
        self.config = config
        self.integrations = dict(config.get("integrations", {}))

    def build(self, provider: str) -> AuthLoginPlan:
        if provider == "google_workspace":
            return self._google_workspace()
        if provider == "microsoft_azure":
            return self._microsoft_azure()
        raise ValueError(f"Unsupported auth provider: {provider}")

    def _provider_config(self, provider: str) -> dict[str, Any]:
        return dict(self.integrations.get(provider, {}))

    def _google_workspace(self) -> AuthLoginPlan:
        cfg = self._provider_config("google_workspace")
        home = cfg.get("home", "./client-home")
        services = cfg.get("services", ["gmail", "calendar"])
        client_secret_path = cfg.get("client_secret_path") or "$GOOGLE_CLIENT_SECRET_JSON"
        service_arg = ",".join(services)
        return AuthLoginPlan(
            provider="google_workspace",
            kind="oauth",
            prerequisites=[str(client_secret_path)],
            env_vars=[] if cfg.get("client_secret_path") else ["GOOGLE_CLIENT_SECRET_JSON"],
            commands=[
                f"mkdir -p {home}/.config/gws",
                f"cp {client_secret_path} {home}/.config/gws/client_secret.json",
                f"HOME={home} gws auth login --services {service_arg}",
                f"HOME={home} gws auth status",
            ],
            notes=[
                "Use the client's Google account/workspace, not the operator's account.",
                "OAuth token files stay under the client home directory and must not be committed.",
            ],
        )

    def _microsoft_azure(self) -> AuthLoginPlan:
        cfg = self._provider_config("microsoft_azure")
        tenant_env = cfg.get("tenant_id_env", "AZURE_TENANT_ID")
        client_env = cfg.get("client_id_env", "AZURE_CLIENT_ID")
        secret_env = cfg.get("client_secret_env", "AZURE_CLIENT_SECRET")
        return AuthLoginPlan(
            provider="microsoft_azure",
            kind="service_principal",
            env_vars=[tenant_env, client_env, secret_env],
            commands=[
                f"az login --service-principal --tenant ${tenant_env} --username ${client_env} --password ${secret_env}",
                "az account show",
                "az rest --method GET --url https://graph.microsoft.com/v1.0/me",
            ],
            notes=[
                "Create an Azure App Registration / service principal per client tenant.",
                "Store tenant/client/secret values in environment variables or a secrets manager, never in git.",
                "Grant only the Graph permissions the client approved.",
            ],
        )


def build_login_plan(provider: str, config: Mapping[str, Any]) -> AuthLoginPlan:
    return AuthLoginBuilder(config).build(provider)
