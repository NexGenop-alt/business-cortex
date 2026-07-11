import json
import unittest

from cortex.integrations.google_workspace import GWSCalendarAdapter, GWSEmailAdapter
from cortex.integrations.microsoft_graph import AzureGraphCalendarAdapter, AzureGraphEmailAdapter


class IntegrationAdaptersTest(unittest.TestCase):
    def test_gws_calendar_adapter_builds_create_event_command_without_executing(self):
        adapter = GWSCalendarAdapter(home="/tmp/client-home")
        command = adapter.build_create_event_command(
            summary="Follow up with Maria - Bright Plumbing",
            start="2026-07-15T10:00:00-07:00",
            end="2026-07-15T10:30:00-07:00",
            attendees=["owner@example.com"],
            description="Discuss missed-call follow-up automation.",
        )

        self.assertIn("HOME=/tmp/client-home", command)
        self.assertIn("gws calendar events create", command)
        self.assertIn("--summary", command)
        self.assertIn("owner@example.com", command)
        self.assertNotIn("OperatorName", command)
        self.assertNotIn("InternalCompany", command)

    def test_gws_email_adapter_builds_draft_payload(self):
        adapter = GWSEmailAdapter(home="/tmp/client-home")
        payload = adapter.build_send_payload(
            to=["maria@example.com"],
            subject="Quick follow-up",
            body="Hi Maria — quick follow-up.",
            cc=["owner@example.com"],
        )

        self.assertEqual(payload["provider"], "google_workspace")
        self.assertEqual(payload["action"], "send_email")
        self.assertTrue(payload["approval_required"])
        self.assertEqual(payload["to"], ["maria@example.com"])
        self.assertEqual(payload["cc"], ["owner@example.com"])

    def test_azure_calendar_adapter_builds_graph_payload(self):
        adapter = AzureGraphCalendarAdapter(tenant_id="tenant", client_id="client")
        payload = adapter.build_create_event_payload(
            summary="Follow up with Maria - Bright Plumbing",
            start="2026-07-15T10:00:00-07:00",
            end="2026-07-15T10:30:00-07:00",
            attendees=["owner@example.com"],
            description="Discuss missed-call follow-up automation.",
        )

        self.assertEqual(payload["subject"], "Follow up with Maria - Bright Plumbing")
        self.assertEqual(payload["start"]["dateTime"], "2026-07-15T10:00:00-07:00")
        self.assertEqual(payload["attendees"][0]["emailAddress"]["address"], "owner@example.com")
        self.assertIn("body", payload)
        self.assertNotIn("tenant", json.dumps(payload).lower())

    def test_azure_email_adapter_builds_graph_sendmail_payload(self):
        adapter = AzureGraphEmailAdapter(tenant_id="tenant", client_id="client")
        payload = adapter.build_send_mail_payload(
            to=["maria@example.com"],
            subject="Quick follow-up",
            body="Hi Maria — quick follow-up.",
            cc=["owner@example.com"],
        )

        message = payload["message"]
        self.assertFalse(payload["saveToSentItems"] is False)
        self.assertEqual(message["subject"], "Quick follow-up")
        self.assertEqual(message["toRecipients"][0]["emailAddress"]["address"], "maria@example.com")
        self.assertEqual(message["ccRecipients"][0]["emailAddress"]["address"], "owner@example.com")


if __name__ == "__main__":
    unittest.main()
