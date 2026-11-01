"""Phase 2: proposer/solver self-play checked by execution, not by another LLM."""

from __future__ import annotations

import traceback

from evo.consolidate import gate_accept
from evo.data import load_probe
from evo.generate import first_line, generate, score_questions
from evo.model import build_model, release
from evo.outer_loop import sft_policy
from evo.runlog import Run
from evo.selfplay.heldout import confidence_prompt, verification_gap
from evo.selfplay.tasks import (
    TASK_TYPES,
    check_solver,
    gold_answer,
    is_example_copy,
    learnability,
    materialize,
    mutate_program,
    parse_proposal,
    proposer_prompt,
    render_proposal,
    solver_prompt,
    worked_example,
)
from evo.util import mean, set_seed


def _outcomes(evo, cfg: dict, task: dict):
    solve_prompt = solver_prompt(task)
    outcomes = []
    for _ in range(cfg["solver_samples"]):
        answer = generate(evo, solve_prompt, cfg["max_new_code"], cfg["temperature"], "policy")
        ok = check_solver(task, answer, cfg["exec_timeout"])
        outcomes.append((ok, answer.strip()))
    rate = mean([1.0 if ok else 0.0 for ok, _answer in outcomes]) or 0.0
    return solve_prompt, outcomes, rate, learnability(rate)


def _mutate_toward_band(evo, cfg: dict, task: dict, rate: float, score: float):
    """Replace an always-solved or never-solved program with an executor-checked variant."""
    if not cfg.get("mutate") or score >= cfg["min_learnability"]:
        return task, rate, score, None, None
    direction = "harder" if rate >= 0.99 else "easier"
    depth = bool(cfg.get("mutate_depth"))
    for program in mutate_program(task["program"], direction, depth=depth):
        proposal = {"type": task["type"], "program": program}
        if task["type"] == "induction":
            proposal["inputs"] = list(task["inputs"])
        else:
            proposal["input"] = task["input"]
        trial = materialize(proposal, cfg["exec_timeout"])
        if trial is None or is_example_copy(trial["program"]):
            continue
        _prompt, trial_outcomes, trial_rate, trial_score = _outcomes(evo, cfg, trial)
        if trial_score >= cfg["min_learnability"]:
            return trial, trial_rate, trial_score, trial_outcomes, direction
    if depth and direction == "easier":
        prefix = worked_example(task, cfg["exec_timeout"])
        if prefix:
            hinted = dict(task)
            hinted["prompt_prefix"] = prefix
            _prompt, trial_outcomes, trial_rate, trial_score = _outcomes(evo, cfg, hinted)
            if trial_score >= cfg["min_learnability"]:
                return hinted, trial_rate, trial_score, trial_outcomes, "example"
    return task, rate, score, None, None


def _round(evo, cfg: dict, round_index: int) -> tuple[list[tuple[str, str]], list[dict]]:
    pairs: list[tuple[str, str]] = []
    records = []
    for type_index, task_type in enumerate(TASK_TYPES):
        for k in range(cfg["proposals_per_type"]):
            set_seed(cfg["seed"] + 50 * round_index + 10 * type_index + k)
            prompt = proposer_prompt(task_type)
            kept = None
            reason = "parse"
            attempts = int(cfg.get("proposal_attempts", 1))
            for attempt in range(attempts):
                raw = generate(evo, prompt, cfg["max_new_code"], cfg["temperature"], "policy")
                parsed = parse_proposal(raw, task_type)
                if parsed is None:
                    reason = "example_copy" if "return x + 1" in raw else "parse"
                    continue
                if cfg.get("reject_example_copy") and is_example_copy(parsed["program"]):
                    reason = "example_copy"
                    prompt = (
                        proposer_prompt(task_type)
                        + "\nThe function must not be `return x + 1`. "
                        + "Use a different arithmetic or list operation."
                    )
                    continue
                task = materialize(parsed, cfg["exec_timeout"])
                if task is None:
                    reason = "execute"
                    continue
                solve_prompt, outcomes, rate, score = _outcomes(evo, cfg, task)
                if cfg.get("curriculum") and score < cfg["min_learnability"] and attempt + 1 < attempts:
                    reason = "too_easy" if rate >= 0.99 else "too_hard"
                    hint = (
                        "The last function was too easy. Use a less obvious combination of operations."
                        if rate >= 0.99
                        else "The last function was too hard. Use one simple arithmetic or list step."
                    )
                    prompt = proposer_prompt(task_type) + "\n" + hint
                    continue
                kept = (task, raw, prompt, rate, score, outcomes, solve_prompt)
                break
            if kept is None:
                records.append({"type": task_type, "valid": False, "reason": reason})
                continue
            task, raw, prompt, rate, score, outcomes, solve_prompt = kept
            mutated_direction = None
            trial_task, trial_rate, trial_score, trial_outcomes, mutated_direction = _mutate_toward_band(
                evo, cfg, task, rate, score
            )
            if trial_outcomes is not None:
                task, rate, score, outcomes = trial_task, trial_rate, trial_score, trial_outcomes
                solve_prompt = solver_prompt(task)
            skip_solved = (cfg.get("curriculum") or cfg.get("mutate")) and rate >= 0.99
            if cfg.get("teach_gold") and not skip_solved:
                pairs.append((solve_prompt, gold_answer(task)))
            for ok, answer in outcomes:
                if ok:
                    pairs.append((solve_prompt, answer))
                if cfg.get("calibrate"):
                    claim = first_line(answer) or answer.strip()
                    pairs.append((confidence_prompt(claim), "yes" if ok else "no"))
            if score >= cfg["min_learnability"]:
                target = render_proposal(task) if mutated_direction else raw.strip()
                pairs.append((proposer_prompt(task_type), target))
            records.append(
                {
                    "type": task_type,
                    "valid": True,
                    "success_rate": rate,
                    "learnability": score,
                    "kept_proposal": score >= cfg["min_learnability"],
                    "mutated": mutated_direction is not None,
                    "mutation": mutated_direction,
                    "program": str(task.get("program", ""))[:180],
                }
            )
    return pairs, records


