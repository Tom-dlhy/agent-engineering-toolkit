"""Static consistency checks for seven AET feedback corrections.

These tests catch conflicting guidance, not live Codex/Claude behavior.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class AETContractConsistencyTests(unittest.TestCase):
    def test_task_outcomes_agree_with_primary_skill(self) -> None:
        body = read("skills/core/verification-before-done/SKILL.md")
        leaf = read("skills/core/verification-before-done/references/evidence-and-release-gates.md")
        section = leaf.split("## Completion states", 1)[1].split("## User-facing report", 1)[0]
        states = set(re.findall(r"^- ([A-Z][A-Z ]+):", section, re.M))
        expected = {"COMPLETE", "PARTIALLY VERIFIED", "BLOCKED", "FAILED"}
        self.assertEqual(states, expected)
        self.assertTrue(all(x in body for x in expected))
        self.assertIn("NOT RUN", section)
        self.assertIn("blocked required gate prevents COMPLETE", section)
        self.assertNotIn("VERIFIED IN SCOPE:", section)

    def test_mcp_version_boundary_is_unambiguous(self) -> None:
        protocol = read("skills/ai/mcp-integration/references/protocol-and-transports.md")
        migration = read("skills/ai/mcp-integration/references/migrations-and-interoperability.md")
        self.assertIn("per-request capability exchange", protocol)
        self.assertIn("2026-07-28 core", protocol)
        self.assertIn("do not add `initialize`/`initialized`", protocol)
        self.assertIn("legacy 2025 compatibility", protocol)
        self.assertIn("version-matched JSON-RPC request/response", migration)
        self.assertIn("2025 legacy", migration)
        self.assertNotIn("capability handshake", " ".join(protocol.split()))
        self.assertNotIn("transport handshake", migration)

    def test_scope_ledger_has_declared_decisions_and_owners(self) -> None:
        body = read("skills/personas/scope-guardian/SKILL.md")
        block = body.split("Maintain a **Scope Ledger**:", 1)[1].split("Allowed decisions:", 1)[0]
        rows = [line for line in block.splitlines() if line.startswith("|")]
        self.assertEqual(len(rows), 6)
        self.assertEqual([v.strip() for v in rows[0].strip("|").split("|")],
                         ["Proposal", "User outcome link", "Cost/risk", "Decision", "Owner"])
        decisions = {"IN", "SIMPLIFY", "DEFER", "OUT", "ESCALATE"}
        for row in rows[2:]:
            cells = [value.strip() for value in row.strip("|").split("|")]
            self.assertEqual(len(cells), 5, row)
            self.assertIn(cells[3], decisions, row)
            self.assertTrue(cells[4], row)
        self.assertIn("NO -> DEFER as optional proposal", body)
        self.assertIn("STOP is an action for a blocker", body)
        self.assertIn("stop and report it", body)

    def test_personal_audit_portability_does_not_authorize_publication(self) -> None:
        author = read("skills/core/skill-authoring/SKILL.md")
        intake = read("skills/core/skill-authoring/references/intake-and-decomposition.md")
        external = read("skills/quality/external-skill-audit/SKILL.md")
        self.assertIn("registry/skills.yaml", author)
        self.assertIn("gateway's Markdown indexes", author)
        self.assertIn("maintained externally", intake)
        self.assertIn("unverified charter compliance", intake)
        self.assertIn("a checkout CLI is not required", intake)
        self.assertIn("does not bypass project rules", intake)
        self.assertIn("user-authorized scope", external)
        self.assertIn("read-only audit", external)
        self.assertIn("without creating a repository or PR", " ".join(external.split()))


if __name__ == "__main__":
    unittest.main()
