"""Table prompts at difficulty <= 3 must name columns (Gate3 gen7 fix)."""

from __future__ import annotations

import unittest

from evo.office.families import make_task
from evo.office.packs import _pack


class TablePromptColumnsTest(unittest.TestCase):
    def setUp(self):
        self.pack = _pack("zeta", "rec", "qty", "st", "done", "on", "rid")

    def test_csv_difficulty_2_and_3_name_columns(self):
        for difficulty in (1, 2, 3):
            task = make_task(self.pack, "table", 0, variant=0, difficulty=difficulty)
            prompt = task["prompt"]
            for col in ("rid", "qty", "st"):
                self.assertIn(col, prompt, msg=f"d={difficulty} missing {col}: {prompt}")
            self.assertIn("done", prompt)

    def test_csv_difficulty_4_may_omit_columns(self):
        task = make_task(self.pack, "table", 0, variant=0, difficulty=4)
        # abbreviated: must not require amount/status column names
        self.assertNotIn("qty", task["prompt"])
        self.assertNotIn("st", task["prompt"])

    def test_jsonl_and_xlsx_still_name_columns_at_d2(self):
        for variant in (1, 2):
            task = make_task(self.pack, "table", 0, variant=variant, difficulty=2)
            self.assertIn("qty", task["prompt"])
            self.assertIn("st", task["prompt"])


if __name__ == "__main__":
    unittest.main()
