"""Plasticity genome, lifetime metrics, and the reference-organism population."""

from __future__ import annotations

import unittest

from evo.bench.families import (
    _EXPR,
    _OPS,
    apply_family,
    build_catalog,
    check_task,
    eval_formula,
    grade_reply,
    parse_int,
    worked_trace,
    families_in,
    render_prompt,
    sample_stream,
    split_catalog,
)
from evo.bench.lifetime_eval import evaluate_sequence, measure_forgetting
from evo.bench.metrics import (
    acceleration_ratio,
    evolution_index,
    families_for_power,
    forgetting,
    heritability,
    learning_curve_area,
    power_for_acceleration,
    samples_to_competence,
)
from evo.bench.office_families import check_office, office_catalog, sample_office
from evo.bench.reasoning import builtin_reasoning, grade, load_reasoning
from evo.evolution.es import DiagCMA, OpenAIES
from evo.evolution.genome import GENE_NAMES, decode, fit_vector, hand_vector, icl_vector, layer_group, make_vector, weak_vector
from evo.evolution.lifetime import assimilate, heldout_ar, shared_tasks, text_area, text_family_ids
from evo.evolution.population import evolve_modes, evolve_plasticity, sweep_signal, transfer_genome
from evo.evolution.runner import run_m0
from evo.plastic.deltanet_carry import StateCarry, carry_from_genome
from evo.plastic.fit import batch_for, lesson, run_fit_loop
from evo.plastic.learner import PlasticLearner
from evo.plastic.lora_life import run_verified_loop
from evo.plastic.runtime import resolve_backend, rollout_plan
from evo.plastic.signal import learning_signal
from evo.plastic.sites import planned_writes


class GenomeTest(unittest.TestCase):
    def test_length_roundtrip_and_groups(self):
        self.assertGreaterEqual(len(GENE_NAMES), 48)
        self.assertLessEqual(len(GENE_NAMES), 64)
        self.assertEqual(len(set(GENE_NAMES)), len(GENE_NAMES))
        genome = decode(hand_vector())
        self.assertEqual(genome.vector, hand_vector())
        self.assertEqual(layer_group(0, 24), "early")
        self.assertEqual(layer_group(23, 24), "last")
        self.assertGreaterEqual(genome.write_after(), 1)
        self.assertLessEqual(genome.write_after(), 8)

    def test_hand_learner_starts_below_the_gate(self):
        genome = decode(hand_vector())
        learner = PlasticLearner(genome)
        self.assertLess(learner.readiness("fresh", "arith"), 0.2)
        self.assertLess(decode(weak_vector()).cluster_alpha("text", "mid"), genome.cluster_alpha("text", "mid"))


class MetricsTest(unittest.TestCase):
    def test_acceleration_forgetting_and_power(self):
        self.assertEqual(samples_to_competence([0.1, 0.4, 0.7], 0.6), 2)
        self.assertEqual(acceleration_ratio(8, 2), 4)
        self.assertGreater(acceleration_ratio(8, 0), 1)
        self.assertGreater(evolution_index([8, 6, 4, 3]), 0)
        self.assertLess(evolution_index([3, 4, 6, 8]), 0)
        self.assertAlmostEqual(forgetting(0.8, 0.3), 0.5)
        self.assertEqual(forgetting(0.2, 0.9), 0.0)
        self.assertAlmostEqual(heritability(2.0, 1.6, floor=1.0), 0.6)
        self.assertGreater(learning_curve_area([0.0, 1.0]), 0.4)
        small = power_for_acceleration(6, sims=40, seed=0)
        large = power_for_acceleration(40, sims=40, seed=0)
        self.assertGreater(large["power"], small["power"])
        needed = families_for_power(target=0.8, seed=0)
        self.assertGreaterEqual(needed["n"], 8)


