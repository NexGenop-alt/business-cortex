import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO / "templates" / "company-os"
RENDERER = TEMPLATE_ROOT / "scripts" / "render-company-os.py"
CONFIG = TEMPLATE_ROOT / "company-config.example.yaml"


class CompanyOSMemoryBoundaryTemplateTest(unittest.TestCase):
    def test_example_config_defines_private_brain_primary_specialists(self):
        data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
        memory = data["memory_architecture"]

        self.assertEqual(memory["source_of_truth"]["type"], "private_brain")
        self.assertTrue(memory["specialists"]["private_brain_primary"])
        self.assertTrue(memory["specialists"]["skill_tree_primary"])
        self.assertFalse(memory["specialists"]["hermes_memory_enabled"])
        self.assertFalse(memory["specialists"]["hermes_user_profile_enabled"])
        self.assertTrue(memory["specialists"]["write_approval"])
        self.assertTrue(memory["orchestrator"]["hermes_memory_enabled"])
        self.assertFalse(memory["ingestion_policy"]["raw_profile_memory_upload_allowed"])
        self.assertFalse(memory["ingestion_policy"]["secrets_allowed"])

    def test_renderer_outputs_memory_architecture_and_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "company-os"
            subprocess.run(
                [sys.executable, str(RENDERER), "--config", str(CONFIG), "--output", str(out)],
                check=True,
                cwd=REPO,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            memory_arch = yaml.safe_load((out / "memory-architecture.yaml").read_text(encoding="utf-8"))
            agent_map = yaml.safe_load((out / "agent-map.yaml").read_text(encoding="utf-8"))
            handoff = (out / "handoff-protocol.md").read_text(encoding="utf-8")
            sales_soul = (out / "souls" / "sales.md").read_text(encoding="utf-8")

            self.assertTrue(memory_arch["specialist_policy"]["private_brain_primary"])
            self.assertFalse(memory_arch["specialist_policy"]["hermes_memory_enabled"])
            self.assertFalse(memory_arch["specialist_policy"]["hermes_user_profile_enabled"])
            self.assertFalse(memory_arch["ingestion_policy"]["raw_profile_memory_upload_allowed"])
            self.assertFalse(memory_arch["ingestion_policy"]["secrets_allowed"])

            self.assertFalse(agent_map["agents"]["sales"]["memory_access"]["profile_memory_enabled"])
            self.assertTrue(agent_map["agents"]["sales"]["memory_access"]["private_brain_primary"])
            self.assertIn("private brain is the durable company knowledge source", handoff.lower())
            self.assertIn("private brain is the durable business knowledge source", sales_soul.lower())

    def test_hermes_setup_runbook_covers_install_and_memory_boundaries(self):
        runbook = (REPO / "docs" / "setup" / "hermes-install-and-runbook.md").read_text(encoding="utf-8")

        self.assertIn("curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash", runbook)
        self.assertIn("iex (irm https://hermes-agent.nousresearch.com/install.ps1)", runbook)
        self.assertIn("pip install hermes-agent", runbook)
        self.assertIn("uv pip install hermes-agent", runbook)
        self.assertIn("hermes setup", runbook)
        self.assertIn("hermes doctor", runbook)
        self.assertIn("memory.memory_enabled false", runbook)
        self.assertIn("memory.user_profile_enabled false", runbook)
        self.assertIn("memory.write_approval true", runbook)
        self.assertIn("All specialist agents must use the **client Private Brain + Skill Tree**", runbook)
        self.assertIn("Do not commit:", runbook)

    def test_template_uses_generic_client_safe_placeholders(self):
        scan_roots = [
            REPO / "docs" / "memory-boundaries.md",
            REPO / "docs" / "setup",
            TEMPLATE_ROOT,
            REPO / "integration_design.md",
        ]
        checked = []
        combined = ""
        for root in scan_roots:
            paths = [root] if root.is_file() else list(root.rglob("*"))
            for path in paths:
                if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".tpl", ".py"}:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    checked.append(path)
                    combined += "\n" + text

        # The product template should use generic client placeholders, not provider-specific
        # domains, home-directory paths, bot usernames, platform IDs, or credential material.
        self.assertIn("client-domain.example", combined)
        self.assertNotRegex(combined, r"[a-z0-9-]+\.(biz|com)/khoj")
        self.assertNotRegex(combined, r"/home/[a-z0-9_-]+/\.hermes")
        self.assertNotRegex(combined, r"[A-Za-z]+bot\b")
        self.assertNotRegex(combined, r"\b\d{15,22}\b")
        self.assertNotRegex(combined, r"(password|token|api[_-]?key|secret)\s*[:=]\s*[^\s<>{}\[\]]+")
        self.assertGreater(len(checked), 5)


if __name__ == "__main__":
    unittest.main()
