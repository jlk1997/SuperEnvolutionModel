"""retain_drop small-n guard + required_arms present check."""

from __future__ import annotations

import unittest

from evo.office.judge import judge_office
from evo.office.stream import _retain_drop


class RetainDropTest(unittest.TestCase):
    def test_small_n_no_false_forget(self):
        items = [
            {"family": "table", "ok": True},
            {"family": "table", "ok": False},
            {"family": "report", "ok": True},
            {"family": "report", "ok": True},
        ]
        self.assertEqual(_retain_drop(items), 0.0)

    def test_large_n_detects_drop(self):
        items = [{"family": "table", "ok": True}] * 4 + [{"family": "table", "ok": False}] * 4
        self.assertGreater(_retain_drop(items), 0.05)


class RequiredArmsJudgeTest(unittest.TestCase):
    def _report(self, arms, seed=0):
        return {
            "seed": seed,
            "arms": [
                {
                    "arm": name,
                    "exam_items": [{"ok": True, "family": "table"} for _ in range(4)],
                    "retain_drop": 0.0,
                    "safety_fails": 0,
                    "exam_leak": False,
                }
                for name in arms
            ],
        }

    def test_narrow_arms_present_true(self):
        rep = self._report(["dual", "agent"])
        judged = judge_office([rep], required_arms=["dual", "agent"])
        self.assertTrue(judged["seeds"][0]["present"])
        self.assertTrue(judged["seeds"][0]["forget_ok"])

    def test_full_slate_missing_arm_present_false(self):
        rep = self._report(["dual", "agent"])
        judged = judge_office([rep])  # default REQUIRED_ARMS
        self.assertFalse(judged["seeds"][0]["present"])


if __name__ == "__main__":
    unittest.main()
