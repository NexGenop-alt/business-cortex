"""Google Workspace adapter helpers.

These helpers are intentionally side-effect free by default. They build commands
or approval payloads that the workflow engine can store, display, and later run
after a human approves the action.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import Iterable, List


def _csv(values: Iterable[str]) -> str:
    return ",".join(v for v in values if v)


@dataclass(frozen=True)
class GWSCalendarAdapter:
    home: str | None = None

    def build_create_event_command(
        self,
        *,
        summary: str,
        start: str,
        end: str,
        attendees: List[str] | None = None,
        description: str = "",
        calendar: str = "primary",
    ) -> str:
        parts = []
        if self.home:
            parts.append(f"HOME={shlex.quote(self.home)}")
        parts.extend(
            [
                "gws",
                "calendar",
                "events",
                "create",
                "--calendar",
                shlex.quote(calendar),
                "--summary",
                shlex.quote(summary),
                "--start",
                shlex.quote(start),
                "--end",
                shlex.quote(end),
            ]
        )
        if attendees:
            parts.extend(["--attendees", shlex.quote(_csv(attendees))])
        if description:
            parts.extend(["--description", shlex.quote(description)])
        return " ".join(parts)

    def build_create_event_payload(self, **kwargs) -> dict:
        return {
            "provider": "google_workspace",
            "action": "create_calendar_event",
            "approval_required": True,
            "command": self.build_create_event_command(**kwargs),
            "params": kwargs,
        }


@dataclass(frozen=True)
class GWSEmailAdapter:
    home: str | None = None

    def build_send_payload(
        self,
        *,
        to: List[str],
        subject: str,
        body: str,
        cc: List[str] | None = None,
        bcc: List[str] | None = None,
    ) -> dict:
        return {
            "provider": "google_workspace",
            "action": "send_email",
            "approval_required": True,
            "to": to,
            "cc": cc or [],
            "bcc": bcc or [],
            "subject": subject,
            "body": body,
        }

    def build_send_command(self, *, to: List[str], subject: str, body: str, cc: List[str] | None = None) -> str:
        parts = []
        if self.home:
            parts.append(f"HOME={shlex.quote(self.home)}")
        parts.extend(
            [
                "gws",
                "gmail",
                "send",
                "--to",
                shlex.quote(_csv(to)),
                "--subject",
                shlex.quote(subject),
                "--body",
                shlex.quote(body),
            ]
        )
        if cc:
            parts.extend(["--cc", shlex.quote(_csv(cc))])
        return " ".join(parts)
