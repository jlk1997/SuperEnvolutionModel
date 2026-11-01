"""Capability crystallizer unit tests (CPU, no GPU)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from evo.crystal.ablate import dissolution_score, run_ablation
from evo.crystal.crystallize import crystallize_from_adapter, crystallize_from_pairs


class CrystallizerTest(unittest.TestCase):
    def test_dissolution_goes_to_zero_when_bare_matches_scaffold(self):
        self.assertEqual(dissolution_score(0.9, 0.9), 0.0)
        self.assertAlmostEqual(dissolution_score(0.9, 0.6), 0.3, places=6)

    def test_pairs_refuse_below_criterion(self):
        pairs = [("q1", "a1"), ("q2", "a2"), ("q3", "a3"), ("q4", "bad")]
        with self.assertRaises(RuntimeError):
            crystallize_from_pairs(
                "toy_add",
                "add",
                pairs,
                grade=lambda p, c: c == "a1",  # 1/4 < 0.6
                criterion=0.6,
            )

    def test_pairs_crystallize_notes_when_above_gate(self):
        pairs = [(f"q{i}", f"a{i}") for i in range(8)]
        with tempfile.TemporaryDirectory() as tmp:
            atom = crystallize_from_pairs(
                "toy_notes",
                "add",
                pairs,
                grade=lambda p, c: True,
                criterion=0.6,
                dest=Path(tmp) / "toy_notes",
            )
            self.assertEqual(atom.scaffold_rate, 1.0)
            self.assertTrue((Path(atom.adapter_dir) / "capability.json").is_file())
            self.assertEqual(atom.evidence.get("kind"), "notes_only")

    def test_adapter_copy_and_ablation_internalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src_adapter"
            src.mkdir()
            (src / "marker.txt").write_text("lora", encoding="utf-8")
            dest = Path(tmp) / "capabilities" / "add6"
            atom = crystallize_from_adapter(
                "add6",
                "add",
                src,
                dest=dest,
                bare_rate=0.9,
                birth=0.0,
                sites=["mlp"],
                evidence={"source": "test"},
                criterion=0.6,
            )
            self.assertTrue((dest / "marker.txt").is_file())
            self.assertTrue((dest / "capability.json").is_file())
            self.assertGreaterEqual(atom.bare_rate, 0.6)

            notes = {"q0": "answer: 15"}

            def act(prompt: str, mode: str) -> str:
                if mode == "scaffold":
                    return notes.get(prompt, "answer: 0")
                # crystallized bare: correct without notes
                return "answer: 15" if prompt == "q0" else "answer: 0"

            def grade(answer: str, reply: str) -> bool:
                return answer in reply

            report = run_ablation(
                ["q0", "q0", "q0", "q0"],
                ["15", "15", "15", "15"],
                act,
                grade,
                criterion=0.6,
            )
            self.assertTrue(report["bare_clears_gate"])
            self.assertEqual(report["dissolution"], 0.0)
            self.assertTrue(report["internalized"])


    def test_eval_add_heldout_items_are_odds(self):
        from evo.crystal.eval_add import _heldout_add_items

        items = _heldout_add_items()
        self.assertEqual([it["n"] for it in items], [1, 3, 5, 7])
        self.assertTrue(all(it["answer"] for it in items))


    def test_router_prefers_internalized_atom(self):
        import json
        import tempfile
        from pathlib import Path
        from evo.crystal.atom import CapabilityAtom
        from evo.crystal.router import prompt_for, route

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cap = root / "capabilities" / "add6_mlp"
            cap.mkdir(parents=True)
            atom = CapabilityAtom(
                name="add6_mlp",
                skill="add",
                adapter_dir=str(cap),
                base_model="dummy",
                criterion=0.6,
                bare_rate=1.0,
                scaffold_rate=1.0,
                dissolution=0.0,
                sites=["mlp"],
            )
            atom.write(cap)
            (root / "capabilities" / "index.json").write_text(
                json.dumps([{"name": "add6_mlp", "path": str(cap), "skill": "add", "bare_rate": 1.0}]),
                encoding="utf-8",
            )
            # Patch repo_path via monkeypatch of router module paths — call with absolute load
            from evo.crystal import router as R
            old = R.list_atoms
            R.list_atoms = lambda index_path=None: json.loads((root / "capabilities" / "index.json").read_text(encoding="utf-8"))
            old_load = R.load_atom
            R.load_atom = lambda name: CapabilityAtom.load(cap)
            try:
                decision = route("add", notes="KEEP OUT")
                self.assertEqual(decision["mode"], "atom")
                self.assertFalse(decision["use_notes"])
                pf = prompt_for("add", "user q", notes="KEEP OUT")
                self.assertEqual(pf["prompt"], "user q")
                self.assertNotIn("KEEP OUT", pf["prompt"])
            finally:
                R.list_atoms = old
                R.load_atom = old_load

if __name__ == "__main__":
    unittest.main()


