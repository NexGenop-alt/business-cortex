"""Core data models for Business Cortex."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class AgentSpec:
    key: str
    name: str
    profile: str
    role: str
    description: str = ""


@dataclass(frozen=True)
class HandoffTask:
    agent_key: str
    agent_name: str
    instruction: str
    payload: Dict[str, Any]
    approval_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CortexResult:
    workflow: str
    summary: str
    next_action: str
    handoffs: List[HandoffTask] = field(default_factory=list)
    lead_id: Optional[int] = None
    organization: str = ""
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["handoffs"] = [task.to_dict() for task in self.handoffs]
        return data
