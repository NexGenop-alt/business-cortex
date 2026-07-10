import json
import tempfile
import unittest
from pathlib import Path

from cortex.core.dispatcher import DispatchResult, DryRunDispatcher, HermesCliDispatcher
from cortex.core.models import HandoffTask
from cortex.core.store import CortexStore


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "cortex.sqlite"
        self.store = CortexStore(str(self.db_path))
        self.task = HandoffTask(
            agent_key="sales",
            agent_name="Sales Agent",
            instruction="Draft a concise follow-up message.",
            payload={"person": "Maria", "company": "Bright Plumbing", "pain": "missed-call follow-up automation"},
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_dispatch_persists_prompt_without_calling_agent(self):
        dispatcher = DryRunDispatcher(self.store)

        result = dispatcher.dispatch(self.task)

        self.assertEqual(result.status, "dry_run")
        self.assertEqual(result.agent_key, "sales")
        self.assertIn("Draft a concise follow-up", result.output)
        records = self.store.list_handoff_runs()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["agent_key"], "sales")
        self.assertEqual(records[0]["status"], "dry_run")
        self.assertIn("Bright Plumbing", records[0]["prompt"])

    def test_hermes_cli_dispatch_builds_token_minimal_prompt_and_records_output(self):
        calls = []

        def fake_runner(command, *, timeout):
            calls.append(command)
            return 0, "sales draft output", ""

        dispatcher = HermesCliDispatcher(self.store, command_runner=fake_runner)

        result = dispatcher.dispatch(self.task, profile="sales")

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.output, "sales draft output")
        self.assertEqual(len(calls), 1)
        self.assertIn("hermes --profile sales chat -q", calls[0])
        self.assertLess(len(calls[0]), 1800)
        records = self.store.list_handoff_runs()
        self.assertEqual(records[0]["status"], "completed")
        self.assertEqual(records[0]["output"], "sales draft output")

    def test_dispatch_result_serializes_cleanly(self):
        result = DispatchResult(agent_key="assistant", status="completed", output="ok", prompt="prompt")
        data = result.to_dict()
        self.assertEqual(json.loads(json.dumps(data))["agent_key"], "assistant")


if __name__ == "__main__":
    unittest.main()
