"""Continuous-learning pieces that do not need a GPU."""

from __future__ import annotations

import random
import unittest

import torch

from evo.live.canary import anchors_hold, decide_commit, pick_canaries, safety_violations
from evo.live.compare import judge_stream
from evo.live.consolidator import drift_pairs
from evo.live.episodic import Episode, EpisodicBuffer
from evo.live.onpolicy import advantages, positive_pairs, reverse_kl
from evo.live.identity import Identity, load_identity
from evo.live.promote import Ledger
from evo.live.rails import denied
from evo.live.service import DriftAPI, absorption, grade_action, parse_action, run_actors, run_pair
from evo.live.stream import tick_plan
from evo.live.triggers import decide
from evo.live.verifier import CheckerTrust, literal_claim
from evo.stats import breakeven_uses, paired_bootstrap, power_paired
from evo.world.agent_baseline import oracle_notes
from evo.world.drift import shift_number_tool
from evo.world.sleep import curriculum_pairs, ordered_night_pairs
from evo.world.tasks import expand_exam_pool
from evo.world.toolbox import build_tools


def _fresh_actor():
    from evo.live.service import _scripted_pair

    return _scripted_pair()["fresh"]


class StreamTest(unittest.TestCase):
    def test_exam_never_enters_the_buffer(self):
        buffer = EpisodicBuffer()
        refused = buffer.add(Episode("hidden exam", "print(1)", True, ["a"], 0, "exam"))
        self.assertFalse(refused)
        self.assertEqual(len(buffer), 0)
        buffer.add(Episode("practice", "print(1)", False, ["a"], 1, "practice"))
        self.assertEqual(buffer.exam_leak({"hidden exam"}), [])
        self.assertEqual(buffer.exam_leak({"practice"}), ["practice"])

    def test_sample_prefers_a_failure(self):
        buffer = EpisodicBuffer()
        buffer.add(Episode("old", "print(1)", True, [], 0, "practice", surprise=0.0))
        buffer.add(Episode("miss", "print(2)", False, [], 1, "practice", surprise=5.0))
        rng = random.Random(0)
        draws = [row.prompt for _ in range(30) for row in buffer.sample(1, rng)]
        self.assertGreater(draws.count("miss"), draws.count("old"))

    def test_trigger_cooldown_failure_and_budget(self):
        state = {
            "tick": 3,
            "opt_steps": 0,
            "max_opt_steps": 4,
            "last_commit_tick": 3,
            "consecutive_failures": 5,
            "buffer_size": 3,
            "recent_successes": 2,
        }
        self.assertIsNone(decide(state, {"cooldown": 2}))
        state["last_commit_tick"] = 0
        self.assertEqual(decide(state), "teacher")
        state["consecutive_failures"] = 0
        self.assertEqual(decide(state), "promote")
        state["opt_steps"] = 4
        self.assertIsNone(decide(state))

    def test_canary_skips_practice_and_blocks_unsafe_code(self):
        rng = random.Random(1)
        tasks = [
            {"id": "p", "split": "practice", "tools": ["a"]},
            {"id": "e1", "split": "exam", "tools": ["a"]},
            {"id": "e2", "split": "exam", "tools": ["b"]},
        ]
        picked = pick_canaries(tasks, 2, rng)
        self.assertEqual({task["split"] for task in picked}, {"exam"})
        self.assertTrue(safety_violations("os.system('rm')"))
        self.assertFalse(anchors_hold(["print(1)", "os.remove('x')"]))
        self.assertFalse(decide_commit(1.0, 1.0, 0.34, ["os.system"]))
        self.assertFalse(decide_commit(1.0, 0.0, 0.34, []))
        self.assertTrue(decide_commit(0.5, 0.4, 0.34, []))

    def test_reverse_kl_and_advantages(self):
        logits = torch.zeros(1, 2, 4)
        self.assertAlmostEqual(float(reverse_kl(logits, logits)), 0.0, places=5)
        self.assertEqual(advantages([1.0, 0.0]), [0.5, -0.5])
        pairs = positive_pairs("p", [{"code": "keep"}, {"code": "drop"}], [0.5, -0.5])
        self.assertEqual(pairs, [("p", "keep")])

    def test_intervals_power_and_breakeven(self):
        interval = paired_bootstrap([1, 1, 1, 0], [0, 0, 1, 0], n_boot=500, seed=1)
        self.assertGreater(interval["mean"], 0)
        self.assertFalse(paired_bootstrap([1], [1, 0])["excludes_zero"])
        power = power_paired(0.9, 0.1, n=20, sims=30, alpha_boots=40, seed=2)
        self.assertGreater(power["power"], 0.5)
        self.assertAlmostEqual(breakeven_uses(100, 10, 30), 5.0)
        self.assertIsNone(breakeven_uses(100, 40, 30))

    def test_gate_fails_closed_without_a_win(self):
        report = {
            "seed": 0,
            "arms": [
                {
                    "arm": "continual",
                    "mastery": 4,
                    "forgotten": 2,
                    "tokens_per_ok": 40,
                    "safety_fails": 0,
                    "exam_leak": [],
                    "drift_recovery": 3,
                    "exam_items": [{"ok": False}, {"ok": True}],
                    "opt_steps": 4,
                    "train_tokens": 100,
                },
                {
                    "arm": "shift",
                    "mastery": 2,
                    "forgotten": 0,
                    "drift_recovery": 1,
                    "exam_items": [{"ok": True}, {"ok": True}],
                    "opt_steps": 4,
                },
                {"arm": "agent", "tokens_per_ok": 100, "exam_items": []},
            ],
        }
        gate = judge_stream([report])
        self.assertFalse(gate["pass"])
        self.assertFalse(gate["checks"]["lag"])
        self.assertIn("branch", gate)

    def test_hand_curriculum_switch_and_wider_exam(self):
        pairs = [("single call", "print(1)"), ("then apply the next", "print(a(b(1)))")]
        self.assertEqual(ordered_night_pairs(pairs, 2, False), pairs)
        ordered = ordered_night_pairs(pairs, 2, True)
        self.assertEqual(ordered[0][0], "single call")
        self.assertGreater(ordered.count(pairs[1]), 1)
        self.assertEqual(curriculum_pairs(pairs, [("r", "c")], [("k", "d")], False), pairs)
        tools = build_tools(3, 2, day=0, pair=True)
        wider = expand_exam_pool([], tools, 0, 3, 2.0, random.Random(0))
        self.assertGreaterEqual(len(wider), 1)
        self.assertTrue(all(task["split"] == "exam" for task in wider))
        held = {str(arg) for tool in tools for arg in tool["held_args"]}
        self.assertTrue(all(str(task["arg"]) in held for task in wider))
        notes = oracle_notes({"prompt": "x"}, [{"text": "one"}, {"text": "two"}], [{"text": "old"}], "")
        self.assertIn("one", notes)
        self.assertIn("two", notes)
        self.assertIn("old", notes)

    def test_drift_rewrites_the_drill(self):
        tool = None
        for seed in range(30):
            built = build_tools(seed, 1, day=0)
            if built[0]["kind"] == "number":
                tool = built[0]
                break
        self.assertIsNotNone(tool)
        before = [answer for prompt, answer in drift_pairs(tool) if "return" in prompt]
        self.assertTrue(shift_number_tool(tool))
        after = [answer for prompt, answer in drift_pairs(tool) if "return" in prompt]
        self.assertNotEqual(before, after)

    def test_one_success_does_not_reach_the_core(self):
        book = Ledger()
        self.assertEqual(book.destination(["alpha"]), "fast")
        book.note_practice(["alpha"], True)
        self.assertEqual(book.destination(["alpha"]), "fast")
        book.note_practice(["alpha"], True)
        self.assertEqual(book.destination(["alpha"]), "slot")
        book.mark_slot(["alpha"])
        book.note_exam(["alpha"], True)
        self.assertEqual(book.destination(["alpha"]), "core")
        book.forget("alpha")
        self.assertEqual(book.destination(["alpha"]), "fast")
        trust = CheckerTrust(minimum=0.8, needed=4)
        self.assertEqual(trust.reward(True, False), 1.0)
        for _ in range(4):
            trust.observe(True, True)
        self.assertTrue(trust.trusted())
        self.assertEqual(trust.reward(True, False), 0.0)
        self.assertEqual(literal_claim("print(12)"), "12")
        self.assertEqual(literal_claim("print('ok')"), "ok")
        self.assertIsNone(literal_claim("print(tool(3))"))
        self.assertEqual(denied("print(1)"), [])
        self.assertIn("file", denied("open('workspace/a.txt', 'w').write('x')"))
        self.assertEqual(denied("open('workspace/a.txt', 'w').write('x')", {"python", "write"}), [])
        self.assertIn("unsafe", denied("os.system('echo')", {"python", "shell"}))
        ident = Identity({"cooldown": 1})
        self.assertFalse(ident.remember("exam q", "print(1)", ["a"], "exam"))
        self.assertTrue(ident.remember("do it", "print(1)", ["a"], "practice"))
        restored = load_identity(ident.pack())
        self.assertEqual(restored.replay_pairs(), [("do it", "print(1)")])
        self.assertEqual(literal_claim("assert answer == 4"), "4")

    def test_service_drifts_and_absorption_needs_a_scaffold_win(self):
        api = DriftAPI(seed=1, count=2)
        name = next(iter(api.endpoints))
        task = api.task(name, 4, "exam")
        action = f"HTTP GET /{name}/4\n{task['expect']}"
        self.assertEqual(parse_action(action)["arg"], 4)
        self.assertTrue(grade_action(action, api, task["expect"]))
        self.assertFalse(grade_action(f"HTTP GET /{name}/4", api, task["expect"]))
        self.assertIn(name, api.manual())
        self.assertNotIn("/4", api.manual())
        changed = api.drift()
        self.assertIsNotNone(changed)
        if changed == name:
            self.assertFalse(grade_action(action, api, str(api.call(name, 4))))
        self.assertIsNone(absorption([True], [False]))
        self.assertEqual(absorption([True, False], [True, True]), 0.5)
        session = run_pair(seed=1, steps=6, drift_at=3)
        self.assertTrue(all(session["fresh"]))
        self.assertIn(False, session["stale"])
        self.assertGreater(session["absorption_fresh"], 0.0)
        self.assertLess(session["evolved"][0], True)
        refused = run_actors(
            {"fresh": _fresh_actor(), "evil": ("bare", lambda _task, _manual: "os.system('echo')")},
            seed=1,
            steps=2,
            drift_at=9,
        )
        self.assertFalse(any(refused["rows"]["evil"]))

    def test_tick_plan_is_shared_by_every_arm(self):
        plan = tick_plan(6, tool_every=3, drift_tick=2, day_ticks=3)
        self.assertEqual([row["tick"] for row in plan if row["exam"]], [0, 3])
        self.assertEqual([row["tick"] for row in plan if row["drift"]], [2])
        self.assertEqual([row["tick"] for row in plan if row["new_tool"]], [3])
        self.assertEqual([row["tick"] for row in plan if row["shift_flush"]], [2, 5])


if __name__ == "__main__":
    unittest.main()
