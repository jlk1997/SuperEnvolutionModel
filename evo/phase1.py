"""Phase 1: self-edit knowledge updates, forgetting, and retention ablations."""

from __future__ import annotations

import random
import traceback

from evo.consolidate import gate_accept, peak_accept, peak_drop, positive_gain, retention_reward
from evo.data import clip_passage, load_passages, load_probe
from evo.eval.retention import (
    matrix_stats,
    retention_curve,
    save_bars,
    save_curves,
    save_heatmap,
    write_matrix_csv,
)
from evo.generate import (
    blind_edit_prompt,
    clean_edit,
    edit_prompt,
    generate,
    score_passages,
    score_questions,
)
from evo.inner_loop import adapt_scratch, build_distill_cache, build_memory_cache, kl_between
from evo.model import build_model, release
from evo.questions import question_splits, with_qas
from evo.outer_loop import sft_policy
from evo.runlog import Run
from evo.util import mean, set_seed


def _qs(passage: dict, cfg: dict) -> list[dict]:
    return passage["qas"][: cfg["questions_per_passage"]]


def _clip_all(passages: list[dict], cfg: dict) -> list[dict]:
    return [clip_passage(passage, cfg["max_passage_chars"]) for passage in passages]


def select_unknown(evo, passages: list[dict], n: int, cfg: dict) -> tuple[list[dict], list[dict]]:
    """Prefer passages the frozen model cannot already answer."""
    ranked = []
    for index, passage in enumerate(passages):
        if cfg.get("split_questions"):
            visible = question_splits(passage, cfg)[0]
        else:
            visible = _qs(passage, cfg)
        stats = score_questions(evo, visible, None, cfg["answer_tokens"])
        ranked.append((stats["f1"], passage["id"], passage))
        print(f"[data] filter {index + 1}/{len(passages)} id={passage['id']} base_f1={stats['f1']:.3f}", flush=True)
    ranked.sort(key=lambda item: (item[0], item[1]))
    chosen = [item[2] for item in ranked[:n]]
    random.Random(cfg["seed"]).shuffle(chosen)
    report = [{"id": item[1], "base_f1": item[0]} for item in ranked]
    return chosen, report


def prepare_passages(evo, cfg: dict, n: int) -> tuple[list[dict], str, list[dict]]:
    pool, source = load_passages(cfg, max(n, cfg.get("candidate_pool", n)))
    pool = _clip_all(pool, cfg)
    chosen, report = select_unknown(evo, pool, n, cfg)
    return chosen, source, report


def _sample_edits(evo, passage: dict, cfg: dict) -> tuple[str, list[str]]:
    practice, _gate, _exam = question_splits(passage, cfg)
    if cfg.get("edit_sees_questions", True):
        prompt = edit_prompt(passage, practice)
    else:
        prompt = blind_edit_prompt(passage)
    edits = []
    for _ in range(cfg["n_edits"]):
        raw = generate(evo, prompt, cfg["edit_tokens"], cfg["temperature"], "policy")
        edits.append(clean_edit(raw))
    return prompt, edits


def _adapt_from_identity(evo, text: str, cfg: dict) -> float:
    evo.reset_scratch()
    loss, _ = adapt_scratch(
        evo,
        text,
        cfg["inner_steps"],
        cfg["inner_lr"],
        cfg["max_seq_len"],
    )
    return loss


def _mean_f1(rows: list[dict]) -> dict:
    return {
        "f1": mean([row["f1"] for row in rows]) or 0.0,
        "em": mean([row["em"] for row in rows]) or 0.0,
        "per_passage": rows,
    }


def _score_edit_from_base(evo, passage: dict, edit: str, cfg: dict) -> dict | None:
    if not edit.strip():
        return None
    loss = _adapt_from_identity(evo, edit, cfg)
    stats = score_questions(evo, _qs(passage, cfg), "scratch", cfg["answer_tokens"])
    return {"edit": edit, "loss": loss, **stats}


def evaluate_self_edits(evo, passages: list[dict], cfg: dict) -> dict:
    per = []
    for index, passage in enumerate(passages):
        set_seed(cfg["seed"] + 500 + index)
        _prompt, edits = _sample_edits(evo, passage, cfg)
        scored = []
        for edit in edits:
            item = _score_edit_from_base(evo, passage, edit, cfg)
            if item is not None:
                scored.append(item)
        if not scored:
            empty = score_questions(evo, _qs(passage, cfg), None, cfg["answer_tokens"])
            per.append({"id": passage["id"], "f1": empty["f1"], "em": empty["em"], "edits": 0, "rows": empty["rows"]})
            continue
        per.append(
            {
                "id": passage["id"],
                "f1": mean([item["f1"] for item in scored]),
                "em": mean([item["em"] for item in scored]),
                "best_f1": max(item["f1"] for item in scored),
                "edits": len(scored),
                "rows": scored[0]["rows"],
            }
        )
    return _mean_f1(per)


