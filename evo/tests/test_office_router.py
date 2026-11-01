"""Office act path prefers internalized atoms over scaffold notes."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from evo.office.stream import _notes, _skill_candidates


class OfficeRouterTest(unittest.TestCase):
    def test_skill_candidates_use_map(self):
        task = {"family": "table"}
        cfg = {"family_skill_map": {"table": "add"}}
        self.assertEqual(_skill_candidates(task, cfg), ["add", "table"])

    def test_strips_notes_when_atom_internalized(self):
        task = {"family": "table", "calls": []}
        cfg = {"prefer_atoms": True, "family_skill_map": {"table": "add"}}
        fake = {
            "mode": "atom",
            "atom": "add6_mlp",
            "use_notes": False,
            "reason": "internalized",
            "skill": "add",
        }
        with mock.patch("evo.crystal.router.route", return_value=fake) as routed:
            out = _notes("agent", task, bank={"table": "PRIOR SUCCESS NOTES"}, cfg=cfg)
        self.assertEqual(out, "")
        self.assertEqual(task["_route"]["mode"], "atom")
        self.assertFalse(task["_route"]["use_notes"])
        routed.assert_called()

    def test_keeps_notes_without_matching_atom(self):
        task = {"family": "shell", "calls": []}
        cfg = {"prefer_atoms": True}
        with mock.patch(
            "evo.crystal.router.route",
            return_value={"mode": "scaffold", "use_notes": True, "notes": "x", "atom": None},
        ):
            out = _notes("agent", task, bank={"shell": "PRIOR"}, cfg=cfg)
        self.assertIn("PRIOR", out)
        self.assertIn("tool_call", out)


if __name__ == "__main__":
    unittest.main()
