import unittest

from evo.consolidate import gate_accept, peak_accept, peak_drop, positive_gain, retention_reward
from evo.eval.retention import matrix_stats, retention_curve
from evo.eval.scoring import exact_match, f1_score, normalize_answer
from evo.model import _retarget, adapter_in_name


class ScoringTest(unittest.TestCase):
    def test_normalize_and_exact(self):
        self.assertEqual(normalize_answer("The Paris!"), "paris")
        self.assertEqual(exact_match("Paris", ["paris", "France"]), 1.0)
        self.assertEqual(exact_match("London", ["Paris"]), 0.0)

    def test_f1_overlap(self):
        self.assertAlmostEqual(f1_score("glass thread", "thread"), 2 / 3)
        self.assertEqual(f1_score("nope", "thread"), 0.0)


class RetentionMathTest(unittest.TestCase):
    def test_reward_penalizes_forgetting(self):
        # gain 0.3, forgotten 0.3, lambda 1 -> 0
        self.assertAlmostEqual(retention_reward(0.2, 0.5, 0.4, 0.1, 1.0), 0.0)
        self.assertAlmostEqual(retention_reward(0.2, 0.5, 0.4, 0.4, 1.0), 0.3)

    def test_peak_catches_a_single_passage_crash(self):
        peaks = {"passage": 0.788, "probe": 0.9}
        self.assertFalse(peak_accept(peaks, {"passage": 0.333, "probe": 0.9}, 0.34))
        self.assertTrue(peak_accept(peaks, {"passage": 0.50, "probe": 0.7}, 0.34))
        self.assertTrue(peak_accept(peaks, {}, 0.34))

    def test_low_peak_does_not_veto(self):
        peaks = {"weak": 0.222, "probe": 0.9}
        wiped = {"weak": 0.0, "probe": 0.9}
        self.assertFalse(peak_accept(peaks, wiped, 0.15))
        self.assertTrue(peak_accept(peaks, wiped, 0.15, min_peak=0.5))
        self.assertEqual(peak_drop(peaks, wiped, min_peak=0.5)[0], "probe")
        self.assertFalse(peak_accept(peaks, {"weak": 0.222, "probe": 0.7}, 0.15, min_peak=0.5))

    def test_positive_gain_rejects_a_zero_update(self):
        self.assertFalse(positive_gain(True, 0.0, 0.0, 0.02))
        self.assertFalse(positive_gain(True, 0.02, -0.006, 0.02))
        self.assertFalse(positive_gain(False, 0.5, 0.5, 0.02))
        self.assertTrue(positive_gain(True, 0.095, 0.095, 0.02))

    def test_gate(self):
        self.assertFalse(gate_accept(0.8, 0.2, 0.1, max_drop=0.34, max_kl=5.0))
        self.assertTrue(gate_accept(0.8, 0.7, 0.2, max_drop=0.34, max_kl=5.0))
        self.assertFalse(gate_accept(0.8, 0.7, 9.0, max_drop=0.34, max_kl=5.0))
        self.assertTrue(gate_accept(0.8, 0.7, None, max_drop=0.34, max_kl=5.0))

    def test_matrix(self):
        matrix = [[0.5, None], [0.2, 0.4]]
        stats = matrix_stats(matrix)
        self.assertAlmostEqual(stats["mean_immediate_f1"], 0.45)
        self.assertAlmostEqual(stats["final_retention_f1"], 0.3)
        self.assertAlmostEqual(retention_curve(matrix)[0], 0.5)
        self.assertAlmostEqual(retention_curve(matrix)[1], 0.3)


class AdapterNameTest(unittest.TestCase):
    def test_retarget(self):
        name = "layers.0.q_proj.lora_B.memory.weight"
        self.assertTrue(adapter_in_name(name, "memory"))
        self.assertFalse(adapter_in_name(name, "policy"))
        self.assertEqual(_retarget(name, "scratch"), "layers.0.q_proj.lora_B.scratch.weight")
