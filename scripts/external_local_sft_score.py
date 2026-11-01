"""Honest train-only SFT on external local toys, then eval score (GPU).

Not upstream ServeLearnBench / EvoArena / PATH-Bench. Gate 0.6 never lowered.
Train pairs come only from adapter phase==train; eval never enters SFT.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from evo.generate import first_line, generate, qa_prompt
from evo.model import add_named_adapter, build_model, release
from evo.office.external_scaffold import ADAPTERS
from evo.outer_loop import sft_policy
from evo.util import load_config, repo_path, set_seed


GATE = 0.6
BENCHES = ("serve_learn", "evo_arena", "path_bench")


def _norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^0-9a-z.\-]+", " ", s)
    return " ".join(s.split())


def _em(pred: str, gold: str) -> float:
    if _norm(pred) == _norm(gold) or gold in pred:
        return 1.0
    m = re.search(r"-?\d+(?:\.\d+)?", pred)
    if m and _norm(m.group(0)) == _norm(gold):
        return 1.0
    if len(gold) == 1 and gold.upper() in "ABCD":
        m2 = re.search(r"\b([ABCD])\b", pred.upper())
        if m2 and m2.group(1) == gold.upper():
            return 1.0
    return 0.0


def build_train_pairs(adapter) -> list[tuple[str, str]]:
    """Train-only (prompt, completion). Eval items must not appear."""
    pairs: list[tuple[str, str]] = []
    for item in adapter.iter_items("train"):
        task = str(item.get("task") or "").strip()
        gold = str(item.get("gold") or "").strip()
        if not task or not gold:
            continue
        pairs.append((qa_prompt(task), gold))
    return pairs


def score_eval(evo, adapter, adapter_name: str | None) -> dict:
    rows = []
    for item in adapter.iter_items("eval"):
        pred = first_line(generate(evo, qa_prompt(item["task"]), 48, 0.0, adapter_name))
        gold = str(item.get("gold", ""))
        em = _em(pred, gold)
        rows.append({"id": item["id"], "task": item["task"], "gold": gold, "pred": pred, "em": em})
    n = len(rows)
    rate = (sum(r["em"] for r in rows) / n) if n else 0.0
    return {
        "n_eval": n,
        "rate": rate,
        "pass_gate": rate >= GATE,
        "rows": rows,
    }


def train_ids(adapter) -> set[str]:
    return {str(x["id"]) for x in adapter.iter_items("train")}


def eval_ids(adapter) -> set[str]:
    return {str(x["id"]) for x in adapter.iter_items("eval")}


def main() -> None:
    cfg = load_config(repo_path("configs/office_gate2_mid_n_dual.yaml"))
    cfg["model_name"] = str(repo_path("models/Qwen2.5-1.5B-Instruct"))
    cfg["lora_preset"] = "full"
    set_seed(int(cfg.get("seed", 0)))
    epochs = int(cfg.get("external_sft_epochs", 6))
    lr = float(cfg.get("outer_lr", 5e-4))
    max_len = int(cfg.get("max_seq_len", 512))

    evo = None
    results: dict = {}
    try:
        evo = build_model(cfg)
        for bid in BENCHES:
            adapter = ADAPTERS[bid]()
            loaded = adapter.load_local()
            if not loaded.get("ok"):
                results[bid] = {"ok": False, "load": loaded}
                continue
            tr_ids = train_ids(adapter)
            ev_ids = eval_ids(adapter)
            leak = tr_ids & ev_ids
            pairs = build_train_pairs(adapter)
            bare = score_eval(evo, adapter, None)
            adapter_name = f"ext_{bid}"
            add_named_adapter(evo, adapter_name)
            train_stats = sft_policy(
                evo,
                pairs,
                lr,
                epochs,
                max_len,
                adapter=adapter_name,
            )
            trained = score_eval(evo, adapter, adapter_name)
            results[bid] = {
                "ok": True,
                "bench_id": bid,
                "local_path": loaded.get("path"),
                "n_train": loaded.get("n_train"),
                "n_eval": loaded.get("n_eval"),
                "train_ids": sorted(tr_ids),
                "eval_ids": sorted(ev_ids),
                "train_eval_overlap": sorted(leak),
                "honest_split": len(leak) == 0 and len(pairs) == len(tr_ids),
                "n_sft_pairs": len(pairs),
                "train": train_stats,
                "bare": bare,
                "trained": trained,
                "gain": trained["rate"] - bare["rate"],
                "pass_gate_bare": bare["pass_gate"],
                "pass_gate_trained": trained["pass_gate"],
                "upstream_claim": False,
            }
    finally:
        release(evo)

    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    all_ok = [v for v in results.values() if v.get("ok")]
    evidence = {
        "kind": "external_local_sft_score",
        "gate": str(GATE),
        "model": cfg["model_name"],
        "timestamp": ts,
        "sft_epochs": epochs,
        "sft_lr": lr,
        "benches": results,
        "all_pass_gate_bare": all(v.get("pass_gate_bare") for v in all_ok) if all_ok else False,
        "all_pass_gate_trained": all(v.get("pass_gate_trained") for v in all_ok) if all_ok else False,
        "honest_splits": all(v.get("honest_split") for v in all_ok) if all_ok else False,
        "upstream_claim": False,
        "notes": (
            "Honest train-only LoRA SFT on local toys then eval. "
            "Not upstream ServeLearnBench / EvoArena / PATH-Bench. "
            "Does not reopen burned packs. Does not unlock Epoch D."
        ),
    }
    out = repo_path("docs") / "EXTERNAL_LOCAL_SFT_SCORE_2026-10-18.json"
    out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    run_out = repo_path("runs") / "external_local_sft_score.json"
    run_out.parent.mkdir(parents=True, exist_ok=True)
    run_out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    summary = {
        "docs": str(out),
        "honest_splits": evidence["honest_splits"],
        "all_pass_gate_trained": evidence["all_pass_gate_trained"],
        "rates_bare": {k: v.get("bare", {}).get("rate") for k, v in results.items()},
        "rates_trained": {k: v.get("trained", {}).get("rate") for k, v in results.items()},
        "gains": {k: v.get("gain") for k, v in results.items()},
    }
    print(json.dumps(summary, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
