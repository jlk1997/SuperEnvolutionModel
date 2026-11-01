"""Census, slots, recipes, inventions, drift, and pixel tasks. No GPU."""

from __future__ import annotations

import random
import unittest

import torch

from evo.model import stack_lora
from evo.world.census import Census, later_faster, mastery_lag, mastery_lags, pick_tasks, rollback_rates
from evo.world.drift import drift_oldest, refresh_expects
from evo.world.invent import concept_pairs, depth_tasks, pose_kept, propose_concepts
from evo.world.lexicon import apply_block, blocked_token_ids
from evo.world.sleep import binding_close
from evo.world.status import format_events
from evo.world.pixels import draw_task, mirror_task, pixel_bundle, vision_status
from evo.world.toolbox import tool_docs
from evo.world.population import fitness, initial_genes, mutate
from evo.world.tasks import day_bundle
from evo.world.toolbox import build_tools
from evo.selfplay.executor import run_code


class EvolveTest(unittest.TestCase):
    def test_census_counts_survival_and_forgetting(self):
        book = Census()
        task = {"id": "t", "tools": ["alpha"], "prompt": "p"}
        book.add(0, "evolved", [{"ok": True, "prompt_tokens": 10, "task": task}])
        book.add(1, "evolved", [{"ok": False, "prompt_tokens": 12, "task": task}])
        report = book.report("evolved", 1, {"alpha": 0})
        self.assertEqual(report["alive"], 0)
        self.assertEqual(report["forgotten"], 1)
        self.assertEqual(report["mastery"], None)
        book.add(2, "evolved", [{"ok": True, "prompt_tokens": 8, "task": task}])
        book.add(3, "evolved", [{"ok": True, "prompt_tokens": 8, "task": task}])
        self.assertEqual(mastery_lag(book.events, "evolved", {"alpha": 0}), 2)
        self.assertEqual(mastery_lags(book.events, "evolved", {"alpha": 0}), [{"tool": "alpha", "birth": 0, "lag": 2}])
        self.assertEqual(rollback_rates([False, True, False]), [0.0, 0.5, 1.0 / 3.0])
        speed = later_faster(
            [
                {"tool": "early", "birth": 0, "lag": 4},
                {"tool": "late", "birth": 3, "lag": 1},
            ]
        )
        self.assertIsNotNone(speed)
        self.assertTrue(speed["later_faster"])
        self.assertTrue(pose_kept(0.5))
        self.assertFalse(pose_kept(0.0))
        self.assertFalse(pose_kept(1.0))
        self.assertEqual(blocked_token_ids([[1, 2], [3]], [[1, 9], [8]]), [8, 9])
        scores = torch.zeros(1, 4)
        blocked = apply_block(scores, [2])
        self.assertEqual(float(blocked[0, 1]), 0.0)
        self.assertLess(float(blocked[0, 2]), -1e4)
        tools = build_tools(1, 2, day=0, pair=True)
        close = binding_close(tools)
        self.assertEqual(len(close), 2)
        blob = "\n".join(prompt for prompt, _code in close)
        for tool in tools:
            self.assertNotIn(str(tool["exam_arg"]), blob)
            self.assertNotIn(str(tool["chain_arg"]), blob)
            self.assertIn(tool["name"], close[0][1] + close[1][1])
        text = format_events(
            [
                {"event": "day0", "agent_rate": 1.0, "base_rate": 0.0, "difficulty": "chain"},
                {
                    "event": "census",
                    "day": 0,
                    "n": 6,
                    "report": {
                        "evolved": {"alive": 2, "forgotten": 0, "mastery": 0.0, "tokens_per_ok": 28.0},
                        "agent": {"alive": 1, "tokens_per_ok": 100.0},
                    },
                },
            ]
        )
        self.assertIn("alive=2", text)
        self.assertIn("difficulty=chain", text)

    def test_census_samples_between_full_mornings(self):
        tasks = [{"id": f"t{index}"} for index in range(20)]
        full = pick_tasks(tasks, 0, 5, 4, random.Random(0))
        sample = pick_tasks(tasks, 1, 5, 4, random.Random(0))
        self.assertEqual(len(full), 20)
        self.assertEqual(len(sample), 4)
        self.assertEqual(pick_tasks(tasks, 9, 5, 4, random.Random(0), last=True), tasks)

    def test_exam_mix_uses_held_out_arguments(self):
        tools = build_tools(3, 2, day=0, pair=True)
        later = build_tools(4, 2, day=1, pair=True)
        bundle = day_bundle(
            1,
            tools + later,
            later,
            "chain",
            {"practice_tasks": 1, "gate_tasks": 1, "exam_tasks": 6, "exec_timeout": 2, "exam_mix": True, "chain_exam": True},
            random.Random(0),
        )
        prompts = [task["prompt"] for task in bundle["exam"]]
        self.assertEqual(len(prompts), 6)
        self.assertEqual(len(set(prompts)), 6)
        self.assertTrue(any(task.get("retention") for task in bundle["exam"]))
        blob = "\n".join(prompts)
        for tool in later:
            self.assertNotIn(tool["name"], blob)

    def test_stack_lora_is_the_sum(self):
        left_a = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        left_b = torch.tensor([[2.0, 0.0], [0.0, 3.0]])
        right_a = torch.tensor([[1.0, 1.0]])
        right_b = torch.tensor([[4.0], [5.0]])
        stacked_a, stacked_b = stack_lora(left_a, left_b, right_a, right_b)
        vector = torch.tensor([1.0, 2.0])
        combined = stacked_b @ stacked_a @ vector
        separate = left_b @ left_a @ vector + right_b @ right_a @ vector
        self.assertTrue(torch.allclose(combined, separate))

    def test_recipe_mutation_stays_in_bounds(self):
        gene = initial_genes({"outer_lr": 5e-4, "night_epochs": 2, "chain_repeat": 2, "kl_coef": 0.5}, 1, random.Random(0))[0]
        child = mutate(gene, random.Random(1))
        self.assertGreaterEqual(child["outer_lr"], 1e-5)
        self.assertLessEqual(child["outer_lr"], 2e-3)
        self.assertIn(child["night_epochs"], range(1, 5))
        self.assertGreater(fitness(1.0, True, 1.0), fitness(0.0, False, 0.0))

    def test_invention_stays_off_the_exam_argument(self):
        tools = build_tools(8, 2, day=0, pair=True)
        code = f"print({tools[1]['name']}({tools[0]['name']}({tools[0]['bind_args'][0]})))"
        trace = {"ok": True, "trace": [{"code": code}], "task": {"split": "practice"}}
        concepts = propose_concepts([trace, trace], tools, set())
        self.assertEqual(len(concepts), 1)
        concept = concepts[0]
        pairs = concept_pairs(concept)
        blob = "\n".join(prompt for prompt, _gold in pairs)
        self.assertNotIn(str(concept["exam_arg"]), blob)
        self.assertNotIn(str(concept["held_args"][0]), blob)
        note = tool_docs([concept])[0]["text"]
        self.assertIn(concept["name"], note)
        self.assertIn(concept["second"], note)
        self.assertIn(str(concept["bind_args"][0]), blob)
        depths = depth_tasks(concept, tools, 2, 2.0)
        self.assertTrue(depths)
        self.assertTrue(all(task["split"] == "exam" for task in depths))
        self.assertNotIn(depths[0]["prompt"], blob)

    def test_drift_changes_the_answer_and_keeps_the_call(self):
        tools = build_tools(5, 2, day=0, pair=True)
        number = next(tool for tool in tools if tool["kind"] == "number") if any(tool["kind"] == "number" for tool in tools) else None
        if number is None:
            tools = []
            for seed in range(30):
                group = build_tools(seed, 1, day=0)
                if group[0]["kind"] == "number":
                    tools = group
                    break
        before = __import__("evo.world.toolbox", fromlist=["call_tool"]).call_tool(tools[0], "11")
        task = {"kind": "call", "gold": f"print({tools[0]['name']}(11))", "expect": str(before)}
        self.assertIsNotNone(drift_oldest(tools))
        after = __import__("evo.world.toolbox", fromlist=["call_tool"]).call_tool(tools[0], "11")
        self.assertNotEqual(before, after)
        self.assertEqual(refresh_expects([task], tools, 2.0), 1)
        self.assertEqual(task["expect"], str(after))
        self.assertIn(tools[0]["name"], task["gold"])

    def test_pixel_exam_is_not_the_practice_grid(self):
        rng = random.Random(0)
        practice = mirror_task("practice", 0, 0, rng)
        exam = mirror_task("exam", 0, 1, random.Random(99))
        self.assertNotEqual(practice["prompt"], exam["prompt"])
        ran = run_code(exam["gold"], 2.0)
        self.assertTrue(ran.ok)
        self.assertEqual(ran.value, exam["expect"])
        bottom = draw_task("exam", 0, 1, "bottom")
        self.assertNotEqual(bottom["expect"], draw_task("practice", 0, 0, "center")["expect"])
        self.assertFalse(vision_status()["loaded"])
        bundle = pixel_bundle(0, random.Random(1))
        practice = "\n".join(task["prompt"] for task in bundle["practice"])
        for task in bundle["exam"]:
            self.assertNotIn(task["prompt"], practice)
            self.assertTrue(task["pixel"])


if __name__ == "__main__":
    unittest.main()