def evaluate_passage_training(evo, passages: list[dict], cfg: dict) -> dict:
    per = []
    for passage in passages:
        _adapt_from_identity(evo, passage["context"], cfg)
        stats = score_questions(evo, _qs(passage, cfg), "scratch", cfg["answer_tokens"])
        per.append({"id": passage["id"], "f1": stats["f1"], "em": stats["em"], "rows": stats["rows"]})
    return _mean_f1(per)


def train_policy(evo, passages: list[dict], cfg: dict, run: Run) -> dict:
    winners = []
    considered = 0
    for index, passage in enumerate(passages):
        set_seed(cfg["seed"] + 800 + index)
        base = score_questions(evo, _qs(passage, cfg), None, cfg["answer_tokens"])
        prompt, edits = _sample_edits(evo, passage, cfg)
        for edit in edits:
            considered += 1
            item = _score_edit_from_base(evo, passage, edit, cfg)
            if item is None:
                continue
            reward = item[cfg["reward_metric"]] - base[cfg["reward_metric"]]
            run.log(
                {
                    "event": "outer_candidate",
                    "passage": passage["id"],
                    "reward": reward,
                    "f1": item["f1"],
                    "base_f1": base["f1"],
                }
            )
            if reward > cfg["reward_threshold"]:
                winners.append((prompt, edit))
    stats = sft_policy(
        evo,
        winners,
        cfg["outer_lr"],
        cfg["outer_epochs"],
        cfg["max_seq_len"],
    )
    stats["considered"] = considered
    stats["kept"] = len(winners)
    run.log({"event": "outer_update", **{k: v for k, v in stats.items() if k != "pairs" or True}})
    if winners:
        run.commit_adapter(evo.model, "policy", {"kind": "rest_em", "kept": len(winners)})
    return stats


def run_baselines(cfg: dict) -> dict:
    set_seed(cfg["seed"])
    run = Run(cfg["runs_root"], "phase1_baselines", cfg)
    evo = None
    try:
        evo = build_model(cfg)
        n = cfg["n_train"] + cfg["n_test"]
        passages, source, report = prepare_passages(evo, cfg, n)
        train, test = passages[: cfg["n_train"]], passages[cfg["n_train"] :]
        run.log({"event": "data", "source": source, "train": [p["id"] for p in train], "test": [p["id"] for p in test]})
        print("[baselines] no_adapt", flush=True)
        no_adapt = score_passages(evo, test, None, cfg["questions_per_passage"], cfg["answer_tokens"])
        print(f"[baselines] passage f1_so_far_no_adapt={no_adapt['f1']:.3f}", flush=True)
        passage = evaluate_passage_training(evo, test, cfg)
        print(f"[baselines] self_edit_untrained passage_f1={passage['f1']:.3f}", flush=True)
        untrained = evaluate_self_edits(evo, test, cfg)
        print(f"[baselines] outer untrained_f1={untrained['f1']:.3f}", flush=True)
        outer = train_policy(evo, train, cfg, run)
        print(f"[baselines] seal kept={outer['kept']}", flush=True)
        seal = evaluate_self_edits(evo, test, cfg)
        summary = {
            "data_source": source,
            "filter": report,
            "vram_mb": evo.vram_mb(),
            "conditions": {
                "no_adapt": {"f1": no_adapt["f1"], "em": no_adapt["em"], "per_passage": no_adapt["per_passage"]},
                "passage": passage,
                "self_edit_untrained": untrained,
                "seal": seal,
            },
            "outer": outer,
            "primary_metric": "mean no-context F1 over self-edits, not the best-of-k",
        }
        run.save_json("summary.json", summary)
        run.log({"event": "baselines_done", "no_adapt": no_adapt["f1"], "passage": passage["f1"], "untrained": untrained["f1"], "seal": seal["f1"]})
        print(f"[baselines] wrote {run.dir}", flush=True)
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        release(evo)


