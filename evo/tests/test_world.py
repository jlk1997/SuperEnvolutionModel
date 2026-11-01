import random
import tempfile
import unittest
from pathlib import Path

from evo.generate import blind_edit_prompt
from evo.questions import question_splits
from evo.retrieval import bm25_rank
from evo.scale_decision import decide_scale
from evo.selfplay.executor import run_code
from evo.world.sleep import (
    chains_last,
    compose_drills,
    repeats_call,
    reserved_chains,
    gate_keeps,
    hindsight_pairs,
    retention_keeps,
    select_traces,
    should_sleep,
    verified_drills,
)
from evo.world.tasks import choose_difficulty, day_bundle
from evo.world.toolbox import build_tools, chain_program, chain_result, prelude


class SplitTest(unittest.TestCase):
    def test_disjoint_questions(self):
        passage = {
            "context": "The alloy brinium melts at 451 degrees.",
            "qas": [
                {"id": "a", "question": "When was it refined?", "answers": ["1888"]},
                {"id": "b", "question": "What temperature?", "answers": ["451"]},
                {"id": "c", "question": "What is the name?", "answers": ["brinium"]},
                {"id": "d", "question": "Is it an alloy?", "answers": ["yes"]},
            ],
        }
        practice, gate, exam = question_splits(passage, {"split_questions": True, "questions_per_passage": 4})
        ids = [item["id"] for item in practice + gate + exam]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(practice[0]["id"], "a")
        self.assertEqual(gate[0]["id"], "b")
        self.assertEqual([item["id"] for item in exam], ["c", "d"])
        prompt = blind_edit_prompt(passage)
        self.assertNotIn("When was it refined?", prompt)
        self.assertIn("brinium", prompt)

    def test_old_split_stays_shared(self):
        passage = {"qas": [{"id": str(i)} for i in range(4)]}
        practice, gate, exam = question_splits(passage, {"questions_per_passage": 3})
        self.assertEqual(practice, gate)
        self.assertEqual(gate, exam)