class DomainTest(unittest.TestCase):
    def test_dsl_heldout_is_large_and_disjoint(self):
        train, held = split_catalog(build_catalog())
        self.assertGreaterEqual(len(held), 30)
        self.assertGreaterEqual(len(train), 8)
        self.assertTrue({family.id for family in train}.isdisjoint({family.id for family in held}))
        self.assertTrue(all(family.template != "branch" for family in train))
        self.assertTrue(any(family.template == "branch" for family in held))
        train_ops = {family.left_op for family in train} | {family.right_op for family in train}
        held_ops = {family.left_op for family in held} | {family.right_op for family in held}
        self.assertTrue(train_ops.isdisjoint(held_ops))
        family = train[0]
        task = family.sample(__import__("random").Random(0), x=4)
        self.assertTrue(check_task(task, str(apply_family(family, 4))))
        self.assertFalse(check_task(task, "not a number"))
        shown = render_prompt(family, 4, reveal=True)
        hidden = render_prompt(family, 4, reveal=False)
        self.assertIn("mod", shown)
        self.assertNotIn("mod", hidden)
        self.assertIsNone(grade_reply("To find the value of (n + 6) mod"))
        self.assertEqual(grade_reply("answer: 36"), 36)
        self.assertEqual(grade_reply("(1 + 6) mod 50 = 7"), 7)
        self.assertIn(str(4), hidden)

    def test_formulas_match_the_primitives(self):
        for cluster, ops in _OPS.items():
            for name, _fn in ops:
                self.assertIn((cluster, name), _EXPR)
                for n in (0, 1, 8, 36):
                    for k in (2, 5, 8):
                        self.assertEqual(eval_formula(cluster, name, n, k), _fn(n, k), (cluster, name, n, k))

    def test_common_random_numbers(self):
        catalog = build_catalog()
        left = sample_stream(catalog, 6, seed=3)
        right = sample_stream(catalog, 6, seed=3)
        other = sample_stream(catalog, 6, seed=4)
        self.assertEqual([task.prompt for task in left], [task.prompt for task in right])
        self.assertNotEqual(left[0].prompt, other[0].prompt)
        self.assertEqual(text_family_ids(5), text_family_ids(5))
        self.assertNotEqual(text_family_ids(5), text_family_ids(6))
        shared = shared_tasks(4, seed=2)
        again = shared_tasks(4, seed=2)
        self.assertEqual([task.answer for task in shared], [task.answer for task in again])

    def test_reasoning_and_office_grade(self):
        tasks = builtin_reasoning(6, seed=1)
        self.assertTrue(all(grade(task, task.answer) for task in tasks))
        loaded = load_reasoning(4, seed=1)
        self.assertGreaterEqual(len(loaded["tasks"]), 4)
        self.assertIn(loaded["source"], {"builtin", "reasoning_gym"})
        rows = office_catalog()
        held = [row for row in rows if row["heldout"]]
        self.assertGreaterEqual(len(held), 30)
        names = {row["pack"]["name"] for row in rows}
        self.assertTrue(names.isdisjoint({"grades", "roster", "library", "warehouse"}))
        task = sample_office(rows[0])
        self.assertTrue(check_office(task, task.answer))
        self.assertFalse(check_office(task, "sum something else"))
        source = __import__("pathlib").Path(__file__).resolve().parents[1].joinpath("bench", "office_families.py").read_text(encoding="utf-8")
        self.assertNotIn("heldout_next", source)
        self.assertNotIn("evo.office.heldout", source)


class CarryAndSitesTest(unittest.TestCase):
    def test_carry_gene_and_decay(self):
        carry = StateCarry(1.0, 0.5)
        carry.remember([1.0, 0.0, 0.0])
        self.assertEqual(carry.recall(), [0.5, 0.0, 0.0])
        carry.remember([0.0, 1.0, 0.0])
        mixed = carry.recall()
        self.assertAlmostEqual(mixed[1], 0.5)
        off = StateCarry(0.0, 0.5)
        off.remember([1.0, 0.0])
        self.assertIsNone(off.recall())
        silent = carry_from_genome(decode(make_vector(-6.0)))
        silent.remember([1.0, 2.0])
        self.assertIsNone(silent.recall())

    def test_plan_skips_dead_sites(self):
        vector = make_vector(-4.0)
        for index, name in enumerate(GENE_NAMES):
            if ".mlp." in name or name == "mem.mid_mix":
                vector[index] = 4.0
        plan = planned_writes(decode(vector))
        sites = [row["site"] for row in plan]
        self.assertIn("mlp", sites)
        self.assertNotIn("attn", sites)
        self.assertNotIn("delta", sites)

    def test_learning_signal_refuses_a_starved_batch(self):
        signal = learning_signal({"grpo_k": 2, "temperature": 0.0})
        self.assertGreaterEqual(signal["grpo_k"], 8)
        self.assertGreater(signal["temperature"], 0.0)
        plan = rollout_plan(4, {"backend": "transformers", "grpo_k": 1, "temperature": 0.0})
        self.assertEqual(plan["backend"], "transformers")
        self.assertGreaterEqual(plan["grpo_k"], 8)
        self.assertEqual(resolve_backend("transformers"), "transformers")


