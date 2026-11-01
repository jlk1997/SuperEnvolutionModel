import unittest

from evo.selfplay.executor import execute_solve, outputs_match, run_code
from evo.selfplay.tasks import (
    check_solver,
    gold_answer,
    is_example_copy,
    learnability,
    materialize,
    mutate_program,
    parse_proposal,
    worked_example,
)


class ExecutorTest(unittest.TestCase):
    def test_prints_result(self):
        result = run_code("print(6 * 7)")
        self.assertTrue(result.ok)
        self.assertIn("42", result.stdout)

    def test_blocks_network_import(self):
        result = run_code("import socket\nprint('nope')")
        self.assertFalse(result.ok)
        self.assertIn("blocked import", (result.error or "") + result.stderr)

    def test_timeout(self):
        result = run_code("while True:\n    pass\n", timeout=1.0)
        self.assertFalse(result.ok)
        self.assertEqual(result.error, "timeout")

    def test_solve_and_match(self):
        result = execute_solve("def solve(x):\n    return x + 1\n", "2")
        self.assertTrue(result.ok)
        self.assertTrue(outputs_match(result.value, "3"))


class TaskTest(unittest.TestCase):
    def test_example_copy_and_gold(self):
        copied = "def solve(x):\n    return x + 1\n"
        invented = "def solve(x):\n    return x * 3\n"
        self.assertTrue(is_example_copy(copied))
        self.assertFalse(is_example_copy(invented))
        self.assertEqual(gold_answer({"type": "deduction", "output": "8"}), "8")
        self.assertEqual(gold_answer({"type": "abduction", "input": "2"}), "2")

    def test_mutate_wraps_and_peels(self):
        program = "def solve(x):\n    return x * 3"
        harder = mutate_program(program, "harder")
        self.assertTrue(harder)
        self.assertTrue(all(not is_example_copy(item) for item in harder))
        wrapped = materialize({"type": "deduction", "program": harder[0], "input": "3"}, 2.0)
        self.assertIsNotNone(wrapped)
        self.assertEqual(wrapped["output"], "11")
        easier = mutate_program(harder[0], "easier")
        self.assertTrue(easier)
        peeled = materialize({"type": "deduction", "program": easier[0], "input": "3"}, 2.0)
        self.assertEqual(peeled["output"], "9")
        deep = mutate_program(program, "harder", depth=True)
        outputs = []
        for item in deep:
            task = materialize({"type": "deduction", "program": item, "input": "3"}, 2.0)
            if task is not None:
                outputs.append(task["output"])
        self.assertIn("2", outputs)
        self.assertIn("82", outputs)
        hinted = worked_example(
            {"type": "abduction", "program": program, "input": "3", "output": "9"},
            2.0,
        )
        self.assertIsNotNone(hinted)
        self.assertNotIn("solve(3)", hinted)

    def test_learnability_peaks_at_half(self):
        self.assertAlmostEqual(learnability(0.5), 1.0)
        self.assertAlmostEqual(learnability(0.0), 0.0)
        self.assertAlmostEqual(learnability(1.0), 0.0)

    def test_deduction_roundtrip(self):
        text = "PROGRAM:\ndef solve(x):\n    return x * 2\nINPUT:\n4\n"
        parsed = parse_proposal(text, "deduction")
        self.assertIsNotNone(parsed)
        task = materialize(parsed, timeout=2.0)
        self.assertEqual(task["output"], "8")
        self.assertTrue(check_solver(task, "8", 2.0))
        self.assertFalse(check_solver(task, "7", 2.0))

    def test_abduction_and_induction(self):
        program = "def solve(x):\n    return x + 1\n"
        abduction = materialize({"type": "abduction", "program": program, "input": "2"}, 2.0)
        self.assertTrue(check_solver(abduction, "2", 2.0))
        self.assertFalse(check_solver(abduction, "9", 2.0))
        induction = materialize(
            {"type": "induction", "program": program, "inputs": ["1", "2", "3"]},
            2.0,
        )
        self.assertTrue(check_solver(induction, program, 2.0))
        wrong = "def solve(x):\n    return x + 5\n"
        self.assertFalse(check_solver(induction, wrong, 2.0))
