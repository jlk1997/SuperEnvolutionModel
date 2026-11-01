"""Fit one tool family into a LoRA, then ask for new inputs.

The reference organism never reads the prompt. A language model does, so the
rule has to be in the string it is trained on, and the exam has to use new
inputs. One example at a time collapses the answer onto that one integer.
A batch, replayed, is the update.
"""

from __future__ import annotations

from evo.bench.families import (
    Family,
    Task,
    build_catalog,
    families_in,
    eval_formula,
    formula,
    grade_reply,
    split_catalog,
    substituted,
    task_at,
    worked_trace,
)
from evo.evolution.genome import Genome, decode, fit_vector


def lesson(seed: int = 0, teach: int = 8, exam: int = 4) -> dict:
    """One arithmetic family. Teach inputs and exam inputs do not overlap."""
    train, _held = split_catalog(build_catalog(seed=0))
    family = families_in(train, "arith", False)[0]
    teach_x = list(range(0, teach * 2, 2))[:teach]
    exam_x = list(range(1, exam * 2 + 1, 2))[:exam]
    absorb_x = list(range(30, 30 + exam))
    used = set(teach_x)
    if used & set(exam_x) or used & set(absorb_x) or set(exam_x) & set(absorb_x):
        raise RuntimeError("exam inputs leaked into teaching")
    return {"family": family, "teach_x": teach_x, "exam_x": exam_x, "absorb_x": absorb_x, "seed": seed}


def _ends(family: Family, which: str) -> tuple[str, str, int]:
    if which == "left":
        return family.left_name, family.left_op, family.left_k
    return family.right_name, family.right_op, family.right_k


def _op_example(family: Family, which: str, value: int) -> tuple[str, str, str]:
    """Prompt, trained completion, and the integer the exam grades.

    Addition is learned from the substituted rule. Multiplication also writes the
    product, because the 1.5B copied `(n * 5 + 1)` and still emitted the wrong total.
    """
    name, op, k = _ends(family, which)
    number = int(value)
    answer = str(eval_formula(family.cluster, op, number, k))
    if op == "spin":
        # The times table is a separate stage. Putting the product and the answer
        # in one completion made the model emit two different integers.
        prompt = (
            f"{name}(n) = (n * {int(k)} + 1) mod 50.\n"
            f"n = {number}\n"
            "Write only `answer: <integer>`."
        )
        return prompt, f"answer: {answer}", answer
    prompt = (
        f"{name}(n) = {formula(family.cluster, op, k)}.\n"
        f"n = {number}\n"
        "Fill in the rule. End with `= <integer>`."
    )
    return prompt, substituted(family.cluster, op, number, k), answer


def times_example(k: int, value: int) -> tuple[str, str, str]:
    """The product alone. The +1 and the modulus come after this is reliable."""
    number = int(value)
    product = number * int(k)
    prompt = f"n = {number}\nWrite `{number} * {int(k)} = <integer>`."
    return prompt, f"{number} * {int(k)} = {product}", str(product)


def times_batch(k: int, values: list[int]) -> list[tuple[str, str]]:
    return [(prompt, completion) for prompt, completion, _answer in (times_example(k, value) for value in values)]


def times_tasks(family: Family, k: int, values: list[int]) -> list[Task]:
    tasks = []
    for value in values:
        prompt, _completion, answer = times_example(k, value)
        tasks.append(Task(family.id, family.cluster, prompt, answer, family.heldout, family.domain))
    return tasks


def op_batch(family: Family, which: str, values: list[int]) -> list[tuple[str, str]]:
    """One operation. The completion is the rule with this n substituted."""
    return [(prompt, completion) for prompt, completion, _answer in (_op_example(family, which, value) for value in values)]


def op_tasks(family: Family, which: str, values: list[int]) -> list[Task]:
    tasks = []
    for value in values:
        prompt, _completion, answer = _op_example(family, which, value)
        tasks.append(Task(family.id, family.cluster, prompt, answer, family.heldout, family.domain))
    return tasks


def step_batch(family: Family, values: list[int]) -> list[tuple[str, str]]:
    """One operation at a time. The completion is the rule with n filled in."""
    pairs = []
    for value in values:
        for name, op, k in (
            (family.left_name, family.left_op, family.left_k),
            (family.right_name, family.right_op, family.right_k),
        ):
            prompt = (
                f"{name}(n) = {formula(family.cluster, op, k)}.\n"
                f"n = {int(value)}\n"
                "Fill in the rule. End with `= <integer>`."
            )
            pairs.append((prompt, substituted(family.cluster, op, value, k)))
    return pairs