class FitTest(unittest.TestCase):
    def test_best_epoch_keeps_the_earliest_peak(self):
        from evo.plastic.fit import best_epoch

        self.assertEqual(best_epoch([0.0, 0.5, 1.0, 0.25]), 2)
        self.assertEqual(best_epoch([0.5, 0.5, 0.25]), 0)
        self.assertEqual(best_epoch([0.0, 1.0, 1.0]), 1)

    def test_new_skill_is_kept_only_when_the_old_one_holds(self):
        from evo.plastic.fit import choose_epoch

        self.assertEqual(choose_epoch([0.0, 1.0, 1.0], [1.0, 1.0, 0.5]), 1)
        self.assertEqual(choose_epoch([0.0, 0.5, 1.0], [1.0, 1.0, 1.0]), 2)
        self.assertEqual(choose_epoch([0.25, 0.5], [0.5, 0.5]), 0)
        prompt, completion, answer = __import__("evo.plastic.fit", fromlist=["offset_example"]).offset_example(13, 1)
        self.assertEqual(grade_reply(completion), 14)
        self.assertEqual(answer, "14")
        self.assertIn("(1 + 13) mod 50 = 14", completion)
        self.assertIn("g(n)", prompt)
    def test_lesson_is_disjoint_and_the_batch_learns(self):
        plan = lesson(teach=8, exam=4)
        self.assertEqual(len(plan["teach_x"]), 8)
        self.assertTrue(set(plan["teach_x"]).isdisjoint(plan["exam_x"]))
        self.assertTrue(set(plan["teach_x"]).isdisjoint(plan["absorb_x"]))
        pairs = batch_for(plan["family"], plan["teach_x"], reveal=True)
        hidden = batch_for(plan["family"], plan["teach_x"], reveal=False)
        self.assertEqual(len(pairs), 8)
        self.assertTrue(all("mod" in prompt for prompt, _answer in pairs))
        self.assertTrue(all("mod" not in prompt for prompt, _answer in hidden))
        value = plan["teach_x"][0]
        self.assertEqual(parse_int(worked_trace(plan["family"], value)), apply_family(plan["family"], value))
        _prompt, completion, answer = __import__("evo.plastic.fit", fromlist=["_op_example"])._op_example(plan["family"], "right", 3)
        self.assertEqual(grade_reply(completion), int(answer))
        self.assertEqual(completion, "answer: 16")
        from evo.plastic.fit import times_example

        _prompt, times_done, product = times_example(5, 3)
        self.assertEqual(grade_reply(times_done), 15)
        self.assertEqual(product, "15")
        state = {"taught": False}

        def act(task):
            if state["taught"]:
                return task.answer
            return "no"

        def teach(batch):
            self.assertGreaterEqual(len(batch), 8)
            state["taught"] = True
            return 4

        report = run_fit_loop(plan["family"], plan["teach_x"], plan["exam_x"], plan["absorb_x"], act, teach, rounds=2)
        self.assertEqual(report["birth"], 0.0)
        self.assertEqual(report["add_rate"], 1.0)
        self.assertEqual(report["mul_rate"], 1.0)
        self.assertEqual(report["with_rule"], 1.0)
        self.assertEqual(report["names_only"], 1.0)
        self.assertGreater(report["gain"], 0.5)

    def test_fit_genome_writes_mlp_and_delta_only(self):
        plan = planned_writes(decode(fit_vector()))
        sites = [row["site"] for row in plan]
        self.assertEqual(sites[0], "mlp")
        self.assertIn("delta", sites)
        self.assertNotIn("attn", sites)
        self.assertTrue(all(row["lr"] <= 8e-4 for row in plan))


