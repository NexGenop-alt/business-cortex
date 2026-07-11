import json
import unittest

from cortex.auth.providers import AuthLoginBuilder, build_login_plan


class AuthLoginBuilderTest(unittest.TestCase):
    def test_builds_google_workspace_login_plan_without_secrets(self):
        config = {
            "integrations": {
                "google_workspace": {
                    "enabled": True,
                    "home": "/clients/acme/home",
                    "services": ["gmail", "calendar", "drive"],
                    "client_secret_path": "/secure/acme/google-client-secret.json",
                }
            }
        }

        plan = build_login_plan("google_workspace", config)

        self.assertEqual(plan.provider, "google_workspace")
        self.assertEqual(plan.kind, "oauth")
        self.assertTrue(any("gws auth login" in command for command in plan.commands))
        self.assertTrue(any("HOME=/clients/acme/home" in command for command in plan.commands))
        self.assertTrue(any("--services gmail,calendar,drive" in command for command in plan.commands))
        self.assertIn("/secure/acme/google-client-secret.json", plan.prerequisites)
        self.assertNotIn("oauth-secret-prefix", json.dumps(plan.to_dict()).lower())

    def test_builds_azure_login_plan_using_env_names_not_secret_values(self):
        config = {
            "integrations": {
                "microsoft_azure": {
                    "enabled": True,
                    "tenant_id_env": "AZURE_TENANT_ID",
                    "client_id_env": "AZURE_CLIENT_ID",
                    "client_secret_env": "AZURE_CLIENT_SECRET",
                    "scopes": ["https://graph.microsoft.com/.default"],
                }
            }
        }

        plan = build_login_plan("microsoft_azure", config)

        self.assertEqual(plan.provider, "microsoft_azure")
        self.assertEqual(plan.kind, "service_principal")
        serialized = json.dumps(plan.to_dict())
        self.assertIn("az login --service-principal", plan.commands[0])
        self.assertIn("$AZURE_CLIENT_SECRET", plan.commands[0])
        self.assertIn("AZURE_TENANT_ID", serialized)
        self.assertNotIn("secret-value", serialized)

    def test_aws_is_out_of_scope_until_explicitly_enabled(self):
        builder = AuthLoginBuilder({"integrations": {"aws": {"enabled": True}}})
        with self.assertRaises(ValueError):
            builder.build("aws")

    def test_unknown_provider_fails_clearly(self):
        builder = AuthLoginBuilder({"integrations": {}})
        with self.assertRaises(ValueError):
            builder.build("unknown")


if __name__ == "__main__":
    unittest.main()
