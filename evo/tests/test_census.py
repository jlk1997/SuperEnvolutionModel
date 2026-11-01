"""Plasticity census scaffolding."""

from __future__ import annotations

import unittest
from pathlib import Path

from evo.plastic.census import plan_cells, run_census
from evo.util import repo_path


class CensusScaffoldTest(unittest.TestCase):
    def test_plan_full_has_three_seeds_and_sites(self):
        cells = plan_cells({"seeds": [0, 1, 2], "skill": "stack"})
        self.assertEqual(len(cells), 9)
        self.assertEqual({c["seed"] for c in cells}, {0, 1, 2})
        self.assertEqual({c["site_id"] for c in cells}, {"mlp", "attn", "attn_mlp"})

    def test_smoke_plans_one_mlp_add_cell(self):
        cells = plan_cells({"seeds": [0, 1, 2], "smoke": True})
        self.assertEqual(len(cells), 1)
        self.assertEqual(cells[0]["site_id"], "mlp")
        self.assertEqual(cells[0]["skill"], "add")

    def test_dry_writes_plan_without_gpu(self):
        dest = repo_path("runs") / "evoplast_census_dry_test.json"
        if dest.is_file():
            dest.unlink()
        report = run_census(
            {
                "run_name": "evoplast_census_dry_test",
                "actor": "model",
                "model_name": str(repo_path("models") / "Qwen2.5-1.5B-Instruct"),
                "seeds": [0, 1],
                "dry": True,
                "write": True,
                "skill": "stack",
            }
        )
        self.assertEqual(report["status"], "dry_plan")
        self.assertIsNone(report["passed"])
        self.assertEqual(report["n_cells"], 6)
        self.assertTrue(dest.is_file())
        dest.unlink()


if __name__ == "__main__":
    unittest.main()