def step_tasks(family: Family, values: list[int]) -> list[Task]:
    tasks = []
    for value in values:
        for name, op, k in (
            (family.left_name, family.left_op, family.left_k),
            (family.right_name, family.right_op, family.right_k),
        ):
            prompt = (
                f"{name}(n) = {formula(family.cluster, op, k)}.\n"
                f"n = {int(value)}\n"
                "Fill in the rule. End with `= <integer>`."
            )
            answer = str(eval_formula(family.cluster, op, value, k))
            tasks.append(Task(family.id, family.cluster, prompt, answer, family.heldout, family.domain))
    return tasks


def batch_for(family: Family, values: list[int], reveal: bool = True) -> list[tuple[str, str]]:
    """The completion is the worked trace, not a bare integer.

    Name-only prompts are a second stage. Mixed into the first batch they teach
    the model to emit one constant, because those prompts barely differ.
    """
    pairs = []
    for value in values:
        task = task_at(family, value, reveal=reveal)
        pairs.append((task.prompt, worked_trace(family, value)))
    return pairs


def exam_tasks(family: Family, values: list[int], reveal: bool) -> list[Task]:
    return [task_at(family, value, reveal=reveal) for value in values]


def choose_epoch(skill_rates: list[float], kept_rates: list[float], floor: float = 0.6) -> int:
    """Earliest epoch that learns the new skill without dropping the old one below `floor`.

    Index 0 is the snapshot from before this skill. If every later epoch drops the
    old skill, that snapshot stays.
    """
    if len(skill_rates) != len(kept_rates) or not skill_rates:
        raise ValueError("epoch scores must be paired and non-empty")
    eligible = [index for index, old in enumerate(kept_rates) if old >= floor]
    if not eligible:
        return 0
    chosen = eligible[0]
    for index in eligible[1:]:
        if skill_rates[index] > skill_rates[chosen]:
            chosen = index
    return chosen


def best_epoch(rates: list[float]) -> int:
    """Earliest epoch with the highest score. A later tie does not replace it."""
    if not rates:
        raise ValueError("no epoch scores")
    chosen = 0
    for index, rate in enumerate(rates):
        if rate > rates[chosen]:
            chosen = index
    return chosen


def run_fit_loop(family: Family, teach_x: list[int], exam_x: list[int], absorb_x: list[int], act, teach, rounds: int = 2) -> dict:
    """Learn the left operation, then the right one, and only then their composition.

    Composition is a new batch. Run too early, it overwrites the operation the
    model just acquired. Each later batch replays the earlier pairs.
    """
    probe = list(exam_x)
    # Evens only, one pass. A denser set and a second pass both made the held-out addition worse.
    drill = list(range(0, 21, 2))
    mul_drill = [n for n in range(0, 31) if n not in set(probe)]
    birth_add = _score(act, op_tasks(family, "left", probe))
    birth_mul = _score(act, op_tasks(family, "right", probe))
    history = [{"round": 0, "add": birth_add["rate"], "mul": birth_mul["rate"], "steps": 0}]
    steps = 0
    add_pairs = op_batch(family, "left", drill)
    steps += int(teach(add_pairs) or 0)
    add_after = _score(act, op_tasks(family, "left", probe))
    history.append({"round": "add", "add": add_after["rate"], "steps": steps})
    times_after = {"rate": 0.0, "hits": []}
    times_pairs: list[tuple[str, str]] = []
    if add_after["rate"] >= 0.6 and family.right_op == "spin":
        times_pairs = times_batch(family.right_k, mul_drill)
        for _attempt in range(2):
            steps += int(teach(add_pairs + times_pairs) or 0)
            times_after = _score(act, times_tasks(family, family.right_k, probe))
            history.append({"round": "times", "times": times_after["rate"], "steps": steps})
            if times_after["rate"] >= 0.6:
                break
    mul_after = {"rate": 0.0, "hits": []}
    add_kept = add_after
    if times_after["rate"] >= 0.6:
        mul_pairs = op_batch(family, "right", mul_drill)
        # Addition and the times table are both replayed, or the new batch erases them.
        steps += int(teach(add_pairs + times_pairs + mul_pairs) or 0)
        mul_after = _score(act, op_tasks(family, "right", probe))
        add_kept = _score(act, op_tasks(family, "left", probe))
        history.append({"round": "mul", "add": add_kept["rate"], "mul": mul_after["rate"], "steps": steps})
    held = {"rate": 0.0, "hits": []}
    bare = {"rate": 0.0, "hits": []}
    if add_kept["rate"] >= 0.6 and mul_after["rate"] >= 0.6:
        composed = batch_for(family, teach_x, reveal=True)
        steps += int(teach(composed + add_pairs + mul_pairs) or 0)
        held = _score(act, exam_tasks(family, exam_x, True))
        bare = _score(act, exam_tasks(family, absorb_x, False))
        history.append({"round": "compose", "with_rule": held["rate"], "names_only": bare["rate"], "steps": steps})
    return {
        "family": family.id,
        "birth": birth_add["rate"],
        "birth_mul": birth_mul["rate"],
        "add_rate": add_after["rate"],
        "times_rate": times_after["rate"],
        "mul_rate": mul_after["rate"],
        "add_kept": add_kept["rate"],
        "steps_rate": add_after["rate"],
        "with_rule": held["rate"],
        "names_only": bare["rate"],
        "gain": add_after["rate"] - birth_add["rate"],
        "steps": steps,
        "history": history,
        "teach": len(drill),
    }