def run_selfplay(cfg: dict) -> dict:
    set_seed(cfg["seed"])
    run = Run(cfg["runs_root"], cfg.get("run_name", "phase2_selfplay"), cfg)
    evo = None
    try:
        evo = build_model(cfg)
        probe = load_probe(cfg)
        gap_before = verification_gap(evo, cfg)
        rounds = []
        for round_index in range(cfg["rounds"]):
            pairs, records = _round(evo, cfg, round_index)
            snapshot = evo.snapshot("policy")
            probe_before = score_questions(evo, probe["qas"], "policy", cfg["answer_tokens"])
            accuracy_before = gap_before["true_accuracy"] if not rounds else rounds[-1]["verification_gap"]["true_accuracy"]
            sft = sft_policy(evo, pairs, cfg["outer_lr"], cfg["outer_epochs"], cfg["max_seq_len"])
            probe_after = score_questions(evo, probe["qas"], "policy", cfg["answer_tokens"])
            gap = verification_gap(evo, cfg)
            keep = gate_accept(
                probe_before["f1"],
                probe_after["f1"],
                None,
                cfg["max_f1_drop"],
                None,
            )
            if cfg.get("accuracy_gate") and gap["true_accuracy"] + 1e-8 < accuracy_before:
                keep = False
            if pairs and not keep:
                evo.restore("policy", snapshot)
                gap = verification_gap(evo, cfg)
            elif pairs and keep:
                run.commit_adapter(
                    evo.model,
                    "policy",
                    {"kind": "selfplay", "round": round_index, "pairs": len(pairs)},
                )
            row = {
                "round": round_index,
                "records": records,
                "pairs": len(pairs),
                "sft": sft,
                "probe_before_f1": probe_before["f1"],
                "probe_after_f1": probe_after["f1"],
                "update_kept": bool(pairs) and keep,
                "verification_gap": gap,
            }
            rounds.append(row)
            run.log(
                {
                    "event": "selfplay_round",
                    "round": round_index,
                    "pairs": len(pairs),
                    "valid": sum(1 for item in records if item.get("valid")),
                    "kept": bool(pairs) and keep,
                    "gap": gap["verification_gap"],
                    "true_accuracy": gap["true_accuracy"],
                    "self_score": gap["self_score"],
                    "consistency": gap.get("consistency"),
                    "consistency_gap": gap.get("consistency_gap"),
                }
            )
        summary = {
            "vram_mb": evo.vram_mb(),
            "gap_before": gap_before,
            "rounds": rounds,
            "gap_after": rounds[-1]["verification_gap"] if rounds else gap_before,
            "note": "verification_gap = self_score - true_accuracy. Positive means overconfident self-judgment.",
        }
        run.save_json("summary.json", summary)
        run.log(
            {
                "event": "selfplay_done",
                "gap_before": gap_before["verification_gap"],
                "gap_after": summary["gap_after"]["verification_gap"],
                "acc_before": gap_before["true_accuracy"],
                "acc_after": summary["gap_after"]["true_accuracy"],
            }
        )
        print(f"[selfplay] wrote {run.dir}", flush=True)
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        release(evo)