class WithinLifeTest(unittest.TestCase):
    def test_m0_reference_gate(self):
        report = run_m0({"episodes": 20, "write": False})
        self.assertLess(report["start"], 0.2)
        self.assertGreaterEqual(report["end"], 0.6)
        self.assertTrue(report["passed"])

    def test_m1_gap_beats_replicate_noise(self):
        report = sweep_signal()
        self.assertTrue(report["passed"], report)
        self.assertGreater(report["gap"], report["replicate_error"])

    def test_icl_does_not_accelerate_across_families(self):
        _train, held = split_catalog(build_catalog())
        families = families_in(held, "text", True)[:4]
        report = evaluate_sequence(decode(icl_vector()), families, budget=6)
        self.assertLess(report["ar"], 1.35)
        hand = evaluate_sequence(decode(hand_vector()), families, budget=6)
        self.assertGreater(hand["ar"], report["ar"])

    def test_forgetting_tracks_the_penalty_gene(self):
        _train, held = split_catalog(build_catalog())
        anchor = families_in(held, "list", True)[0]
        distractors = families_in(held, "arith", True)[:3]
        calm = decode(_set(hand_vector(), "mem.forget_penalty", -4.0))
        harsh = decode(_set(hand_vector(), "mem.forget_penalty", 4.0))
        low = measure_forgetting(calm, anchor, distractors, budget=6)
        high = measure_forgetting(harsh, anchor, distractors, budget=6)
        self.assertGreater(high["forgetting"], low["forgetting"] + 0.05)

    def test_verified_loop_learns_after_teaching(self):
        train, _held = split_catalog(build_catalog())
        family = train[0]
        tasks = [family.sample(__import__("random").Random(index), x=index) for index in range(10)]
        state = {"skill": 0}

        def act(task):
            if state["skill"] >= 3:
                return task.answer
            return "none"

        def teach(pairs):
            self.assertTrue(pairs)
            state["skill"] += 1
            return 1

        report = run_verified_loop(tasks, act, teach, {"grpo_k": 8, "temperature": 0.7})
        self.assertEqual(report["start"], 0.0)
        self.assertEqual(report["end"], 1.0)
        self.assertGreaterEqual(report["grpo_k"], 8)
        self.assertGreater(report["steps"], 0)


class PopulationTest(unittest.TestCase):
    def test_strategies_climb_a_sphere(self):
        target = [0.4] * 4

        def fitness(vector):
            return -sum((value - goal) ** 2 for value, goal in zip(vector, target))

        es = OpenAIES(4, sigma=0.35, lr=0.45, seed=2, pop=10)
        start = fitness(es.mean)
        for _ in range(40):
            samples = es.ask()
            es.tell([fitness(sample) for sample in samples])
        self.assertGreater(fitness(es.mean), start + 0.3)

        cma = DiagCMA(4, sigma=0.6, seed=2, pop=10)
        start = fitness(cma.mean)
        for _ in range(40):
            samples = cma.ask()
            cma.tell([fitness(sample) for sample in samples])
        self.assertGreater(fitness(cma.mean), start + 0.3)

    def test_es_beats_weak_and_in_context_on_heldout(self):
        report = evolve_plasticity({"generations": 10, "pop": 8, "seed": 0, "sigma": 0.5, "es_lr": 0.4})
        self.assertGreater(report["area"], report["baselines"]["weak"]["area"] + 0.02)
        self.assertGreater(report["heldout"]["ar"], report["baselines"]["icl"]["ar"])
        self.assertGreater(report["heldout"]["ar"], 1.05)
        self.assertGreater(report["map"]["delta"], report["map"]["attn"])
        self.assertTrue(all(row["task_seed"] == report["task_seed"] for row in report["history"]))
        self.assertGreaterEqual(report["area"], report["baselines"]["random_median"])

    def test_baldwin_lamarck_and_darwin_separate(self):
        genome = decode(weak_vector())
        learner = PlasticLearner(genome)
        learner.cluster["logic"] = 0.62
        child = assimilate(genome, learner)
        self.assertGreater(child.innate("logic"), genome.innate("logic") + 0.2)

        for seed in (0, 1, 2):
            modes = evolve_modes(generations=12, pop=16, seed=seed)
            baldwin = modes["baldwin"]["history"]
            lamarck = modes["lamarck"]["history"]
            post_gain = baldwin[-1]["post_area"] - baldwin[0]["post_area"]
            birth_gain = baldwin[-1]["birth_balanced"] - baldwin[0]["birth_balanced"]
            self.assertGreater(post_gain, birth_gain, seed)
            self.assertGreater(post_gain, 0.02, seed)
            self.assertGreater(baldwin[-1]["birth_frequent"], baldwin[-1]["birth_rare"] + 0.1, seed)
            self.assertGreater(
                lamarck[-1]["offspring_birth_frequent"],
                baldwin[-1]["offspring_birth_frequent"],
                seed,
            )

    def test_heritability_across_gains(self):
        found = evolve_plasticity({"generations": 8, "pop": 8, "seed": 1, "sigma": 0.5, "es_lr": 0.4})
        moved = transfer_genome(found["genome"], source_gain=0.6, target_gain=1.0)
        self.assertGreaterEqual(moved["heritability"], 0.5)
        self.assertGreater(moved["ar_transferred"], moved["ar_floor"])