def _candidate(
    evo,
    passage,
    edit,
    old_passages,
    new_before,
    cfg,
    method: str,
    replay_text: str | None = None,
) -> dict | None:
    if not edit.strip():
        return None
    evo.copy_memory_to_scratch()
    cache = None
    kl_coef = 0.0
    if method == "kl":
        cache = build_distill_cache(
            evo,
            passage["context"],
            _qs(passage, cfg),
            cfg["answer_tokens"],
            cfg["distill_questions"],
        )
        kl_coef = cfg["kl_coef"]
    elif method in ("anchor", "replay", "strict", "probe"):
        remembered = []
        for earlier in old_passages:
            remembered.extend(earlier["qas"][:1])
        cache = build_memory_cache(
            evo,
            remembered,
            cfg["answer_tokens"],
            cfg["distill_questions"],
            adapter="memory",
        )
        kl_coef = cfg["kl_coef"] if cache else 0.0
    loss, _ = adapt_scratch(
        evo,
        edit,
        cfg["inner_steps"],
        cfg["inner_lr"],
        cfg["max_seq_len"],
        kl_coef=kl_coef,
        distill_cache=cache,
        replay_text=replay_text if method == "replay" else None,
        replay_coef=cfg.get("replay_coef", 0.5),
    )
    new_after = score_questions(evo, _qs(passage, cfg), "scratch", cfg["answer_tokens"])
    old_after = score_passages(evo, old_passages, "scratch", cfg["questions_per_passage"], cfg["answer_tokens"])
    drift = kl_between(evo, passage["context"][:400], "memory", "scratch", min(128, cfg["max_seq_len"]))
    metric = cfg["reward_metric"]
    gain = new_after[metric] - new_before[metric]
    reward = retention_reward(new_before[metric], new_after[metric], 0.0, 0.0, 0.0)
    # old scores are filled by the caller via old_before; placeholder replaced below
    return {
        "edit": edit,
        "loss": loss,
        "new_f1": new_after["f1"],
        "new_em": new_after["em"],
        "old_f1": old_after["f1"],
        "gain": gain,
        "kl": drift,
        "per_f1": {item["id"]: item["f1"] for item in old_after["per_passage"]},
        "state": evo.snapshot("scratch"),
        "reward_gain_only": reward,
    }


def run_sequence(evo, passages: list[dict], cfg: dict, method: str, run: Run) -> dict:
    probe = load_probe(cfg)
    probe_before = score_questions(evo, probe["qas"], "memory", cfg["answer_tokens"])
    matrix: list[list[float | None]] = []
    accepted = 0
    peaks = {probe["id"]: probe_before["f1"]}
    accepted_edits: list[str] = []
    for index, passage in enumerate(passages):
        print(f"[sequence] method={method} step={index + 1}/{len(passages)} id={passage['id']}", flush=True)
        set_seed(cfg["seed"] + 1000 + index)
        previous = passages[:index]
        graded_prev = [with_qas(item, question_splits(item, cfg)[1]) for item in previous]
        old_passages = [probe] + graded_prev
        old_before = score_passages(evo, old_passages, "memory", cfg["questions_per_passage"], cfg["answer_tokens"])
        graded_new = with_qas(passage, question_splits(passage, cfg)[1])
        new_before = score_questions(evo, graded_new["qas"], "memory", cfg["answer_tokens"])
        _prompt, edits = _sample_edits(evo, passage, cfg)
        candidates = []
        for edit_index, edit in enumerate(edits):
            print(f"[sequence] edit {edit_index + 1}/{len(edits)} device={evo.device}", flush=True)
            replay_text = "\n".join(accepted_edits) if method == "replay" else None
            item = _candidate(
                evo,
                graded_new,
                edit,
                old_passages,
                new_before,
                cfg,
                method,
                replay_text=replay_text,
            )
            if item is None:
                continue
            item["reward"] = retention_reward(
                new_before["f1"],
                item["new_f1"],
                old_before["f1"],
                item["old_f1"],
                cfg["lam"],
            )
            item["accept_gate"] = gate_accept(
                old_before["f1"],
                item["old_f1"],
                item["kl"],
                cfg["max_f1_drop"],
                cfg["max_kl"],
            )
            min_peak = float(cfg.get("min_peak") or 0.0) if method == "probe" else 0.0
            found = peak_drop(peaks, item["per_f1"], min_peak)
            item["worst_drop"] = None if found is None else [found[0], found[1]]
            item["accept_peak"] = peak_accept(peaks, item["per_f1"], cfg["max_f1_drop"], min_peak)
            candidates.append(item)
        choice = None
        accept = False
        if candidates:
            if method in ("peak", "anchor", "replay", "strict", "probe"):
                viable = [item for item in candidates if item["accept_peak"]]
                if method in ("strict", "probe"):
                    floor = float(cfg.get("min_gain", 0.02))
                    viable = [
                        item
                        for item in viable
                        if positive_gain(True, item["gain"], item["reward"], floor)
                    ]
                if viable:
                    choice = max(viable, key=lambda item: item["reward"])
                    accept = True
            elif method == "reward":
                choice = max(candidates, key=lambda item: item["reward"])
                accept = True
            elif method == "gate":
                viable = [item for item in candidates if item["accept_gate"]]
                if viable:
                    choice = max(viable, key=lambda item: item["gain"])
                    accept = True
            else:
                choice = max(candidates, key=lambda item: item["gain"])
                accept = True
        if accept and choice is not None:
            evo.restore("scratch", choice["state"])
            evo.copy_scratch_to_memory()
            accepted += 1
            accepted_edits.append(choice["edit"])
            run.commit_adapter(
                evo.model,
                "memory",
                {
                    "kind": "consolidate",
                    "method": method,
                    "passage": passage["id"],
                    "reward": choice["reward"],
                    "gain": choice["gain"],
                    "kl": choice["kl"],
                    "edit": choice["edit"][:500],
                },
            )
        for item in candidates:
            item.pop("state", None)
        row = []
        for seen_index, earlier in enumerate(passages):
            if seen_index > index:
                row.append(None)
                continue
            _practice, gate_qs, exam_qs = question_splits(earlier, cfg)
            stats = score_questions(evo, exam_qs, "memory", cfg["answer_tokens"])
            row.append(stats["f1"])
            if gate_qs == exam_qs:
                gate_f1 = stats["f1"]
            else:
                gate_f1 = score_questions(evo, gate_qs, "memory", cfg["answer_tokens"])["f1"]
            peaks[earlier["id"]] = max(peaks.get(earlier["id"], gate_f1), gate_f1)
        if accept and choice is not None:
            for key, value in choice["per_f1"].items():
                peaks[key] = max(peaks.get(key, value), value)
        matrix.append(row)
        run.log(
            {
                "event": "sequence",
                "method": method,
                "step": index,
                "passage": passage["id"],
                "accepted": accept,
                "candidates": len(candidates),
                "gain": None if choice is None else choice["gain"],
                "reward": None if choice is None else choice["reward"],
                "kl": None if choice is None else choice["kl"],
                "candidate_gains": [item["gain"] for item in candidates],
                "candidate_rewards": [item["reward"] for item in candidates],
                "candidate_peak": [bool(item["accept_peak"]) for item in candidates],
                "candidate_worst": [item.get("worst_drop") for item in candidates],
                "row": row,
            }
        )
    probe_after = score_questions(evo, probe["qas"], "memory", cfg["answer_tokens"])
    stats = matrix_stats(matrix)
    return {
        "method": method,
        "accepted": accepted,
        "matrix": matrix,
        "curve": retention_curve(matrix),
        "probe_before_f1": probe_before["f1"],
        "probe_after_f1": probe_after["f1"],
        **stats,
    }


