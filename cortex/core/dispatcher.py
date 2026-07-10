"""Dispatch role-specific handoffs to specialist agents.

The dispatcher is the piece that removes copy/paste from an operator workflow.
Business Cortex produces small HandoffTask packets; dispatchers decide how to
run them: dry-run for review, Hermes CLI for local profiles, or future adapters
for queues/API workers.
"""

from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import asdict, dataclass
from typing import Callable, Protocol

from cortex.core.models import HandoffTask
from cortex.core.store import CortexStore


@dataclass(frozen=True)
class DispatchResult:
    agent_key: str
    status: str
    output: str
    prompt: str
    exit_code: int = 0
    error: str = ""
    run_id: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class Dispatcher(Protocol):
    def dispatch(self, task: HandoffTask, **kwargs) -> DispatchResult:
        ...


def build_handoff_prompt(task: HandoffTask) -> str:
    """Build a compact, role-specific prompt for an agent.

    Do not include full chat history here. The payload is the context boundary.
    """

    payload = json.dumps(task.payload, indent=2, sort_keys=True)
    approval = "yes" if task.approval_required else "no"
    return (
        f"You are receiving a Business Cortex handoff.\n"
        f"Agent: {task.agent_name} ({task.agent_key})\n"
        f"Approval required before external side effects: {approval}\n\n"
        f"Instruction:\n{task.instruction}\n\n"
        f"Context payload:\n{payload}\n\n"
        "Return only the requested work product plus any critical next-step note. "
        "Do not invent missing facts."
    )


class DryRunDispatcher:
    def __init__(self, store: CortexStore):
        self.store = store

    def dispatch(self, task: HandoffTask, **kwargs) -> DispatchResult:
        prompt = build_handoff_prompt(task)
        output = f"DRY RUN for {task.agent_name}\n\n{prompt}"
        run_id = self.store.add_handoff_run(
            agent_key=task.agent_key,
            agent_name=task.agent_name,
            status="dry_run",
            prompt=prompt,
            output=output,
        )
        return DispatchResult(
            agent_key=task.agent_key,
            status="dry_run",
            output=output,
            prompt=prompt,
            run_id=run_id,
        )


CommandRunner = Callable[[str], tuple[int, str, str]]


def default_command_runner(command: str, *, timeout: int = 180) -> tuple[int, str, str]:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


class HermesCliDispatcher:
    def __init__(self, store: CortexStore, command_runner=None, timeout: int = 300):
        self.store = store
        self.command_runner = command_runner or default_command_runner
        self.timeout = timeout

    def dispatch(self, task: HandoffTask, *, profile: str | None = None, **kwargs) -> DispatchResult:
        prompt = build_handoff_prompt(task)
        profile_name = profile or task.agent_key
        command = f"hermes --profile {shlex.quote(profile_name)} chat -q {shlex.quote(prompt)} --quiet"
        code, stdout, stderr = self.command_runner(command, timeout=self.timeout)
        status = "completed" if code == 0 else "failed"
        output = stdout.strip() if stdout.strip() else stderr.strip()
        run_id = self.store.add_handoff_run(
            agent_key=task.agent_key,
            agent_name=task.agent_name,
            status=status,
            prompt=prompt,
            output=output,
            error=stderr.strip() if code != 0 else "",
            exit_code=code,
        )
        return DispatchResult(
            agent_key=task.agent_key,
            status=status,
            output=output,
            prompt=prompt,
            exit_code=code,
            error=stderr.strip() if code != 0 else "",
            run_id=run_id,
        )