def run_model_fit(cfg: dict) -> dict:
    """Load the base, fit the lesson, unload. Prints each exam so a long run is visible."""
    import torch

    if not torch.cuda.is_available():
        return {"status": "no_cuda", "passed": False, "reason": "CUDA is not available."}
    from pathlib import Path

    from evo.model import build_model, release

    path = Path(str(cfg.get("model_name") or ""))
    if not path.is_dir():
        return {"status": "no_weights", "passed": False, "reason": f"weights not on disk: {path}"}
    plan = lesson(
        seed=int(cfg.get("seed", 0)),
        teach=int(cfg.get("teach", 8)),
        exam=int(cfg.get("exam", 4)),
    )
    genome = decode(fit_vector())
    evo = None
    try:
        evo = build_model(cfg)
        print(f"[fit] loaded {path.name} vram_mb={evo.vram_mb():.0f}", flush=True)

        def act(task: Task) -> str:
            from evo.generate import generate

            reply = generate(
                evo,
                task.prompt,
                int(cfg.get("max_new_code", 8)),
                0.0,
                "policy",
                max_len=int(cfg.get("max_seq_len", 512)),
            )
            got = grade_reply(reply)
            ok = got is not None and got == int(task.answer)
            print(f"[fit] ask {task.answer} -> {reply!r} ok={ok}", flush=True)
            return reply

        def teach(pairs: list[tuple[str, str]]) -> int:
            import random

            from evo.plastic.sites import apply_planned_updates

            rng = random.Random(int(cfg.get("seed", 0)))
            steps = 0
            sites = []
            for _epoch in range(int(cfg.get("fit_epochs", 3))):
                order = list(pairs)
                rng.shuffle(order)
                stats = apply_planned_updates(evo, order, genome, cfg, epochs=1)
                steps += int(stats["steps"])
                sites = stats["sites"]
            print(f"[fit] update steps={steps} sites={sites} pairs={len(pairs)}", flush=True)
            return steps

        if cfg.get("skill") == "add":
            report = _stable_add(evo, act, genome, cfg, plan["family"])
        elif cfg.get("skill") == "stack":
            report = _stack(evo, act, genome, cfg, plan["family"])
        else:
            report = run_fit_loop(
                plan["family"],
                plan["teach_x"],
                plan["exam_x"],
                plan["absorb_x"],
                act,
                teach,
                rounds=int(cfg.get("rounds", 2)),
            )
        report["model"] = str(path)
        report["vram_mb"] = evo.vram_mb()
        report["sites"] = [row["site"] for row in _sites(genome, cfg)]
        if "passed" not in report:
            report["passed"] = report["birth"] < 0.5 and report["add_kept"] >= 0.6 and report["gain"] > 0
        report["status"] = "passed" if report["passed"] else "failed"
        if report["passed"]:
            dest = _adapter_dir(cfg)
            dest.mkdir(parents=True, exist_ok=True)
            evo.model.save_pretrained(dest)
            report["adapter"] = str(dest)
            print(f"[fit] saved {dest}", flush=True)
        if not report["passed"]:
            if report.get("recommendation"):
                pass
            elif float(report.get("second_birth") or report.get("times_birth") or 0) >= 0.5:
                report["recommendation"] = (
                    "Second skill was already above 0.5 at birth, so the stack gate "
                    "(second_birth < 0.5) cannot fire. Use second_kind=affine, widen "
                    "second_affines, or skill=add; do not lower the 0.6 competence gate."
                )
            elif report.get("skill") == "stack" and float(report.get("second_report") or 0) < 0.6:
                report["recommendation"] = (
                    "Second skill report stayed below 0.6 while addition held. "
                    "Try second_phase=solo / more solo_epochs, or a slightly easier affine; "
                    "do not lower the 0.6 gate."
                )
            else:
                report["recommendation"] = (
                    "Held-out addition did not clear 0.6. Stay on one operation, replay it, "
                    "and do not train the composition until that exam holds."
                )
        return report
    finally:
        if evo is not None:
            release(evo)