class RealLifeTest(unittest.TestCase):
    """The real-model life harness, without a GPU."""

    def test_traces_reduce_one_operation_per_step(self):
        from evo.plastic.curriculum import catalog, reduce_steps

        self.assertEqual(
            reduce_steps("(37 * 7 + 4) % 50"),
            ["(37 * 7 + 4) mod 50", "(259 + 4) mod 50", "263 mod 50", "13"],
        )
        self.assertEqual(reduce_steps("(37 * 4) % 17"), ["(37 * 4) mod 17", "148 mod 17", "12"])
        self.assertEqual(reduce_steps("(60 - 3 * 37) % 50")[-2:], ["-51 mod 50", "49"])
        for mode in ("shown", "named"):
            for skill in catalog(mode):
                for n in range(100):
                    self.assertEqual(grade_reply(skill.completion(n)), skill.answer(n), (skill.id, n))

    def test_inputs_split_without_overlap(self):
        from evo.plastic.curriculum import split_inputs

        split = split_inputs()
        self.assertEqual((len(split["train"]), len(split["select"]), len(split["report"])), (68, 16, 16))
        self.assertEqual(sorted(split["train"] + split["select"] + split["report"]), list(range(100)))
        self.assertTrue(all(n < 50 for n in split["select"] + split["report"]))

    def test_birth_filter_and_heldout_rules(self):
        from evo.plastic.curriculum import HELDOUT_IDS, catalog, new_skills, split_skills

        train, held = split_skills(catalog())
        self.assertEqual({skill.id for skill in held}, set(HELDOUT_IDS))
        self.assertFalse({skill.id for skill in train} & set(HELDOUT_IDS))
        births = [{"skill": "add6", "innate": True}, {"skill": "lin7", "innate": False}]
        kept = [skill.id for skill in new_skills(train, births)]
        self.assertNotIn("add6", kept)
        self.assertIn("lin7", kept)

    def test_keeper_matches_choose_epoch(self):
        import random

        from evo.plastic.fit import choose_epoch
        from evo.plastic.life import Keeper

        rng = random.Random(3)
        for _ in range(200):
            size = rng.randint(1, 9)
            new = [rng.choice([0.0, 0.25, 0.5, 0.75, 1.0]) for _ in range(size)]
            kept = [rng.choice([0.4, 0.7, 0.9, 1.0]) for _ in range(size)]
            keeper = Keeper(0.8)
            for index, (rate, old) in enumerate(zip(new, kept)):
                keeper.offer(rate, old, index, lambda index=index: index)
            self.assertEqual(keeper.state, choose_epoch(new, kept, floor=0.8))

    def test_acceleration_and_fitness(self):
        from evo.plastic.life import acceleration, fitness

        speed = acceleration([48, 24, None, 0])
        self.assertEqual(speed["ratios"], [1.0, 2.0, None, 48.0])
        self.assertLess(speed["slope"], 0)
        base = {"per_skill": [{"samples": 48}, {"samples": 48}], "final_select": {"a": 1.0, "b": 1.0}, "slots": []}
        quick = {"per_skill": [{"samples": 12}, {"samples": 6}], "final_select": {"a": 1.0, "b": 1.0}, "slots": []}
        missed = {"per_skill": [{"samples": None}, {"samples": 6}], "final_select": {"a": 0.0, "b": 1.0}, "slots": []}
        cfg = {"life_cap": 144}
        self.assertGreater(fitness(quick, cfg), fitness(base, cfg))
        self.assertGreater(fitness(base, cfg), fitness(missed, cfg))

    def test_life_genes_decode(self):
        from evo.plastic.real_genome import LIFE_GENES, decode_life, default_vector, encode_units, grown_vector

        genes = decode_life(default_vector())
        self.assertAlmostEqual(genes.mlp_lr, 2e-4, places=8)
        self.assertEqual((genes.lesson, genes.batch, genes.attn_lr, genes.grow), (12, 8, 0.0, "never"))
        self.assertAlmostEqual(genes.keep, 0.8, places=6)
        self.assertEqual(decode_life(grown_vector()).grow, "need")
        self.assertEqual(decode_life(grown_vector("always")).grow, "always")
        self.assertEqual(decode_life(grown_vector()).sleep_every, 2)
        self.assertEqual(len(encode_units(lesson=1.0)), len(LIFE_GENES))
        self.assertEqual(decode_life(encode_units(lesson=1.0)).lesson, 40)
        self.assertAlmostEqual(genes.lr_at("mlp", 2), 2e-4, places=8)

    def test_padding_and_one_pass_hits(self):
        import torch

        from evo.outer_loop import pad_right
        from evo.plastic.fastscore import _rows, agreement

        ids, labels, attn = pad_right([([1, 2, 3], [-100, 2, 3]), ([4, 5], [-100, 5])], 0, "cpu")
        self.assertEqual(ids.tolist(), [[1, 2, 3], [4, 5, 0]])
        self.assertEqual(labels.tolist(), [[-100, 2, 3], [-100, 5, -100]])
        self.assertEqual(attn.tolist(), [[1, 1, 1], [1, 1, 0]])
        logits = torch.zeros(2, 2, 6)
        logits[0, 0, 2] = 5.0
        logits[0, 1, 3] = 5.0
        logits[1, 0, 1] = 5.0
        rows = _rows(logits, labels[:, 1:])
        self.assertTrue(rows[0]["hit"])
        self.assertGreater(rows[0]["margin"], 0)
        self.assertFalse(rows[1]["hit"])
        self.assertLess(rows[1]["margin"], 0)
        self.assertEqual(agreement([True, False], [True, True]), 0.5)

    def test_stream_plan_and_grading(self):
        import tempfile
        from pathlib import Path

        from evo.computer.actions import format_call
        from evo.plastic.use_stream import KINDS, _thirds, grade, job, plan_stream

        plan = plan_stream(14, 0)
        self.assertEqual(len({row["seed"] for row in plan}), 14)
        self.assertEqual({row["kind"] for row in plan[:7]}, set(KINDS))
        self.assertEqual(_thirds([True, False, True, True, False, False]), [0.5, 1.0, 0.0])
        root = Path(tempfile.mkdtemp())
        task = job(("table", 0), 101)
        code = task["calls"][0].arguments["code"]
        self.assertTrue(grade(task, "```python\n" + code + "\n```", root, "good"))
        self.assertFalse(grade(job(("table", 0), 101), format_call("python", {"code": "print(1)"}), root, "bad"))