def _save_sequence_plots(run: Run, result: dict, stem: str) -> None:
    write_matrix_csv(result["matrix"], run.dir / f"{stem}_matrix.csv")
    save_heatmap(result["matrix"], run.dir / f"{stem}_matrix.png", stem)
    save_curves({stem: result["curve"]}, run.dir / f"{stem}_curve.png", stem)


def run_continual(cfg: dict) -> dict:
    set_seed(cfg["seed"])
    run = Run(cfg["runs_root"], "phase1_continual", cfg)
    evo = None
    try:
        evo = build_model(cfg)
        passages, source, report = prepare_passages(evo, cfg, cfg["n_passages"])
        result = run_sequence(evo, passages, cfg, cfg.get("method", "none"), run)
        summary = {"data_source": source, "filter": report, "vram_mb": evo.vram_mb(), **result}
        run.save_json("summary.json", summary)
        _save_sequence_plots(run, result, "continual")
        run.log({"event": "continual_done", **matrix_stats(result["matrix"])})
        print(f"[continual] wrote {run.dir}", flush=True)
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        release(evo)


def run_antiforget(cfg: dict) -> dict:
    set_seed(cfg["seed"])
    run = Run(cfg["runs_root"], cfg.get("run_name", "phase1_antiforget"), cfg)
    evo = None
    try:
        evo = build_model(cfg)
        passages, source, report = prepare_passages(evo, cfg, cfg["n_passages"])
        release(evo)
        evo = None
        results = {}
        for method in cfg["methods"]:
            evo = build_model(cfg)
            results[method] = run_sequence(evo, passages, cfg, method, run)
            _save_sequence_plots(run, results[method], method)
            release(evo)
            evo = None
        summary = {"data_source": source, "filter": report, "methods": results}
        run.save_json("summary.json", summary)
        save_bars(
            {name: {"mean_immediate_f1": item["mean_immediate_f1"], "final_retention_f1": item["final_retention_f1"]} for name, item in results.items()},
            run.dir / "ablation.png",
        )
        save_curves({name: item["curve"] for name, item in results.items()}, run.dir / "ablation_curves.png", "retention")
        run.log({"event": "ablation_done", "retention": {name: item["final_retention_f1"] for name, item in results.items()}})
        print(f"[antiforget] wrote {run.dir}", flush=True)
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        release(evo)