def _stable_add(evo, act, genome: Genome, cfg: dict, family: Family) -> dict:
    """One epoch at a time. The selection odds pick the epoch. A different set of odds is the report.

    The report odds are not used to choose. A second pass that scores worse is thrown away.
    """
    import random

    from evo.model import adapter_state, load_adapter_state
    from evo.plastic.sites import apply_planned_updates

    report_x = [1, 3, 5, 7]
    select_x = [9, 11, 13, 15]
    train_x = list(range(0, 21, 2))
    if set(train_x) & set(report_x) or set(train_x) & set(select_x) or set(report_x) & set(select_x):
        raise RuntimeError("addition exam leaked into training")
    pairs = op_batch(family, "left", train_x)
    epochs = int(cfg.get("fit_epochs", 4))
    snaps = [adapter_state(evo.model, "policy")]
    select_rates = [_score(act, op_tasks(family, "left", select_x))["rate"]]
    birth = _score(act, op_tasks(family, "left", report_x))["rate"]
    rng = random.Random(int(cfg.get("seed", 0)))
    for epoch in range(epochs):
        order = list(pairs)
        rng.shuffle(order)
        stats = apply_planned_updates(evo, order, genome, cfg, epochs=1)
        rate = _score(act, op_tasks(family, "left", select_x))["rate"]
        snaps.append(adapter_state(evo.model, "policy"))
        select_rates.append(rate)
        print(f"[fit] epoch {epoch + 1} select={rate} steps={stats['steps']}", flush=True)
    chosen = best_epoch(select_rates)
    load_adapter_state(evo.model, "policy", snaps[chosen])
    report_rate = _score(act, op_tasks(family, "left", report_x))["rate"]
    print(f"[fit] kept epoch {chosen} report={report_rate} birth={birth}", flush=True)
    return {
        "family": family.id,
        "skill": "add",
        "birth": birth,
        "select_rates": select_rates,
        "kept_epoch": chosen,
        "add_rate": report_rate,
        "add_kept": report_rate,
        "gain": report_rate - birth,
        "steps": chosen * len(pairs),
    }


def offset_example(offset: int, value: int, modulus: int = 50) -> tuple[str, str, str]:
    """A second addition, different constant. Birth on this prompt is zero for the 1.5B."""
    number = int(value)
    result = (number + int(offset)) % int(modulus)
    prompt = (
        f"g(n) = (n + {int(offset)}) mod {int(modulus)}.\n"
        f"n = {number}\n"
        "Fill in the rule. End with `= <integer>`."
    )
    completion = f"({number} + {int(offset)}) mod {int(modulus)} = {result}"
    return prompt, completion, str(result)


def offset_batch(offset: int, values: list[int]) -> list[tuple[str, str]]:
    return [(prompt, completion) for prompt, completion, _answer in (offset_example(offset, value) for value in values)]


def offset_tasks(offset: int, values: list[int]) -> list[Task]:
    tasks = []
    for value in values:
        prompt, _completion, answer = offset_example(offset, value)
        tasks.append(Task("offset", "arith", prompt, answer, True, "dsl"))
    return tasks



def affine_example(a: int, b: int, value: int, modulus: int = 50) -> tuple[str, str, str]:
    """Linear rule the 1.5B rarely has at birth: (n * a + b) mod m."""
    number = int(value)
    aa, bb, mod = int(a), int(b), int(modulus)
    result = (number * aa + bb) % mod
    prompt = (
        f"h(n) = (n * {aa} + {bb}) mod {mod}.\n"
        f"n = {number}\n"
        "Fill in the rule. End with `= <integer>`."
    )
    completion = f"({number} * {aa} + {bb}) mod {mod} = {result}"
    return prompt, completion, str(result)


def affine_batch(a: int, b: int, values: list[int]) -> list[tuple[str, str]]:
    return [(prompt, completion) for prompt, completion, _ in (affine_example(a, b, value) for value in values)]


def affine_tasks(a: int, b: int, values: list[int]) -> list[Task]:
    tasks = []
    for value in values:
        prompt, _completion, answer = affine_example(a, b, value)
        tasks.append(Task(f"affine-{a}-{b}", "arith", prompt, answer, True, "dsl"))
    return tasks


