"""Office families, the sealed packs, and the gate arithmetic."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from evo.live.fleet import run_drill
from evo.office.families import FAMILIES
from evo.office.judge import choose_difficulty, judge_office, judge_transfer, touches_to_rate
from evo.office.packs import DEV_PACKS
from evo.office.pilot import demo
from evo.office.seal import load_heldout
from evo.office.stream import _notes, run_office, zipf_plan
from evo.office.verify import health_report


def _arm(name: str, flags: list[bool], tokens: float, drop: float = 0.0) -> dict:
    return {
        "arm": name,
        "exam_items": [{"ok": flag, "family": "table"} for flag in flags],
        "tokens_per_ok": tokens,
        "retain_drop": drop,
        "safety_fails": 0,
        "exam_leak": False,
    }


class OfficeTest(unittest.TestCase):
    def test_verifier_health(self):
        report = health_report()
        self.assertTrue(report["ok"], report["rows"])

    def test_seal_and_zipf_and_scripted_stream(self):
        with self.assertRaises(PermissionError):
            load_heldout(False)
        with tempfile.TemporaryDirectory() as folder:
            seal = Path(folder) / "seal.json"
            packs = load_heldout(True, "unit", seal)
            self.assertEqual([pack["name"] for pack in packs], ["grades", "roster"])
            self.assertTrue(all(pack["heldout"] for pack in packs))
            with self.assertRaises(PermissionError):
                load_heldout(True, "again", seal)
            from evo.office.seal import load_next_heldout

            with self.assertRaises(PermissionError):
                load_next_heldout(False)
            nxt = load_next_heldout(True, "unit-next", Path(folder) / "next.json")
            self.assertEqual([pack["name"] for pack in nxt], ["library", "warehouse"])
            with self.assertRaises(PermissionError):
                load_next_heldout(True, "again", Path(folder) / "next.json")
        self.assertNotIn("heldout_next", (Path(__file__).resolve().parents[2] / "evo" / "office" / "stream.py").read_text(encoding="utf-8"))

    def test_judge_transfer_heritability_ceiling(self):
        # Branch B: fresh=trained=1.0, speed ok, gain 0
        judged = judge_transfer([1, 1, 1, 1], [1, 1, 1, 1], 1, 1)
        self.assertTrue(judged["pass"])
        self.assertEqual(judged["pass_branch"], "heritability")
        self.assertTrue(judged["checks"]["ceiling"])
        self.assertTrue(judged["gate3_claim"])

    def test_judge_transfer_requires_room_for_transfer_branch(self):
        # Perfect fresh blocks Branch A even if somehow gain positive is impossible;
        # gain 0 at ceiling uses B not A
        judged = judge_transfer([1, 1, 1, 1], [1, 1, 1, 1], 1, 1)
        self.assertNotEqual(judged["pass_branch"], "transfer")

    def test_judge_transfer_fail_below_heritability_floor(self):
        # speed ok but fresh=0.5 trained=0.5 — no gain, no ceiling floor path for B (fresh<0.99)
        judged = judge_transfer([0, 1, 0, 1], [0, 1, 0, 1], 2, 2)
        self.assertFalse(judged["pass"])
        self.assertFalse(judged.get("gate3_claim"))

    def test_gen3_seal_burns_once(self):
        from evo.office.seal import load_gen3_heldout
        with tempfile.TemporaryDirectory() as folder:
            rec = Path(folder) / "gen3.json"
            packs = load_gen3_heldout(True, "unit-gen3", rec)
            self.assertEqual([p["name"] for p in packs], ["ferry", "bakery"])
            with self.assertRaises(PermissionError):
                load_gen3_heldout(True, "again", rec)

        plan = zipf_plan(8, list(FAMILIES), 0, drift_at=3, revisit_every=4)
        self.assertEqual(len(plan), 8)
        self.assertTrue(plan[3]["drift"])
        self.assertEqual(plan[4]["kind"], "revisit")
        with tempfile.TemporaryDirectory() as folder:
            report = run_office(
                {
                    "runs_root": folder,
                    "run_name": "office_unit",
                    "seeds": [0],
                    "actor": "reference",
                    "steps": 4,
                    "difficulty": 1,
                    "day_after": 2,
                    "families": ["table"],
                    "arms": ["agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft"],
                    "write_gate": False,
                    "packs": ["orders"],
                }
            )
        dual = report["reports"][0]["arms"][4]
        self.assertGreater(dual["ok_rate"], 0.9)
        self.assertFalse(dual["exam_leak"])
        self.assertGreaterEqual(dual["writes"], 1)
        self.assertIn("orders", DEV_PACKS[0]["name"])

    def test_gate_and_difficulty_and_pilot_and_fleet(self):
        arms = [_arm(name, [True, True, True, False], 100) for name in ("agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft")]
        tied = judge_office([{"seed": 0, "arms": arms}])
        self.assertFalse(tied["pass"])
        weak = [False, False, False, False]
        strong = [True, True, True, True]
        named = {name: _arm(name, weak, 100) for name in ("agent", "oracle", "shift", "continual", "dual_agent", "continual_sft")}
        named["dual"] = _arm("dual", strong, 10)
        ahead = judge_office([{"seed": 0, "arms": [named[name] for name in ("agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft")]}])
        self.assertTrue(ahead["checks"]["beat_agent"])
        gained = judge_transfer([1, 1, 1, 1], [0, 0, 0, 0], 5, 6)
        self.assertTrue(gained["checks"]["transfer"])
        self.assertTrue(gained["checks"]["speed"])
        self.assertEqual(touches_to_rate([False, True, True, True, True]), 5)
        self.assertEqual(choose_difficulty({1: 0.9, 3: 0.5, 5: 0.1})["difficulty"], 3)
        self.assertEqual(choose_difficulty({1: 0.1, 5: 0.0})["why"], "too hard")
        sample = demo()
        self.assertNotIn("out.txt", sample["shadow_changed"])
        self.assertIn("out.txt", sample["assist_changed"])
        self.assertEqual(sample["auto_ok"], [False])
        bare = _notes("agent", {"family": "table", "calls": []})
        self.assertNotIn("demo.csv", bare)
        recalled = _notes("dual_agent", {"family": "table"}, {"table": "open('orders.csv')"})
        self.assertIn("orders.csv", recalled)
        self.assertNotIn("demo.csv", recalled)
        drill = run_drill()
        self.assertTrue(drill["helped"])
        self.assertTrue(drill["leak_blocked"])
        self.assertTrue(drill["export_ok"])
        self.assertTrue(drill["sorted_core"])
        self.assertTrue(drill["sorted_drop"])

    def test_expenses_swap_is_not_a_model_pass(self):
        from evo.office.probe import STOP, conclude, exercise_swap

        swapped = exercise_swap()
        self.assertEqual(swapped["leaks"], [])
        self.assertNotIn("amount", swapped["procedure"])
        self.assertNotIn("paid", swapped["procedure"])
        self.assertNotIn("order_id", swapped["procedure"])
        self.assertIn("sum {AMOUNT}", swapped["procedure"])
        self.assertNotIn("import", swapped["procedure"])
        self.assertLess(len(swapped["procedure"]), 80)
        self.assertNotIn("Sum", swapped["question"])
        self.assertNotIn("where", swapped["question"])
        self.assertNotIn("sum {AMOUNT} where", swapped["question"])
        from evo.computer.episode import run_episode
        from evo.computer.license import License
        from evo.office.families import make_task
        from evo.office.packs import pack_by_name
        from evo.session.procedure import said_line

        self.assertFalse(said_line(swapped["question"]))
        orders = pack_by_name("orders")
        task = make_task(orders, "table", 0, variant=0, difficulty=1)

        def echo(_messages):
            return swapped["question"]

        with tempfile.TemporaryDirectory() as folder:
            echoed = run_episode(task, echo, Path(folder), License(grants={"python", "read", "write"}))
        self.assertFalse(echoed["ok"])
        from evo.office.probe import NOT_RUN, NOT_SAID, SAID, probe_outcome

        missing = probe_outcome(False)
        self.assertEqual(missing["why"], NOT_RUN)
        self.assertEqual(missing["stop"], "")
        silent = probe_outcome(True, said=False, checked=False, steps=1)
        self.assertEqual(silent["stop"], NOT_SAID)
        self.assertFalse(silent["orders_ok"])
        spoke = probe_outcome(True, said=True, checked=True, steps=1)
        self.assertEqual(spoke["why"], SAID)
        self.assertTrue(spoke["model"])
        from evo.office.probe import probe_train_plan

        plan = probe_train_plan()
        self.assertEqual(plan["steps"], 8)
        self.assertIn("gate_proj", plan["sites"])
        self.assertNotIn("q_proj", plan["sites"])
        from evo.office.packs import pack_by_name
        from evo.office.probe import blind_pair, grade_reply
        from evo.session.procedure import LINE

        orders = pack_by_name("orders")
        _task, easy, line, card = blind_pair(orders, 0, 1)
        _hard_task, hard, hard_line, hard_card = blind_pair(orders, 0, 5)
        self.assertEqual(line, LINE)
        self.assertEqual(hard_line, LINE)
        self.assertNotEqual(easy, hard)
        self.assertNotIn("where", hard)
        self.assertNotIn("Sum", hard)
        self.assertNotIn(LINE, hard)
        self.assertFalse(grade_reply(hard, _hard_task, hard_card))
        self.assertTrue(grade_reply(LINE, _hard_task, hard_card))
        from evo.office.probe import wording_split

        trained, held_out = wording_split(orders, 0)
        held_question = held_out[1]
        self.assertEqual(len(trained), 2)
        self.assertTrue(all(item == LINE for _prompt, item in trained))
        self.assertNotIn(held_question, {prompt for prompt, _item in trained})
        self.assertTrue(all("where" not in prompt and LINE not in prompt for prompt, _item in trained))
        from evo.office.probe import file_line, other_job, other_jobs, report_job

        self.assertNotIn(LINE, other_job())
        self.assertNotIn("where", other_job())
        neg_train, neg_held = other_jobs()
        self.assertEqual(len(neg_train), 2)
        self.assertNotIn(neg_held, neg_train)
        self.assertNotIn(LINE, file_line())
        self.assertNotIn(file_line(), LINE)
        self.assertIn("{", file_line())
        self.assertIn("{", LINE)
        self.assertTrue(all(LINE not in text and file_line() not in text for text in neg_train))
        self.assertNotIn(LINE, neg_held)
        self.assertNotIn(LINE, report_job())
        self.assertNotIn(report_job(), neg_train)
        self.assertNotEqual(report_job(), neg_held)
        from evo.office.probe import none_jobs, none_line

        refused, left_out = none_jobs()
        self.assertEqual(left_out, report_job())
        self.assertEqual(len(refused), 2)
        self.assertNotIn(left_out, refused)
        self.assertNotIn(LINE, none_line())
        self.assertNotIn(file_line(), none_line())
        self.assertTrue(all(none_line() not in text and LINE not in text for text in refused))
        from evo.office.probe import replay_budget

        budget = replay_budget()
        self.assertGreater(budget["procedure"], budget["refusal"])
        self.assertEqual(budget["refusal"], 1)
        from evo.office.probe import choose_line

        self.assertEqual(choose_line({"sum": 1.0, "file": 2.0}), "sum")
        self.assertEqual(choose_line({"sum": 2.0, "file": 1.0}), "file")
        self.assertIsNone(choose_line({"sum": 1.0, "file": 1.05}))
        from evo.office.probe import contrast_pairs, exam_sheet, exam_verdict

        contrasted = contrast_pairs([("add the rows", LINE), ("move the file", file_line())])
        self.assertEqual(contrasted[0], ("add the rows", file_line()))
        self.assertEqual(contrasted[1][0], "move the file")
        self.assertNotIn("{OUT}", contrasted[1][1])
        self.assertNotIn(LINE, contrasted[1][1])
        sheet = exam_sheet()
        trained_text = {prompt for prompt, _line in sheet["pairs"]}
        self.assertEqual(len(sheet["sums"]), 4)
        for _name, _task, question, line, _card in sheet["sums"]:
            self.assertEqual(line, LINE)
            self.assertNotIn(question, trained_text)
            self.assertNotIn(LINE, question)
        self.assertNotIn(sheet["file"], trained_text)
        self.assertNotIn(sheet["report"], trained_text)
        self.assertTrue(all(answer != none_line() for _prompt, answer in sheet["pairs"]))
        missed = exam_verdict({"sums": [{"before": False, "after": True, "notes": False}] * 4, "file_said": True, "file_sum": False, "report_sum": True})
        self.assertFalse(missed["passed"])
        self.assertEqual(missed["failed"], ["写报告"])
        passed = exam_verdict({"sums": [{"before": False, "after": True, "notes": False}] * 4, "file_said": True, "file_sum": False, "report_sum": False})
        self.assertTrue(passed["passed"])
        from evo.office.probe import with_notes

        self.assertIn(LINE, with_notes(held_question))
        self.assertNotIn(LINE, held_question)
        expenses = pack_by_name("expenses")
        _expense_train, expense_held = wording_split(expenses, 0)
        self.assertNotEqual(expense_held[1], held_question)
        self.assertIn("claim", expense_held[1])
        self.assertNotIn("order", expense_held[1])
        self.assertNotIn(LINE, expense_held[1])
        self.assertNotIn("cost", expense_held[1])
        self.assertNotIn("approved", expense_held[1])
        for name, noun, banned in (
            ("attendance", "shift", ("hours", "present")),
            ("parcels", "parcel", ("weight", "delivered")),
        ):
            _rows, held_row = wording_split(pack_by_name(name), 0)
            self.assertIn(noun, held_row[1])
            self.assertNotIn(LINE, held_row[1])
            self.assertNotEqual(held_row[1], held_question)
            for word in banned:
                self.assertNotIn(word, held_row[1])
        self.assertIn("cost", swapped["swapped"])
        self.assertIn("approved", swapped["swapped"])
        self.assertNotIn("amount", swapped["swapped"])
        self.assertTrue(swapped["script_ok"])
        self.assertFalse(swapped["model"])
        stopped = conclude(False)
        self.assertEqual(stopped["stop"], STOP)
        self.assertFalse(stopped["orders_ok"])
        self.assertFalse(stopped["expenses_ok"])
        probe = (Path(__file__).resolve().parents[2] / "evo" / "office" / "probe.py").read_text(encoding="utf-8")
        self.assertNotIn("heldout_next", probe)
        self.assertNotIn("heldout", probe)
        road = (Path(__file__).resolve().parents[2] / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("判定：未通过。", road)
        self.assertEqual(road.count("判定：未通过。"), 3)
