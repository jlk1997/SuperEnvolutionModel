"""Per-arm prefer_atoms for B-X6 dual-vs-agent contrast."""

from __future__ import annotations

import unittest

from evo.office.stream import _prefer_atoms_for


class PreferAtomsByArmTest(unittest.TestCase):
    def test_global_default_true(self):
        self.assertTrue(_prefer_atoms_for({}))

    def test_global_false(self):
        self.assertFalse(_prefer_atoms_for({"prefer_atoms": False}))

    def test_by_arm_overrides(self):
        cfg = {"prefer_atoms": True, "prefer_atoms_by_arm": {"dual": True, "agent": False}}
        self.assertTrue(_prefer_atoms_for(cfg, "dual"))
        self.assertFalse(_prefer_atoms_for(cfg, "agent"))
        # unknown arm falls back to global
        self.assertTrue(_prefer_atoms_for(cfg, "oracle"))


if __name__ == "__main__":
    unittest.main()
