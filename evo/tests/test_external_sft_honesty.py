"""CPU honesty checks for external train-only SFT pairs."""

from __future__ import annotations

import unittest

from evo.office.external_scaffold import (
    EvoArenaLocalAdapter,
    PathBenchLocalAdapter,
    ServeLearnLocalAdapter,
)


def _train_eval_ids(adapter):
    adapter.load_local()
    train = {r["id"] for r in adapter.iter_items("train")}
    eval_ = {r["id"] for r in adapter.iter_items("eval")}
    return train, eval_


class ExternalSftHonestyTest(unittest.TestCase):
    def test_train_eval_disjoint_and_nonempty(self):
        for cls in (ServeLearnLocalAdapter, EvoArenaLocalAdapter, PathBenchLocalAdapter):
            adapter = cls()
            train, eval_ = _train_eval_ids(adapter)
            self.assertTrue(train, msg=cls.__name__)
            self.assertTrue(eval_, msg=cls.__name__)
            self.assertFalse(train & eval_, msg=f"{cls.__name__} leak {train & eval_}")

    def test_build_train_pairs_only_uses_train(self):
        # Import from script module path
        import importlib.util
        from pathlib import Path

        path = Path(__file__).resolve().parents[2] / "scripts" / "external_local_sft_score.py"
        spec = importlib.util.spec_from_file_location("external_local_sft_score", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        adapter = ServeLearnLocalAdapter()
        adapter.load_local()
        pairs = mod.build_train_pairs(adapter)
        self.assertEqual(len(pairs), adapter.load_local()["n_train"])
        eval_tasks = {r["task"] for r in adapter.iter_items("eval")}
        for prompt, _gold in pairs:
            # qa_prompt embeds the train task; eval tasks must not appear
            for et in eval_tasks:
                self.assertNotIn(et, prompt)


if __name__ == "__main__":
    unittest.main()
