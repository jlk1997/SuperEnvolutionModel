"""Write policy, process events, and the office arm's existing fields."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.live.rhythm import morning_card
from evo.office.stream import run_office
from evo.session.policy import write_policy


class WritePolicyTest(unittest.TestCase):
    def test_gates_intersect_conservatively(self):
        self.assertEqual(write_policy("slot", False, "drop")["dest"], "retrieval")
        self.assertFalse(write_policy("slot", False, "core")["write"])
        self.assertEqual(write_policy("fast", True, "drop")["dest"], "fast")
        self.assertFalse(write_policy("fast", True, "core")["write"])
        self.assertEqual(write_policy("slot", True, "drop")["dest"], "drop")
        self.assertEqual(write_policy("core", True, "local")["dest"], "local")
        self.assertTrue(write_policy("core", True, "local")["write"])
        self.assertEqual(write_policy("slot", True, "core")["dest"], "slot")
        self.assertEqual(write_policy("core", True, "core")["dest"], "core")
        self.assertEqual(write_policy("slot", True, "local")["dest"], "local")
        self.assertEqual(write_policy("local", True, "core")["dest"], "local")

    def test_morning_card_keeps_the_string(self):
        card = morning_card([{"name": "table", "dest": "slot", "why": "gates agree on slot"}], [])
        self.assertIn("table", card["text"])
        self.assertEqual(card["commits"][0]["dest"], "slot")

    def test_episode_emits_turns(self):
        seen = []

        def reply(_messages):
            return format_call("finish", {"answer": "x"})

        task = {"id": "t", "prompt": "hi", "family": "table", "check": lambda _workspace: True}
        with tempfile.TemporaryDirectory() as folder:
            run_episode(task, reply, Path(folder), License(), on_event=lambda kind, _payload: seen.append(kind))
        self.assertIn("model_turn", seen)
        self.assertIn("tool", seen)


class OfficeSessionTest(unittest.TestCase):
    def _cfg(self, folder: str, **extra) -> dict:
        cfg = {
            "runs_root": folder,
            "run_name": "office_session",
            "seeds": [0],
            "actor": "reference",
            "steps": 4,
            "difficulty": 1,
            "day_after": 2,
            "families": ["table"],
            "arms": ["dual"],
            "write_gate": False,
            "packs": ["orders"],
            "events_path": str(Path(folder) / "events.jsonl"),
        }
        cfg.update(extra)
        return cfg

    def test_arm_fields_and_events(self):
        with tempfile.TemporaryDirectory() as folder:
            report = run_office(self._cfg(folder))
            arm = report["reports"][0]["arms"][0]
            for key in (
                "exam_items",
                "practice_ok",
                "writes",
                "safety_fails",
                "exam_leak",
                "retain_drop",
                "tokens_per_ok",
                "train_tokens",
                "morning",
                "ok_rate",
            ):
                self.assertIn(key, arm)
            self.assertIsInstance(arm["morning"], str)
            self.assertIn("commits", arm["morning_card"])
            self.assertGreaterEqual(arm["writes"], 1)
            self.assertFalse(arm["exam_leak"])
            self.assertGreater(arm["ok_rate"], 0.9)
            kinds = {json.loads(line)["type"] for line in Path(folder, "events.jsonl").read_text(encoding="utf-8").splitlines()}
        self.assertTrue({"task_start", "model_turn", "tool", "check", "ledger", "absorb", "write", "sleep", "morning"} <= kinds)

    def test_paid_absorption_stops_at_the_slot(self):
        # The reference actor can finish the table. That does not keep a weight write.
        with tempfile.TemporaryDirectory() as folder:
            report = run_office(
                self._cfg(
                    folder,
                    steps=1,
                    day_after=1,
                    absorb_train_tokens=10,
                    ladder={"slot_after": 1, "core_holds": 1},
                )
            )
        arm = report["reports"][0]["arms"][0]
        day = next(row for row in arm["morning_card"]["commits"] if row["name"] == "table")
        self.assertFalse(day["kept"])
        self.assertEqual(day["policy_dest"], "local")
        self.assertEqual(day["why"], "reference is not the model")
        self.assertIn("sum {AMOUNT}", day["procedure"])
        self.assertNotIn("import", day["procedure"])
        self.assertLess(len(day["procedure"]), 80)
        self.assertNotIn("amount", day["procedure"])
        self.assertNotIn("paid", day["procedure"])
        self.assertNotIn("order_id", day["procedure"])
        self.assertNotIn("status", day["procedure"])
        self.assertNotIn("-> core", arm["morning"])

    def test_fast_ledger_blocks_a_weight_write(self):
        with tempfile.TemporaryDirectory() as folder:
            report = run_office(
                self._cfg(
                    folder,
                    steps=1,
                    day_after=1,
                    absorb_train_tokens=10,
                    ladder={"slot_after": 2, "core_holds": 1},
                )
            )
        text = report["reports"][0]["arms"][0]["morning"]
        self.assertIn("one success stays in the fast state", text)

    def test_day_and_night_touch_different_projections(self):
        import json
        from pathlib import Path

        from evo.session.sites import sites_for

        self.assertEqual(sites_for("day", "slot"), ["in_proj_qkv", "in_proj_z", "out_proj"])
        self.assertEqual(sites_for("day", "retrieval"), [])
        night = sites_for("night", "slot")
        self.assertIn("in_proj_qkv", night)
        self.assertIn("gate_proj", night)
        self.assertNotIn("q_proj", night)
        self.assertIn("q_proj", sites_for("day", "core"))
        with tempfile.TemporaryDirectory() as folder:
            run_office(
                self._cfg(
                    folder,
                    steps=1,
                    day_after=1,
                    absorb_train_tokens=10,
                    ladder={"slot_after": 1, "core_holds": 1},
                )
            )
            rows = [json.loads(line) for line in Path(folder, "events.jsonl").read_text(encoding="utf-8").splitlines()]
        writes = [row for row in rows if row["type"] == "write"]
        day = next(row for row in writes if row.get("name") == "table")
        night = next(row for row in writes if row.get("name") == "night")
        self.assertEqual(day["phase"], "day")
        self.assertIn("gate_proj", day["sites"])
        self.assertNotIn("in_proj_qkv", day["sites"])
        self.assertFalse(day["kept"])
        self.assertEqual(night["dest"], "retrieval")
        self.assertNotIn("gate_proj", night.get("sites") or [])

    def test_a_miss_that_hits_the_other_total_is_relabeled(self):
        from evo.computer.actions import format_call
        from evo.computer.license import License
        from evo.office.families import make_task
        from evo.office.packs import DEV_PACKS
        from evo.session.organism import OrganismSession

        task = make_task(DEV_PACKS[0], "table", 0, variant=0, difficulty=1)
        task["split"] = "practice"
        code = "open('paid_total.csv','w',encoding='utf-8').write('total\\n%.2f\\n')" % float(task["expected_all"])

        def reply(_messages):
            return format_call("python", {"code": code})

        session = OrganismSession("dual", {"day_after": 2}, license=License(grants={"python", "read", "write"}))
        with tempfile.TemporaryDirectory() as folder:
            session.step(task, {"index": 0, "family": "table", "kind": "draw", "drift": False, "exam": False}, reply, Path(folder))
        self.assertEqual(session.practice_flags, [False])
        self.assertEqual(session.counts, {})
        self.assertEqual(session.demonstrations[0]["other"], "all")
        self.assertFalse(session.demonstrations[0]["kept"])
        self.assertTrue(any(event["type"] == "relabel" for event in session.bus.events))
        self.assertFalse(any(event["type"] == "write" and event.get("write") for event in session.bus.events))

    def test_a_new_base_keeps_practice_and_drops_exams(self):
        from evo.live.identity import carry_card
        from evo.session.organism import OrganismSession

        card = carry_card(
            {
                "episodes": [
                    {"prompt": "exam", "code": "print(1)", "tools": [], "split": "exam"},
                    {"prompt": "do", "code": "print(2)", "tools": ["table"], "split": "practice"},
                ],
                "verified": {"table": 2},
            }
        )
        self.assertEqual(card["practice"], 1)
        self.assertEqual(card["exams_dropped"], 1)
        self.assertFalse(card["weights"])
        session = OrganismSession("dual", {})
        moved = session.carry(
            {
                "episodes": [{"prompt": "do", "code": "print(2)", "tools": ["table"], "split": "practice"}],
                "verified": {"table": 2},
                "holds": {},
                "in_slot": [],
            }
        )
        self.assertEqual(moved["practice"], 1)
        self.assertEqual(session.ledger.verified.get("table"), 2)
        self.assertEqual(session.identity.replay_pairs(), [("do", "print(2)")])

    def test_shadow_keeps_weights_only_after_a_bare_pass(self):
        from evo.computer.actions import format_call
        from evo.computer.license import License
        from evo.office.families import make_task
        from evo.office.packs import pack_by_name
        from evo.session.organism import OrganismSession

        task = make_task(pack_by_name("orders"), "table", 0, variant=0, difficulty=1)
        task["split"] = "practice"
        code = task["calls"][0].arguments["code"]

        class _Weights:
            def __init__(self):
                self.value = 0
                self.restored = 0

            def snapshot(self, _name):
                return self.value

            def restore(self, _name, state):
                self.value = state
                self.restored += 1

            def promote(self):
                self.value = 1

        def run(passed: bool):
            seen = []
            weights = _Weights()

            def train(_adapter, pairs):
                seen.extend(pairs)
                return {"steps": 1}

            session = OrganismSession(
                "dual",
                {
                    "day_after": 1,
                    "absorb_train_tokens": 10,
                    "ladder": {"slot_after": 1, "core_holds": 1},
                    "ablation": lambda _adapter, _card: passed,
                    "shadow_train": train,
                    "actor": "model",
                },
                evo=weights,
                license=License(grants={"python", "read", "write"}),
            )

            def reply(_messages):
                return format_call("python", {"code": code})

            with tempfile.TemporaryDirectory() as folder:
                session.step(
                    task,
                    {"index": 0, "family": "table", "kind": "draw", "drift": False, "exam": False},
                    reply,
                    Path(folder),
                )
            return session, weights, seen

        missed, restored, trained = run(False)
        blob = "\n".join(part for pair in trained for part in pair)
        self.assertNotIn("amount", blob)
        self.assertNotIn("paid", blob)
        self.assertTrue(trained)
        self.assertTrue(all(code.startswith("sum {AMOUNT}") for _prompt, code in trained))
        self.assertTrue(all("import" not in code for _prompt, code in trained))
        self.assertTrue(all("Sum" not in prompt and "where" not in prompt for prompt, _code in trained))
        self.assertEqual(restored.value, 0)
        self.assertGreaterEqual(restored.restored, 1)
        self.assertFalse(missed.writes[-1]["kept"])
        self.assertEqual(missed.bindings["orders"]["{AMOUNT}"], "amount")
        self.assertNotIn("amount", missed.writes[-1]["procedure"])

        kept, promoted, _again = run(True)
        self.assertTrue(kept.writes[-1]["kept"])
        self.assertEqual(promoted.value, 1)
        self.assertTrue(kept.book.decision("table")["measured"])
        self.assertGreater(kept.book.decision("table")["per_use"], 0)
