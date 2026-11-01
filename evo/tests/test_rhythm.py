"""Dual rhythm, relabel, absorption, and the cross-pack rung on the ledger."""

from __future__ import annotations

import unittest

from evo.live.absorb import AbsorbBook
from evo.live.promote import Ledger
from evo.live.relabel import relabel
from evo.live.rhythm import apply_rollback, day_ready, interleave, morning_report, sleep_pressure
from evo.live.share import export_skill
from evo.live.sorter import classify, resolve_sort, structural_class
from evo.model import lora_targets


class RhythmTest(unittest.TestCase):
    def test_pressure_report_and_interleave(self):
        self.assertEqual(sleep_pressure({"day_steps": 3, "day_budget": 2}), "budget")
        self.assertEqual(sleep_pressure({"drift": True, "day_steps": 0, "day_budget": 9}), "drift")
        self.assertIsNone(sleep_pressure({"day_steps": 0, "day_budget": 9}))
        self.assertTrue(day_ready({"table": 2}, "table", 2))
        self.assertEqual(interleave(["a"], ["b", "c"]), ["a", "b", "c"])
        text = morning_report([{"name": "table", "dest": "core", "why": "held"}], [])
        self.assertIn("table", text)
        self.assertEqual(apply_rollback([{"name": "table"}, {"name": "file"}], "table"), [{"name": "file"}])

    def test_relabel_absorb_sort_and_cross_rung(self):
        self.assertEqual(relabel(9, "paid", [("paid", 4), ("all", 9)]), "all")
        self.assertIsNone(relabel(4, "paid", [("paid", 4), ("all", 9)]))
        book = AbsorbBook()
        book.note("table", 100, 500)
        book.note("table", 100, 500)
        self.assertFalse(book.decision("table")["absorb"])
        self.assertFalse(book.decision("table")["measured"])
        for _ in range(3):
            book.note("table", 100, 500)
        self.assertFalse(book.decision("table")["absorb"])
        book.measure("table", 0)
        self.assertFalse(book.decision("table")["measured"])
        book.measure("table", 50)
        self.assertFalse(book.decision("table")["absorb"])
        for _ in range(5):
            book.note("table", 100, 500)
        self.assertTrue(book.decision("table")["absorb"])
        self.assertEqual(book.decision("table")["per_use"], 50)
        self.assertEqual(classify(0.2, 0.6, [0.5, 0.4], [0.5, 0.7]), "core")
        self.assertEqual(classify(0.2, 0.6, [0.5], [0.1]), "drop")
        self.assertEqual(classify(0.2, 0.6, [], []), "local")
        self.assertEqual(structural_class("import csv\nopen('a')", "CANARY", ["csv"]), "core")
        self.assertEqual(structural_class("customer CANARY", "CANARY", ["csv"]), "local")
        self.assertEqual(resolve_sort("row['amount']", "", ["csv"], ["amount"], False), "local")
        self.assertEqual(resolve_sort("import csv\nopen('a')", "", ["csv"], ["amount"], False), "local")
        self.assertEqual(resolve_sort("import csv\nopen('a')", "", ["csv"], ["amount"], True), "core")
        from evo.live.share import offer_skill

        stayed = offer_skill("row['amount']", "local", {}, [])
        self.assertFalse(stayed["ok"])
        self.assertEqual(stayed["text"], "")
        leaked = offer_skill("customer CANARY-X", "core", {}, ["CANARY-X"])
        self.assertFalse(leaked["ok"])
        shared = offer_skill("customer CANARY-X", "core", {"CANARY-X": "{id}"}, ["CANARY-X"])
        self.assertTrue(shared["ok"])
        self.assertNotIn("CANARY-X", shared["text"])
        exported = export_skill("see CANARY", {"CANARY": "{id}"}, ["CANARY"])
        self.assertTrue(exported["ok"])
        self.assertNotIn("CANARY", exported["text"])
        ledger = Ledger()
        ledger.note_practice(["alpha"], True)
        ledger.note_practice(["alpha"], True)
        ledger.mark_slot(["alpha"])
        ledger.note_exam(["alpha"], True)
        self.assertEqual(ledger.destination(["alpha"]), "core")
        self.assertEqual(ledger.destination(["alpha"], {"cross_holds": 1}), "local")
        ledger.note_cross(["alpha"], True)
        self.assertEqual(ledger.destination(["alpha"], {"cross_holds": 1}), "core")

    def test_lora_presets(self):
        self.assertEqual(lora_targets({"lora_preset": "attn"}), ["q_proj", "k_proj", "v_proj", "o_proj"])
        full = lora_targets({"lora_preset": "full"})
        self.assertIn("in_proj_qkv", full)
        self.assertIn("gate_proj", full)
        self.assertEqual(lora_targets({"lora_preset": "day_delta"}), ["in_proj_qkv", "in_proj_z", "out_proj"])
        self.assertEqual(lora_targets({"lora_preset": "mlp"}), ["gate_proj", "up_proj", "down_proj"])
        self.assertEqual(lora_targets({"target_modules": ["q_proj"]}), ["q_proj"])