def _set(vector, name, value):
    out = list(vector)
    out[GENE_NAMES.index(name)] = value
    return out


if __name__ == "__main__":
    unittest.main()


class StackSecondSkillTest(unittest.TestCase):
    def test_affine_answers_and_batch_align(self):
        from evo.plastic.fit import affine_batch, affine_example, affine_tasks, _second_spec

        prompt, completion, answer = affine_example(3, 17, 4)
        self.assertEqual(answer, str((4 * 3 + 17) % 50))
        self.assertIn("h(n)", prompt)
        self.assertTrue(completion.endswith(answer))
        pairs = affine_batch(3, 17, [0, 2, 4])
        self.assertEqual(len(pairs), 3)
        tasks = affine_tasks(7, 11, [1, 3])
        self.assertEqual(tasks[0].answer, str((1 * 7 + 11) % 50))
        spec = _second_spec({"second_kind": "affine"})
        self.assertEqual(spec["kind"], "affine")
        self.assertGreaterEqual(len(spec["candidates"]), 3)

    def test_offset_spec_still_available(self):
        from evo.plastic.fit import _second_spec

        spec = _second_spec({"second_kind": "offset", "second_offsets": [17, 23]})
        self.assertEqual(spec["kind"], "offset")
        self.assertEqual(spec["candidates"][0]["offset"], 17)



class FitSitesForceTest(unittest.TestCase):
    def test_fit_sites_forces_attn_when_genome_skips_it(self):
        from evo.evolution.genome import decode, fit_vector
        from evo.plastic.fit import _sites

        cfg = {"fit_sites": ["attn", "mlp"]}
        rows = _sites(decode(fit_vector()), cfg)
        names = {row["site"] for row in rows}
        self.assertIn("attn", names)
        self.assertIn("mlp", names)
