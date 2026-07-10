"""SQLite storage for portable Business Cortex deployments."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class CortexStore:
    """Small embedded CRM/workflow store.

    This is intentionally boring and portable: every client can run it on their
    own infrastructure before graduating to HubSpot, Salesforce, Airtable, etc.
    """

    def __init__(self, sqlite_path: str):
        self.path = Path(sqlite_path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person TEXT NOT NULL,
                    company TEXT NOT NULL,
                    pain TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    source TEXT NOT NULL DEFAULT 'cortex',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER NOT NULL,
                    kind TEXT NOT NULL,
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lead_id) REFERENCES leads(id)
                );

                CREATE TABLE IF NOT EXISTS followups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER NOT NULL,
                    due_text TEXT NOT NULL,
                    attendee TEXT,
                    memo TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending_approval',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lead_id) REFERENCES leads(id)
                );
                """
            )

    def create_lead(self, *, person: str, company: str, pain: str, stage: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO leads(person, company, pain, stage) VALUES (?, ?, ?, ?)",
                (person, company, pain, stage),
            )
            return int(cur.lastrowid)

    def update_lead_stage(self, lead_id: int, stage: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE leads SET stage = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (stage, lead_id),
            )

    def add_activity(self, lead_id: int, *, kind: str, body: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO activities(lead_id, kind, body) VALUES (?, ?, ?)",
                (lead_id, kind, body),
            )
            return int(cur.lastrowid)

    def add_followup(self, lead_id: int, *, due_text: str, memo: str, attendee: Optional[str] = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO followups(lead_id, due_text, attendee, memo) VALUES (?, ?, ?, ?)",
                (lead_id, due_text, attendee, memo),
            )
            return int(cur.lastrowid)

    def list_leads(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM leads ORDER BY id").fetchall()
            return [dict(row) for row in rows]

    def list_activities(self, lead_id: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM activities WHERE lead_id = ? ORDER BY id", (lead_id,)).fetchall()
            return [dict(row) for row in rows]

    def list_followups(self, lead_id: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM followups WHERE lead_id = ? ORDER BY id", (lead_id,)).fetchall()
            return [dict(row) for row in rows]
