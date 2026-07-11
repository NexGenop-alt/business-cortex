#!/usr/bin/env python3
"""Productized Business Cortex orchestrator.

The orchestrator is intentionally tenant-agnostic: it can run for any
client by swapping configuration. It does three things:

1. Classify a business request into a workflow.
2. Persist the minimum durable business state.
3. Produce role-specific handoff packets so specialist agents receive only the
   context they need.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

from cortex.core.models import AgentSpec, CortexResult, HandoffTask
from cortex.core.store import CortexStore


DEFAULT_CONFIG: Dict[str, Any] = {
    "organization": {"name": "Client Organization", "industry": "general business"},
    "agents": {
        "orchestrator": {"name": "Business Cortex", "profile": "default", "role": "strategy"},
        "sales": {"name": "Sales Agent", "profile": "sales", "role": "sales"},
        "assistant": {"name": "Assistant Agent", "profile": "assistant", "role": "calendar"},
        "support": {"name": "Support Agent", "profile": "support", "role": "customer_success"},
        "operations": {"name": "Operations Agent", "profile": "operations", "role": "ops"},
    },
    "storage": {"sqlite_path": ".cortex/cortex.sqlite"},
    "offer": {
        "default": "business automation / AI workflow improvement",
        "followup": "follow-up automation that prevents missed opportunities",
    },
}


class BusinessCortex:
    def __init__(self, config: Mapping[str, Any]):
        self.config = {**DEFAULT_CONFIG, **dict(config)}
        self.organization = dict(DEFAULT_CONFIG["organization"])
        self.organization.update(dict(config.get("organization", {})))
        self.offer = dict(DEFAULT_CONFIG["offer"])
        self.offer.update(dict(config.get("offer", {})))
        self.agents = self._load_agents(config.get("agents", DEFAULT_CONFIG["agents"]))
        storage = dict(DEFAULT_CONFIG["storage"])
        storage.update(dict(config.get("storage", {})))
        self.store = CortexStore(storage["sqlite_path"])

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "BusinessCortex":
        return cls(config)

    @classmethod
    def from_json_file(cls, path: str) -> "BusinessCortex":
        data = json.loads(Path(path).expanduser().read_text())
        return cls(data)

    def _load_agents(self, raw_agents: Mapping[str, Any]) -> Dict[str, AgentSpec]:
        agents: Dict[str, AgentSpec] = {}
        merged = dict(DEFAULT_CONFIG["agents"])
        merged.update(dict(raw_agents))
        for key, data in merged.items():
            agents[key] = AgentSpec(
                key=key,
                name=data.get("name", key.replace("_", " ").title()),
                profile=data.get("profile", key),
                role=data.get("role", key),
                description=data.get("description", ""),
            )
        return agents

    def run(self, text: str) -> CortexResult:
        workflow = self.classify(text)
        if workflow == "lead_followup":
            return self._lead_followup(text)
        if workflow == "sales":
            return self._sales_only(text)
        return self._general_business_request(text)

    def classify(self, text: str) -> str:
        t = text.lower()
        if any(word in t for word in ["lead", "prospect", "customer"]) and any(
            word in t for word in ["follow up", "follow-up", "email", "text", "call"]
        ):
            return "lead_followup"
        if any(word in t for word in ["cold email", "outreach", "proposal", "close", "deal", "icp"]):
            return "sales"
        return "general"

    def _lead_followup(self, text: str) -> CortexResult:
        lead = self._extract_lead(text)
        lead_id = self.store.create_lead(
            person=lead["person"],
            company=lead["company"],
            pain=lead["pain"],
            stage="intake",
        )
        self.store.add_activity(lead_id, kind="lead_intake", body=text)
        self.store.add_followup(
            lead_id,
            due_text=lead["due_text"],
            memo=f"Follow up with {lead['person']} at {lead['company']} about {lead['pain']}.",
            attendee=lead.get("attendee"),
        )
        self.store.update_lead_stage(lead_id, "followup_drafted")

        sales = self.agents["sales"]
        assistant = self.agents["assistant"]
        sales_task = HandoffTask(
            agent_key="sales",
            agent_name=sales.name,
            instruction="Draft a concise follow-up message. Do not schedule anything. Return message + subject/CTA only.",
            payload={
                "organization": self.organization["name"],
                "person": lead["person"],
                "company": lead["company"],
                "pain": lead["pain"],
                "offer": self.offer.get("followup", self.offer["default"]),
                "tone": "clear, practical, buyer-focused",
                "approval_gate": "human must approve before sending",
            },
        )
        assistant_task = HandoffTask(
            agent_key="assistant",
            agent_name=assistant.name,
            instruction="Prepare a calendar reminder only after the sales message is approved. Do not rewrite sales copy.",
            payload={
                "organization": self.organization["name"],
                "lead_id": lead_id,
                "person": lead["person"],
                "company": lead["company"],
                "due_text": lead["due_text"],
                "calendar_instruction": f"Create follow-up reminder for {lead['due_text']}.",
                "memo": f"Previous outreach will address: {lead['pain']}. Next step: confirm interest and book discovery.",
                "approval_gate": "human must approve calendar creation",
            },
        )
        return CortexResult(
            workflow="lead_followup",
            organization=self.organization["name"],
            lead_id=lead_id,
            summary=f"{self.organization['name']} captured lead {lead['person']} at {lead['company']} and prepared sales + calendar handoffs.",
            next_action="approve_sales_message",
            handoffs=[sales_task, assistant_task],
        )

    def _sales_only(self, text: str) -> CortexResult:
        sales = self.agents["sales"]
        return CortexResult(
            workflow="sales",
            organization=self.organization["name"],
            summary=f"{self.organization['name']} routed request to {sales.name}.",
            next_action="review_sales_output",
            handoffs=[
                HandoffTask(
                    agent_key="sales",
                    agent_name=sales.name,
                    instruction="Handle this sales request and return concise buyer-ready output.",
                    payload={"organization": self.organization["name"], "request": text[:700]},
                )
            ],
        )

    def _general_business_request(self, text: str) -> CortexResult:
        orchestrator = self.agents["orchestrator"]
        return CortexResult(
            workflow="general",
            organization=self.organization["name"],
            summary=f"{self.organization['name']} routed request to {orchestrator.name} for planning.",
            next_action="classify_or_plan",
            handoffs=[
                HandoffTask(
                    agent_key="orchestrator",
                    agent_name=orchestrator.name,
                    instruction="Clarify the business outcome, select specialists, and propose the next workflow.",
                    payload={"organization": self.organization["name"], "request": text[:700]},
                )
            ],
        )

    def _extract_lead(self, text: str) -> Dict[str, Optional[str]]:
        person = self._match_first(text, [r"Lead:\s*([A-Z][a-zA-Z'-]+)", r"(?:with|for)\s+([A-Z][a-zA-Z'-]+)"]) or "Unknown"
        company = self._match_first(
            text,
            [
                r"owns\s+([A-Z][A-Za-z0-9&' -]+?)(?:\.|,|\s+She\b|\s+He\b|\s+They\b|\s+needs\b)",
                r"at\s+([A-Z][A-Za-z0-9&' -]+?)(?:\.|,|\s+needs\b)",
            ],
        ) or "Unknown Company"
        pain = self._match_first(text, [r"needs\s+(.+?)(?:\.\s*Follow|\.\s*$|$)", r"pain[: ]+(.+?)(?:\.\s*Follow|$)"]) or "business workflow improvement"
        due_text = self._match_first(text, [r"Follow up\s+(.+?)(?:\.|$)", r"follow-up\s+(.+?)(?:\.|$)"]) or "next business day"
        attendee = self._match_first(text, [r"add\s+([\w.+-]+@[\w.-]+)\s+as\s+an?\s+attendee"])
        return {"person": person, "company": company.strip(), "pain": pain.strip(), "due_text": due_text.strip(), "attendee": attendee}

    @staticmethod
    def _match_first(text: str, patterns: list[str]) -> Optional[str]:
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None


# Backwards-compatible alias for the old README examples.
class Cortex(BusinessCortex):
    def __init__(self, config_path: str = ""):
        if config_path and Path(config_path).expanduser().exists():
            super().__init__(json.loads(Path(config_path).expanduser().read_text()))
        else:
            super().__init__(DEFAULT_CONFIG)

    def query(self, text: str) -> str:
        return json.dumps(self.run(text).to_dict(), indent=2)


cortex = Cortex()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(cortex.query(" ".join(sys.argv[1:])))
    else:
        print("Business Cortex orchestrator loaded. Query anything.")