def _second_spec(cfg: dict) -> dict:
    """How the stack's second skill is built. Prefer affine; offset remains available."""
    kind = str(cfg.get("second_kind") or "affine")
    if kind == "offset":
        offsets = list(cfg.get("second_offsets") or [cfg.get("second_offset", 13), 17, 19, 23, 29, 37, 41])
        return {"kind": "offset", "candidates": [{"offset": int(o)} for o in offsets]}
    affines = list(cfg.get("second_affines") or [[3, 17], [4, 13], [5, 9], [7, 11], [3, 23], [8, 19], [6, 29]])
    return {"kind": "affine", "candidates": [{"a": int(a), "b": int(b)} for a, b in affines]}


def _second_batch(spec: dict, values: list[int]) -> list[tuple[str, str]]:
    if spec["kind"] == "offset":
        return offset_batch(int(spec["offset"]), values)
    return affine_batch(int(spec["a"]), int(spec["b"]), values)


def _second_tasks(spec: dict, values: list[int]) -> list[Task]:
    if spec["kind"] == "offset":
        return offset_tasks(int(spec["offset"]), values)
    return affine_tasks(int(spec["a"]), int(spec["b"]), values)


def _pick_second(act, cfg: dict, report_x: list[int]) -> dict:
    """Pick the first candidate with birth < 0.5 on the report odds."""
    meta = _second_spec(cfg)
    probed = []
    for cand in meta["candidates"]:
        spec = {"kind": meta["kind"], **cand}
        birth = _score(act, _second_tasks(spec, report_x))["rate"]
        probed.append({**spec, "birth": birth})
        print(f"[fit] second probe {spec} birth={birth}", flush=True)
        if birth < 0.5:
            return {**spec, "birth": birth, "probed": probed}
    # None hard enough — return the hardest (lowest birth) so the report is honest.
    best = min(probed, key=lambda row: row["birth"]) if probed else {"kind": meta["kind"], "birth": 1.0, "probed": []}
    return {**best, "probed": probed, "all_easy": True}




