"""C6 honesty: office atoms route by family; multi-atom conflict; gate 0.6."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evo.crystal.atom import CapabilityAtom
from evo.crystal.router import is_internalized, load_atom, prompt_for, route


def _write_atom(folder: Path, *, name: str, skill: str, bare: float, dissolution: float = 0.0) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    atom = CapabilityAtom(
        name=name,
        skill=skill,
        adapter_dir=str(folder),
        base_model="test",
        criterion=0.6,
        bare_rate=bare,
        scaffold_rate=bare,
        dissolution=dissolution,
        sites=["office", skill],
        evidence={"source": "unit"},
    )
    atom.write(folder)


class OfficeRouterAtomsTest(unittest.TestCase):
    def test_table_report_file_shell_atoms_internalized_and_route(self):
        for skill in ("table", "report", "file", "shell"):
            atom = load_atom(f"office_{skill}_uselog")
            self.assertIsNotNone(atom, skill)
            self.assertIsNotNone(atom.bare_rate)
            self.assertGreaterEqual(atom.bare_rate, 0.6)
            self.assertTrue(is_internalized(atom), skill)
            decision = route(skill, notes="scaffold should be ignored", prefer_atom=True)
            self.assertEqual(decision["mode"], "atom", decision)
            self.assertFalse(decision.get("use_notes"))
            self.assertEqual(decision.get("atom"), f"office_{skill}_uselog")

    def test_unknown_skill_falls_back_to_scaffold(self):
        decision = route("not_a_real_office_skill", notes="keep me", prefer_atom=True)
        self.assertEqual(decision["mode"], "scaffold")
        self.assertTrue(decision.get("use_notes"))

    def test_cross_family_atoms_do_not_steal(self):
        """Multi-atom conflict: routing table must not return shell/report/file."""
        for skill in ("table", "report", "file", "shell"):
            decision = route(skill, notes="x", prefer_atom=True)
            self.assertEqual(decision["mode"], "atom")
            self.assertEqual(decision["atom"], f"office_{skill}_uselog")
            for other in ("table", "report", "file", "shell"):
                if other == skill:
                    continue
                self.assertNotEqual(decision["atom"], f"office_{other}_uselog")

    def test_prefer_atom_false_keeps_scaffold_notes(self):
        decision = route("table", notes="KEEP_NOTES", prefer_atom=False)
        self.assertEqual(decision["mode"], "scaffold")
        self.assertTrue(decision.get("use_notes"))
        self.assertEqual(decision.get("notes"), "KEEP_NOTES")
        # atom may still be named for diagnostics
        self.assertEqual(decision.get("atom"), "office_table_uselog")

    def test_same_skill_picks_higher_bare_internalized(self):
        """Two competing atoms for one skill → highest bare internalized wins."""
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            weak = root / "weak_shell"
            strong = root / "strong_shell"
            _write_atom(weak, name="weak_shell", skill="shell", bare=0.65, dissolution=0.0)
            _write_atom(strong, name="strong_shell", skill="shell", bare=1.0, dissolution=0.0)
            # also a non-shell decoy that must not win
            decoy = root / "decoy_table"
            _write_atom(decoy, name="decoy_table", skill="table", bare=1.0, dissolution=0.0)
            index = root / "index.json"
            index.write_text(
                json.dumps(
                    [
                        {"name": "weak_shell", "path": str(weak), "skill": "shell", "bare_rate": 0.65},
                        {"name": "strong_shell", "path": str(strong), "skill": "shell", "bare_rate": 1.0},
                        {"name": "decoy_table", "path": str(decoy), "skill": "table", "bare_rate": 1.0},
                    ]
                ),
                encoding="utf-8",
            )
            decision = route("shell", notes="ignore", prefer_atom=True, index_path=index)
            self.assertEqual(decision["mode"], "atom")
            self.assertEqual(decision["atom"], "strong_shell")
            self.assertGreaterEqual(decision.get("n_matches", 0), 2)
            # table still picks decoy, not shell
            table = route("table", notes="x", prefer_atom=True, index_path=index)
            self.assertEqual(table["atom"], "decoy_table")

    def test_non_internalized_loses_to_scaffold(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            weak = root / "weak_file"
            _write_atom(weak, name="weak_file", skill="file", bare=0.4, dissolution=0.2)
            index = root / "index.json"
            index.write_text(
                json.dumps([{"name": "weak_file", "path": str(weak), "skill": "file", "bare_rate": 0.4}]),
                encoding="utf-8",
            )
            decision = route("file", notes="need scaffold", prefer_atom=True, index_path=index)
            self.assertEqual(decision["mode"], "scaffold")
            self.assertTrue(decision.get("use_notes"))

    def test_prompt_for_strips_notes_when_atom_wins(self):
        out = prompt_for("shell", "do the copy", notes="SECRET_NOTES")
        self.assertEqual(out["mode"], "atom")
        self.assertEqual(out["prompt"], "do the copy")
        self.assertNotIn("SECRET_NOTES", out["prompt"])


if __name__ == "__main__":
    unittest.main()