class WorldTest(unittest.TestCase):
    def test_tools_hide_source_and_splits_differ(self):
        tools = build_tools(0, 3, day=0)
        self.assertEqual(len({tool["name"] for tool in tools}), 3)
        for tool in tools:
            self.assertNotIn('"""', tool["source"])
            self.assertNotIn("'''", tool["source"])
            self.assertTrue(tool["source"].startswith("def "))
        bundle = day_bundle(
            0,
            tools,
            tools,
            "single",
            {"practice_tasks": 2, "gate_tasks": 1, "exam_tasks": 2, "exec_timeout": 2},
            random.Random(0),
        )
        practice = {task["prompt"] for task in bundle["practice"]}
        gate = {task["prompt"] for task in bundle["gate"]}
        exam = {task["prompt"] for task in bundle["exam"]}
        self.assertTrue(practice.isdisjoint(exam))
        self.assertTrue(gate.isdisjoint(exam))
        self.assertTrue(practice.isdisjoint(gate))
        names = {tool["name"] for tool in tools}
        for split_rows in bundle.values():
            for task in split_rows:
                for name in names:
                    self.assertNotIn(name, task["prompt"])
                self.assertNotIn("def ", task["prompt"])
        for task in bundle["exam"]:
            self.assertTrue(task["gold"].startswith("print("))
            again = run_code(task["gold"], prelude=prelude(tools), world=True)
            self.assertTrue(again.ok)
            self.assertEqual(again.value, task["expect"])

    def test_sandbox_blocks_source_and_allows_workspace(self):
        tools = build_tools(1, 1, day=0)
        tool = tools[0]
        hidden = run_code(
            f"import inspect\nprint(inspect.getsource({tool['name']}))",
            prelude=prelude(tools),
            world=True,
        )
        self.assertFalse(hidden.ok)
        opened = run_code("print(open('main.py').read())", prelude=prelude(tools), world=True)
        self.assertFalse(opened.ok)
        self.assertIn("blocked", (opened.error or "") + opened.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            wrote = run_code(
                "open('workspace/keep.txt','w',encoding='utf-8').write('hi')\nprint('saved')",
                prelude=prelude(tools),
                world=True,
                workspace=workspace,
            )
            self.assertTrue(wrote.ok)
            self.assertEqual((workspace / "keep.txt").read_text(encoding="utf-8"), "hi")

    def test_quiz_matches_tool(self):
        tool = build_tools(2, 1, day=0)[0]
        pairs = verified_drills(tool)
        self.assertGreaterEqual(len(pairs), 2)
        self.assertEqual(pairs[0][1], tool["name"])
        self.assertIn(tool["nick"], pairs[0][0])

    def test_rules(self):
        self.assertEqual(choose_difficulty(0.1), "single")
        self.assertEqual(choose_difficulty(0.4), "mixed")
        self.assertEqual(choose_difficulty(0.9), "chain")
        self.assertTrue(should_sleep(0.0, 0, 4, False))
        self.assertFalse(should_sleep(0.1, 0, 4, True))
        self.assertTrue(should_sleep(0.1, 2, 2, True))
        self.assertFalse(gate_keeps(0.8, 0.1, 0.9, 0.9, 0.34, 0.15))
        self.assertTrue(gate_keeps(0.5, 0.5, 0.9, 0.8, 0.34, 0.15))
        traces = [
            {"id": "easy", "ok": True},
            {"id": "easy", "ok": True},
            {"id": "mid", "ok": True},
            {"id": "mid", "ok": False},
        ]
        kept = select_traces(traces, True, 0.34)
        self.assertEqual([row["id"] for row in kept], ["mid"])
        ranked = bm25_rank("zorvex reverse", [{"id": "a", "text": "zorvex reverses text"}, {"id": "b", "text": "unrelated cooking"}])
        self.assertEqual(ranked[0]["id"], "a")

    def test_compose_drills_avoid_the_exam_argument(self):
        tools = build_tools(0, 3, day=0)
        prompts = [prompt for prompt, _code in compose_drills(tools)]
        self.assertTrue(prompts)
        for tool in tools:
            for prompt in prompts:
                self.assertNotIn(f"applied to {tool['exam_arg']}", prompt)
                self.assertNotIn(tool["name"], prompt)
        failed = {
            "ok": False,
            "task": {
                "split": "practice",
                "prompt": "Print the result of red-stamp applied to 'gh'.",
                "gold": "print(zorvex('gh'))",
            },
        }
        exam = {
            "ok": False,
            "task": {"split": "exam", "prompt": "exam", "gold": "print(1)"},
        }
        done = {"ok": True, "task": {"split": "practice", "prompt": "done", "gold": "print(2)"}}
        pairs = hindsight_pairs([failed, exam, done])
        self.assertEqual(len(pairs), 1)
        self.assertIn("red-stamp", pairs[0][0])
        self.assertIn("zorvex", pairs[0][1])
        self.assertTrue(retention_keeps(0, 0, 0.34))
        self.assertFalse(retention_keeps(2, 0, 0.34))
        self.assertTrue(retention_keeps(2, 2, 0.34))

    def test_chain_exam_is_scored_and_drilled_on_other_arguments(self):
        tools = build_tools(4, 2, day=0, pair=True)
        self.assertEqual(tools[0]["kind"], tools[1]["kind"])
        drills = [prompt for prompt, _code in compose_drills(tools)]
        chain_drills = [prompt for prompt in drills if "then apply" in prompt]
        self.assertGreaterEqual(len(chain_drills), 2)
        for prompt in chain_drills:
            self.assertNotIn(tools[0]["chain_arg"], prompt)
            self.assertNotIn(tools[1]["chain_arg"], prompt)
            self.assertNotIn(tools[0]["name"], prompt)
        bundle = day_bundle(
            1,
            tools,
            tools,
            "mixed",
            {"practice_tasks": 2, "gate_tasks": 1, "exam_tasks": 2, "exec_timeout": 2, "chain_exam": True},
            random.Random(0),
        )
        exam_chain = bundle["exam"][0]
        self.assertIn("chain", exam_chain["id"])
        self.assertIn(tools[0]["chain_arg"], exam_chain["prompt"])
        self.assertTrue(bundle["exam"][-1]["retention"])
        self.assertNotIn("chain", bundle["exam"][-1]["id"])

    def test_each_kind_gets_its_own_chain_drills(self):
        text = []
        number = []
        for seed in range(40):
            group = build_tools(seed, 2, day=0, pair=True)
            if group[0]["kind"] == "text" and not text:
                text = group
            if group[0]["kind"] == "number" and not number:
                number = group
        self.assertTrue(text and number)
        prompts = [prompt for prompt, _code in compose_drills(text + number)]
        chain_prompts = [prompt for prompt in prompts if "then apply" in prompt]
        self.assertTrue(any(text[0]["nick"] in prompt for prompt in chain_prompts))
        self.assertTrue(any(number[0]["nick"] in prompt for prompt in chain_prompts))
        for tool in text + number:
            for prompt in chain_prompts:
                self.assertNotIn(tool["chain_arg"], prompt)
                self.assertNotIn(tool["gate_arg"], prompt)
                self.assertNotIn(tool["name"], prompt)
        ordered = chains_last(
            [("single", "print(1)"), ("Apply a to 3, then apply b to that result.", "print(b(a(3)))")],
            2,
        )
        self.assertEqual(ordered[0][0], "single")
        self.assertEqual(len(ordered), 3)
        program = chain_program(number[0], number[1], number[0]["bind_args"][0])
        self.assertIn(number[0]["name"], program)
        self.assertIn(number[1]["name"], program)
        self.assertNotIn(number[0]["chain_arg"], program)
        ran = run_code(program, prelude=prelude(number), world=True)
        self.assertTrue(ran.ok)
        self.assertEqual(ran.value, str(chain_result(number[0], number[1], number[0]["bind_args"][0])))

    def test_reserved_tail_rehearses_old_and_new_pairs_off_the_exam(self):
        text = []
        number = []
        for seed in range(40):
            group = build_tools(seed, 2, day=0, pair=True)
            if group[0]["kind"] == "text" and not text:
                text = group
            if group[0]["kind"] == "number" and not number:
                number = group
        held_prompt = (
            f"Apply {text[0]['nick']} to {text[0]['chain_arg']}, then apply {text[1]['nick']} "
            "to that result. Print the final result."
        )
        held = {
            "id": "d0-exam-chain-0",
            "tools": [text[0]["name"], text[1]["name"]],
            "prompt": held_prompt,
            "arg": text[0]["chain_arg"],
        }
        tail = reserved_chains(text + number, [held], number)
        prompts = [prompt for prompt, _code in tail]
        self.assertTrue(any(text[0]["nick"] in prompt and text[1]["nick"] in prompt for prompt in prompts))
        self.assertTrue(any(number[0]["nick"] in prompt and number[1]["nick"] in prompt for prompt in prompts))
        blob = "\n".join(prompts)
        self.assertNotIn(held_prompt, blob)
        self.assertIn(text[0]["bind_args"][0], blob)
        self.assertIn(number[0]["bind_args"][0], blob)
        for tool in text + number:
            self.assertNotIn(tool["chain_arg"], blob)
            self.assertNotIn(tool["gate_arg"], blob)
            self.assertNotIn(tool["practice_arg"], blob)
            self.assertNotIn(tool["exam_arg"], blob)
            self.assertNotIn(tool["name"], blob)
        ordered = chains_last([("single", "print(1)")], 1) + tail
        self.assertEqual(ordered[0][0], "single")
        self.assertIn("then apply", ordered[-1][0])
        single_held = {
            "id": "d1-exam-call-1",
            "tools": [text[0]["name"]],
            "prompt": f"Print the result of {text[0]['nick']} applied to {text[0]['exam_arg']}.",
        }
        with_single = reserved_chains(text + number, [held, single_held], number)
        single_blob = "\n".join(prompt for prompt, _code in with_single)
        self.assertNotIn(text[0]["exam_arg"], single_blob)
        self.assertIn(text[0]["drill_args"][0], single_blob)
        self.assertIn("then apply", with_single[-1][0])
        closing = with_single[-12:]
        self.assertEqual(len(closing), 12)
        self.assertTrue(any(text[0]["name"] in code and text[1]["name"] in code for _prompt, code in closing))
        self.assertTrue(any(number[0]["name"] in code and number[1]["name"] in code for _prompt, code in closing))
        self.assertIn(number[0]["name"], with_single[-1][1])
        self.assertTrue(repeats_call("print(doxtav(vektav(vektav(19))))"))
        self.assertFalse(repeats_call("print(doxtav(vektav(19)))"))

    def test_scale_decision(self):
        smoke = {"days": [{"exam": {"evolved": {"rate": 0.5}, "agent": {"rate": 0.4}}}]}
        live = {
            "days": [
                {"exam": {"evolved": {"rate": 0.3}, "agent": {"rate": 0.2}}},
                {"exam": {"evolved": {"rate": 0.5}, "agent": {"rate": 0.3}}},
            ]
        }
        decision = decide_scale(smoke, live)
        self.assertTrue(decision["recommend_rent_7b"])
        behind = {"days": [{"exam": {"evolved": {"rate": 0.1}, "agent": {"rate": 0.8}}}]}
        no = decide_scale(smoke, behind)
        self.assertFalse(no["recommend_rent_7b"])


if __name__ == "__main__":
    unittest.main()
