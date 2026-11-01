"""External exam scaffold smoke (CPU)."""

from __future__ import annotations

import unittest

from evo.office.external_scaffold import (
    ClBenchLocalAdapter,
    EvoArenaLocalAdapter,
    PathBenchLocalAdapter,
    ServeLearnLocalAdapter,
    adapter_contract,
    discover_cl_bench_local,
    discover_local,
    list_benches,
    run_scaffold_smoke,
)


class ExternalScaffoldTest(unittest.TestCase):
    def test_four_benches_all_local_wires(self):
        benches = list_benches()
        self.assertEqual(len(benches), 4)
        self.assertTrue(adapter_contract("cl_bench")["ok"])
        self.assertFalse(adapter_contract("nope")["ok"])
        for bid in ("cl_bench", "serve_learn", "evo_arena", "path_bench"):
            self.assertIsNotNone(discover_local(bid), msg=bid)
            self.assertTrue(adapter_contract(bid)["wired"], msg=bid)
            self.assertEqual(
                next(b["status"] for b in benches if b["id"] == bid),
                "wired_local_fixture",
                msg=bid,
            )
        self.assertIsNotNone(discover_cl_bench_local())

        for cls in (
            ClBenchLocalAdapter,
            ServeLearnLocalAdapter,
            EvoArenaLocalAdapter,
            PathBenchLocalAdapter,
        ):
            adapter = cls()
            loaded = adapter.load_local()
            self.assertTrue(loaded["ok"], msg=cls.__name__)
            self.assertGreaterEqual(loaded["n"], 4, msg=cls.__name__)
            self.assertFalse(loaded["upstream_claim"])
            preds = {row["id"]: row["gold"] for row in adapter.iter_items()}
            scored = adapter.score(preds)
            self.assertTrue(scored["ok"], msg=cls.__name__)
            self.assertEqual(scored["rate"], 1.0, msg=cls.__name__)
            self.assertFalse(scored["upstream_claim"])

        evidence = run_scaffold_smoke(write_evidence=False)
        self.assertTrue(evidence["pass"])
        self.assertEqual(
            set(evidence["wired_ids"]),
            {"cl_bench", "serve_learn", "evo_arena", "path_bench"},
        )
        self.assertFalse(evidence["upstream_claim"])


if __name__ == "__main__":
    unittest.main()
