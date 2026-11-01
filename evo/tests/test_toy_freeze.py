"""Frozen contract of the fictional-tool world.

Office work is a new exam. These checks lock the old world so a later change
cannot quietly move the baseline the census was scored on.
"""

from __future__ import annotations

import unittest

from evo.live.episodic import Episode, EpisodicBuffer
from evo.live.promote import DEFAULT_LADDER, Ledger
from evo.live.rails import DEFAULT_GRANTS, denied
from evo.selfplay.executor import outputs_match
from evo.world.sleep import curriculum_pairs, ordered_night_pairs
from evo.world.toolbox import build_tools


class ToyFreezeTest(unittest.TestCase):
    def test_ladder_and_grants_stay_put(self):
        self.assertEqual(DEFAULT_LADDER, {"slot_after": 2, "core_holds": 1})
        self.assertEqual(set(DEFAULT_GRANTS), {"python"})
        book = Ledger()
        self.assertEqual(book.destination(["zor"]), "fast")
        book.note_practice(["zor"], True)
        book.note_practice(["zor"], True)
        self.assertEqual(book.destination(["zor"]), "slot")

    def test_exam_stays_out_of_the_buffer_and_files_stay_gated(self):
        buf = EpisodicBuffer()
        refused = buf.add(Episode("q", "print(1)", True, ["zor"], 0, "exam"))
        self.assertFalse(refused)
        self.assertEqual(buf.successes(), [])
        self.assertEqual(denied("print(1)"), [])
        self.assertIn("file", denied("open('x.txt')"))

    def test_hand_curriculum_is_optional_and_default_on(self):
        base = [("drill", "print(1)")]
        reserved = [("Apply a then apply b", "print(2)")]
        closing = [("close", "print(3)")]
        self.assertEqual(curriculum_pairs(base, reserved, closing, hand=False), base)
        handed = curriculum_pairs(base, reserved, closing, hand=True)
        self.assertEqual(handed[0], base[0])
        self.assertIn(reserved[0], handed)
        self.assertEqual(handed.count(closing[0]), 2)
        self.assertEqual(ordered_night_pairs(handed, 2, hand=False), handed)

    def test_tools_still_hide_the_exam_argument(self):
        tools = build_tools(seed=0, count=2, day=1)
        self.assertEqual(len(tools), 2)
        for tool in tools:
            self.assertTrue(tool["name"].isidentifier())
            self.assertNotIn('"""', tool["source"])
            for bucket in ("drill_args", "quiz_args", "held_args"):
                self.assertNotIn(tool["exam_arg"], tool[bucket])
            self.assertNotEqual(tool["exam_arg"], tool["practice_arg"])

    def test_output_match_accepts_equal_literals_only(self):
        self.assertTrue(outputs_match("3", "3"))
        self.assertTrue(outputs_match("3.0", "3"))
        self.assertFalse(outputs_match("4", "3"))


if __name__ == "__main__":
    unittest.main()
