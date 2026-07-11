import json
import tempfile
import unittest
from pathlib import Path

from cortex.core.orchestrator import BusinessCortex
from cortex.core.store import CortexStore


class BusinessCortexProductMVPTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "cortex.sqlite"
        self.config = {
            "organization": {"name": "Demo Company", "industry": "home services"},
            "agents": {
                "orchestrator": {"name": "Orchestrator", "profile": "default", "role": "strategy"},
                "sales": {"name": "Revenue Agent", "profile": "sales", "role": "sales"},
                "assistant": {"name": "Ops Assistant", "profile": "assistant", "role": "calendar"},
            },
            "memory": {"provider": "stub"},
            "storage": {"sqlite_path": str(self.db_path)},
        }
        self.cortex = BusinessCortex.from_config(self.config)

    def tearDown(self):
        self.tmp.cleanup()

    def test_routes_sales_followup_to_sales_and_calendar_agents(self):
        result = self.cortex.run(
            "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am."
        )

        self.assertEqual(result.workflow, "lead_followup")
        self.assertEqual([task.agent_key for task in result.handoffs], ["sales", "assistant"])
        self.assertIn("Bright Plumbing", result.summary)
        self.assertEqual(result.next_action, "approve_sales_message")

    def test_workflow_persists_lead_activity_and_followup(self):
        result = self.cortex.run(
            "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am."
        )

        store = CortexStore(str(self.db_path))
        leads = store.list_leads()
        activities = store.list_activities(leads[0]["id"])
        followups = store.list_followups(leads[0]["id"])

        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0]["company"], "Bright Plumbing")
        self.assertEqual(leads[0]["stage"], "followup_drafted")
        self.assertEqual(activities[0]["kind"], "lead_intake")
        self.assertIn("missed-call", activities[0]["body"])
        self.assertIn("5 business days", followups[0]["due_text"])

    def test_handoff_payloads_are_token_minimal_and_role_specific(self):
        result = self.cortex.run(
            "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am."
        )

        sales_payload = result.handoffs[0].payload
        assistant_payload = result.handoffs[1].payload

        self.assertLess(len(json.dumps(sales_payload)), 900)
        self.assertLess(len(json.dumps(assistant_payload)), 900)
        self.assertIn("pain", sales_payload)
        self.assertIn("offer", sales_payload)
        self.assertNotIn("calendar_instruction", sales_payload)
        self.assertIn("calendar_instruction", assistant_payload)
        self.assertNotIn("offer", assistant_payload)

    def test_product_config_is_not_jay_specific(self):
        result = self.cortex.run(
            "Lead: Maria owns Bright Plumbing. She needs missed-call follow-up automation. Follow up in 5 business days at 10am."
        )
        serialized = json.dumps(result.to_dict()).lower()

        self.assertNotIn("jay", serialized)
        self.assertNotIn("nexgen", serialized)
        self.assertIn("demo company", serialized)


if __name__ == "__main__":
    unittest.main()