def _stack_signal(evo, act, genome, cfg, family, added, picked, second_birth, report_x, select_x, add_pairs):
    """H-signal: on-policy keep_successes + verifier fallback on a fresh skill2 adapter."""
    import random
    from evo.generate import generate
    from evo.model import adapter_state, add_named_adapter, load_adapter_state, LORA_SITES
    from evo.outer_loop import sft_policy
    from evo.plastic.sites import CAP, planned_writes
    from evo.plastic.signal import learning_signal, with_verifier
    from evo.bench.families import check_task

    rng = random.Random(int(cfg.get("seed", 0)) + 77)
    add_snap = adapter_state(evo.model, "policy")
    slot_name = str(cfg.get("slot_name") or "skill2")
    add_named_adapter(evo, slot_name)
    signal = learning_signal(cfg)
    epochs = int(cfg.get("signal_epochs", cfg.get("slot_epochs", 6)))
    holdout = set(report_x) | set(select_x)
    dense_vals = [n for n in range(0, 50) if n not in holdout]
    rng_pick = random.Random(int(cfg.get("seed", 0)) + 3)
    cap = int(cfg.get("signal_tasks", 16))
    if len(dense_vals) > cap:
        dense_vals = sorted(rng_pick.sample(dense_vals, cap))
    tasks = _second_tasks(picked, dense_vals)
    print(
        f"[fit] second_phase=signal adapter={slot_name} epochs={epochs} tasks={len(tasks)} "
        f"grpo_k={signal['grpo_k']} temp={signal['temperature']}",
        flush=True,
    )
    rates = []
    add_hold = []
    snaps = []
    sources_all = []
    for epoch in range(epochs):
        order = list(tasks)
        rng.shuffle(order)
        pairs = []
        epoch_sources = []
        for task in order:
            samples = []
            for _ in range(signal["grpo_k"]):
                samples.append(
                    generate(
                        evo,
                        task.prompt,
                        int(cfg.get("max_new_code", 24)),
                        float(signal["temperature"]),
                        slot_name,
                        max_len=int(cfg.get("max_seq_len", 256)),
                    )
                )
            chosen = with_verifier(
                task.prompt,
                samples,
                lambda reply, task=task: check_task(task, reply),
                task.answer,
            )
            pairs.extend(chosen["pairs"])
            epoch_sources.append(chosen["source"])
        # Also mix gold dense SFT so verifier path is not alone
        gold = _second_batch(picked, dense_vals)
        rng.shuffle(gold)
        train_pairs = pairs + gold[: max(8, len(pairs))]
        rng.shuffle(train_pairs)
        plan = planned_writes(genome)
        keep = cfg.get("fit_sites")
        if keep:
            have = {row["site"] for row in plan}
            for site in set(keep):
                if site not in have and site in LORA_SITES:
                    plan.append({"site": site, "modules": list(LORA_SITES[site]), "lr": CAP})
            plan = [row for row in plan if row["site"] in set(keep)]
        steps = 0
        for row in plan:
            stats = sft_policy(
                evo,
                train_pairs,
                float(row["lr"]),
                1,
                int(cfg.get("max_seq_len", 256)),
                adapter=slot_name,
                sites=list(row["modules"]),
            )
            steps += int(stats.get("steps") or 0)

        def act_slot(task, _adapter=slot_name):
            return generate(
                evo, task.prompt, int(cfg.get("max_new_code", 24)), 0.0, _adapter,
                max_len=int(cfg.get("max_seq_len", 256)),
            )

        sr = _score(act_slot, _second_tasks(picked, select_x))["rate"]
        load_adapter_state(evo.model, "policy", add_snap)
        ar = _score(act, op_tasks(family, "left", select_x))["rate"]
        rates.append(sr)
        add_hold.append(ar)
        snaps.append(adapter_state(evo.model, slot_name))
        sources_all.append(epoch_sources)
        on_pol = sum(1 for s in epoch_sources if s == "on_policy")
        print(
            f"[fit] signal epoch {epoch + 1} second={sr} add_hold={ar} steps={steps} "
            f"on_policy={on_pol}/{len(epoch_sources)} pairs={len(pairs)}",
            flush=True,
        )

    best_i, best_sr = 0, -1.0
    for i, (sr, ar) in enumerate(zip(rates, add_hold)):
        if ar >= 0.6 and sr >= best_sr:
            best_sr, best_i = sr, i
    load_adapter_state(evo.model, slot_name, snaps[best_i])
    print(f"[fit] signal kept epoch {best_i + 1} select={rates[best_i]}", flush=True)

    def act_slot_final(task):
        return generate(
            evo, task.prompt, int(cfg.get("max_new_code", 24)), 0.0, slot_name,
            max_len=int(cfg.get("max_seq_len", 256)),
        )

    second_report = _score(act_slot_final, _second_tasks(picked, report_x))["rate"]
    load_adapter_state(evo.model, "policy", add_snap)
    add_report = _score(act, op_tasks(family, "left", report_x))["rate"]
    passed = (
        second_birth < 0.5
        and second_report >= 0.6
        and add_report >= 0.6
        and added["add_rate"] >= 0.6
        and not picked.get("all_easy")
    )
    print(f"[fit] signal done second_report={second_report} add_report={add_report} passed={passed}", flush=True)
    out = {
        "family": family.id,
        "skill": "stack",
        "birth": added["birth"],
        "add_rate": added["add_rate"],
        "add_kept": add_report,
        "gain": added["gain"],
        "second_kind": picked.get("kind"),
        "second_spec": {k: picked[k] for k in ("kind", "a", "b", "offset") if k in picked},
        "second_birth": second_birth,
        "second_report": second_report,
        "second_kept_epoch": best_i + 1,
        "second_select": rates,
        "add_select": add_hold,
        "second_probed": picked.get("probed"),
        "slot": slot_name,
        "signal": {"grpo_k": signal["grpo_k"], "temperature": signal["temperature"]},
        "passed": passed,
        "steps": added["steps"],
    }
    if "offset" in picked:
        out["second_offset"] = picked["offset"]
    if not passed:
        out["recommendation"] = (
            "H-signal did not clear second_report>=0.6 with add held. "
            "Next: H-base (larger model) or curriculum redesign; do not lower 0.6."
        )
    return out

