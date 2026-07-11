"""Microsoft Azure / Microsoft Graph adapter helpers.

The product should support Microsoft-first businesses as well as Google-first
businesses. These helpers build Graph API payloads without requiring live Azure
credentials during workflow planning or tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


def _recipient(address: str) -> dict:
    return {"emailAddress": {"address": address}}


@dataclass(frozen=True)
class AzureGraphConfig:
    tenant_id: str
    client_id: str
    authority_host: str = "https://login.microsoftonline.com"
    graph_base_url: str = "https://graph.microsoft.com/v1.0"


@dataclass(frozen=True)
class AzureGraphCalendarAdapter:
    tenant_id: str
    client_id: str
    graph_base_url: str = "https://graph.microsoft.com/v1.0"

    def build_create_event_payload(
        self,
        *,
        summary: str,
        start: str,
        end: str,
        attendees: List[str] | None = None,
        description: str = "",
        timezone: str = "UTC",
    ) -> dict:
        return {
            "subject": summary,
            "body": {"contentType": "HTML", "content": description},
            "start": {"dateTime": start, "timeZone": timezone},
            "end": {"dateTime": end, "timeZone": timezone},
            "attendees": [
                {**_recipient(email), "type": "required"}
                for email in (attendees or [])
            ],
            "allowNewTimeProposals": True,
        }

    def build_approval_payload(self, **kwargs) -> dict:
        return {
            "provider": "microsoft_graph",
            "action": "create_calendar_event",
            "approval_required": True,
            "endpoint": f"{self.graph_base_url}/me/events",
            "payload": self.build_create_event_payload(**kwargs),
        }


@dataclass(frozen=True)
class AzureGraphEmailAdapter:
    tenant_id: str
    client_id: str
    graph_base_url: str = "https://graph.microsoft.com/v1.0"

    def build_send_mail_payload(
        self,
        *,
        to: List[str],
        subject: str,
        body: str,
        cc: List[str] | None = None,
        bcc: List[str] | None = None,
        save_to_sent_items: bool = True,
    ) -> dict:
        return {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": body},
                "toRecipients": [_recipient(email) for email in to],
                "ccRecipients": [_recipient(email) for email in (cc or [])],
                "bccRecipients": [_recipient(email) for email in (bcc or [])],
            },
            "saveToSentItems": save_to_sent_items,
        }

    def build_approval_payload(self, **kwargs) -> dict:
        return {
            "provider": "microsoft_graph",
            "action": "send_email",
            "approval_required": True,
            "endpoint": f"{self.graph_base_url}/me/sendMail",
            "payload": self.build_send_mail_payload(**kwargs),
        }
