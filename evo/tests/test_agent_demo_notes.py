"""Agent weak demo notes (no atoms, no task secrets)."""

from __future__ import annotations

import unittest

from evo.office.stream import _agent_demo_notes, _notes


class AgentDemoNotesTest(unittest.TestCase):
    def test_family_demos_mention_python_or_shell(self):
        for fam in ("table", "report", "file"):
            blob = _agent_demo_notes(fam)
            self.assertIn("<tool_call>", blob)
            self.assertIn("python", blob)

    def test_notes_include_demo_when_enabled(self):
        raw = _notes(
            "agent",
            {"family": "report", "prompt": "x", "calls": []},
            bank={},
            cfg={"agent_demo_notes": True, "prefer_atoms": False},
        )
        self.assertIn("Format demo", raw)
        self.assertIn("python", raw)

    def test_notes_skip_demo_when_disabled(self):
        raw = _notes(
            "agent",
            {"family": "report", "prompt": "x", "calls": []},
            bank={},
            cfg={"agent_demo_notes": False, "prefer_atoms": False},
        )
        self.assertNotIn("Format demo", raw)


if __name__ == "__main__":
    unittest.main()