def _stack_slot(evo, act, genome, cfg, family, added, picked, second_birth, report_x, select_x, add_pairs):
    """Train second skill on a fresh adapter; keep add frozen in policy."""
    import random
    from evo.generate import generate
    from evo.model import adapter_state, add_named_adapter, load_adapter_state, LORA_SITES
    from evo.outer_loop import sft_policy
    from evo.plastic.sites import CAP, planned_writes

    rng = random.Random(int(cfg.get("seed", 0)) + 91)
    add_snap = adapter_state(evo.model, "policy")
    slot_name = str(cfg.get("slot_name") or "skill2")
    add_named_adapter(evo, slot_name)
    slot_epochs = int(cfg.get("slot_epochs", 8))
    holdout = set(report_x) | set(select_x)
    dense_vals = [n for n in range(0, 40) if n not in holdout]
    dense_second = _second_batch(picked, dense_vals)
    print(f"[fit] second_phase=slot adapter={slot_name} epochs={slot_epochs} dense={len(dense_second)}", flush=True)
    slot_rates = []
    add_hold = []
    slot_snaps = []
    for epoch in range(slot_epochs):
        order = list(dense_second)
        rng.shuffle(order)
        plan = planned_writes(genome)
        keep = cfg.get("fit_sites")
        if keep:
            have = {row["site"] for row in plan}
            for site in set(keep):
                if site not in have and site in LORA_SITES:
                    plan.append({"site": site, "modules": list(LORA_SITES[site]), "lr": CAP})
            plan = [row for row in plan if row["site"] in set(keep)]
        steps = 0
        for row in plan:
            stats = sft_policy(
                evo, order, float(row["lr"]), 1, int(cfg.get("max_seq_len", 256)),
                adapter=slot_name, sites=list(row["modules"]),
            )
            steps += int(stats.get("steps") or 0)

        def act_slot(task, _adapter=slot_name):
            return generate(
                evo, task.prompt, int(cfg.get("max_new_code", 24)), 0.0, _adapter,
                max_len=int(cfg.get("max_seq_len", 256)),
            )

        sr = _score(act_slot, _second_tasks(picked, select_x))["rate"]
        load_adapter_state(evo.model, "policy", add_snap)
        ar = _score(act, op_tasks(family, "left", select_x))["rate"]
        slot_rates.append(sr)
        add_hold.append(ar)
        slot_snaps.append(adapter_state(evo.model, slot_name))
        print(f"[fit] slot epoch {epoch + 1} second={sr} add_hold={ar} steps={steps}", flush=True)

    # Restore best slot epoch: max second select with add_hold >= 0.6
    best_i = 0
    best_sr = -1.0
    for i, (sr, ar) in enumerate(zip(slot_rates, add_hold)):
        if ar >= 0.6 and sr >= best_sr:
            best_sr = sr
            best_i = i
    load_adapter_state(evo.model, slot_name, slot_snaps[best_i])
    print(f"[fit] slot kept epoch {best_i + 1} select={slot_rates[best_i]}", flush=True)

    def act_slot_final(task):
        return generate(
            evo, task.prompt, int(cfg.get("max_new_code", 24)), 0.0, slot_name,
            max_len=int(cfg.get("max_seq_len", 256)),
        )

    second_report = _score(act_slot_final, _second_tasks(picked, report_x))["rate"]
    load_adapter_state(evo.model, "policy", add_snap)
    add_report = _score(act, op_tasks(family, "left", report_x))["rate"]
    passed = (
        second_birth < 0.5
        and second_report >= 0.6
        and add_report >= 0.6
        and added["add_rate"] >= 0.6
        and not picked.get("all_easy")
    )
    print(f"[fit] slot done second_report={second_report} add_report={add_report} passed={passed}", flush=True)
    out = {
        "family": family.id,
        "skill": "stack",
        "birth": added["birth"],
        "add_rate": added["add_rate"],
        "add_kept": add_report,
        "gain": added["gain"],
        "second_kind": picked.get("kind"),
        "second_spec": {k: picked[k] for k in ("kind", "a", "b", "offset") if k in picked},
        "second_birth": second_birth,
        "second_report": second_report,
        "second_kept_epoch": best_i + 1,
        "second_select": slot_rates,
        "add_select": add_hold,
        "second_probed": picked.get("probed"),
        "slot": slot_name,
        "passed": passed,
        "steps": added["steps"],
    }
    if "offset" in picked:
        out["second_offset"] = picked["offset"]
    if not passed:
        out["recommendation"] = (
            "Slot phase did not clear second_report>=0.6 with add held. "
            "Try denser drills, H-signal (on-policy), or larger base; do not lower 0.6."
        )
    return out


def _stack(evo, act, genome: Genome, cfg: dict, family: Family) -> dict:
    """Learn addition, then a second rule that is hard at birth.

    Default second skill is an affine `(n * a + b) mod 50` chosen so birth < 0.5
    on the report odds. Offset +13 is often already known on Qwen2.5-1.5B.
    An epoch that drops addition below the keep floor is discarded.
    """
    import random

    from evo.model import adapter_state, load_adapter_state
    from evo.plastic.sites import apply_planned_updates

    added = _stable_add(evo, act, genome, cfg, family)
    report_x = list(cfg.get("second_report_x") or [31, 33, 35, 37])
    select_x = list(cfg.get("second_select_x") or [21, 23, 25, 27])
    picked = _pick_second(act, cfg, report_x)
    second_birth = float(picked["birth"])
    add_pairs = op_batch(family, "left", list(range(0, 21, 2)))
    phase = str(cfg.get("second_phase") or "")
    if phase == "slot":
        return _stack_slot(evo, act, genome, cfg, family, added, picked, second_birth, report_x, select_x, add_pairs)
    if phase == "signal":
        return _stack_signal(evo, act, genome, cfg, family, added, picked, second_birth, report_x, select_x, add_pairs)
    second_pairs = _second_batch(picked, list(range(0, 21, 2)))
    epochs = int(cfg.get("fit_epochs", 4))
    snaps = [adapter_state(evo.model, "policy")]
    second_rates = [_score(act, _second_tasks(picked, select_x))["rate"]]
    add_rates = [_score(act, op_tasks(family, "left", select_x))["rate"]]
    rng = random.Random(int(cfg.get("seed", 0)) + 17)
    for epoch in range(epochs):
        order = list(add_pairs + second_pairs)
        rng.shuffle(order)
        stats = apply_planned_updates(evo, order, genome, cfg, epochs=1)
        second_rates.append(_score(act, _second_tasks(picked, select_x))["rate"])
        add_rates.append(_score(act, op_tasks(family, "left", select_x))["rate"])
        snaps.append(adapter_state(evo.model, "policy"))
        print(
            f"[fit] second epoch {epoch + 1} second={second_rates[-1]} add={add_rates[-1]} steps={stats['steps']}",
            flush=True,
        )
    if str(cfg.get("second_phase") or "") == "solo" and max(second_rates) < 0.6:
        solo_epochs = int(cfg.get("solo_epochs", max(4, epochs)))
        print(f"[fit] second_phase=solo for {solo_epochs} epochs", flush=True)
        for epoch in range(solo_epochs):
            order = list(second_pairs + second_pairs + add_pairs[: max(1, len(add_pairs) // 4)])
            rng.shuffle(order)
            stats = apply_planned_updates(evo, order, genome, cfg, epochs=1)
            second_rates.append(_score(act, _second_tasks(picked, select_x))["rate"])
            add_rates.append(_score(act, op_tasks(family, "left", select_x))["rate"])
            snaps.append(adapter_state(evo.model, "policy"))
            print(
                f"[fit] solo epoch {epoch + 1} second={second_rates[-1]} add={add_rates[-1]} steps={stats['steps']}",
                flush=True,
            )
    chosen = choose_epoch(second_rates, add_rates)
    load_adapter_state(evo.model, "policy", snaps[chosen])
    second_report = _score(act, _second_tasks(picked, report_x))["rate"]
    add_report = _score(act, op_tasks(family, "left", report_x))["rate"]
    print(
        f"[fit] stack kept {chosen} second_report={second_report} add_report={add_report} "
        f"second_birth={second_birth} spec={ {k: picked[k] for k in picked if k not in {'probed', 'all_easy'}} }",
        flush=True,
    )
    passed = (
        second_birth < 0.5
        and second_report >= 0.6
        and add_report >= 0.6
        and added["add_rate"] >= 0.6
        and not picked.get("all_easy")
    )
    out = {
        "family": family.id,
        "skill": "stack",
        "birth": added["birth"],
        "add_rate": added["add_rate"],
        "add_kept": add_report,
        "gain": added["gain"],
        "second_kind": picked.get("kind"),
        "second_spec": {k: picked[k] for k in ("kind", "a", "b", "offset") if k in picked},
        "second_birth": second_birth,
        "second_report": second_report,
        "second_kept_epoch": chosen,
        "second_select": second_rates,
        "add_select": add_rates,
        "second_probed": picked.get("probed"),
        "passed": passed,
        "steps": added["steps"],
    }
    if "offset" in picked:
        out["second_offset"] = picked["offset"]
    if picked.get("all_easy"):
        out["recommendation"] = (
            "Every second-skill candidate was already >= 0.5 at birth. "
            "Widen second_affines / second_offsets; do not lower the 0.6 gate."
        )
    return out


def _adapter_dir(cfg: dict):
    from pathlib import Path

    from evo.util import repo_path

    raw = Path(str(cfg.get("adapter_dir") or "runs/evoplast_adapter"))
    return raw if raw.is_absolute() else repo_path(raw)


def _sites(genome: Genome, cfg: dict) -> list[dict]:
    from evo.model import LORA_SITES
    from evo.plastic.sites import CAP, planned_writes

    rows = planned_writes(genome)
    keep = cfg.get("fit_sites")
    if keep:
        keep_set = set(keep)
        have = {row["site"] for row in rows}
        for site in keep_set:
            if site not in have and site in LORA_SITES:
                rows.append({"site": site, "modules": list(LORA_SITES[site]), "lr": CAP})
        rows = [row for row in rows if row["site"] in keep_set]
    return rows


def _score(act, tasks: list[Task]) -> dict:
    hits = []
    for task in tasks:
        got = grade_reply(act(task))
        hits.append(got is not None and got == int(task.answer))
    rate = sum(hits) / len(hits) if hits else 0.0
    return {"hits": hits, "rate": rate}
