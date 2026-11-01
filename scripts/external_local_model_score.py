"""Score wired external local toys on 1.5B (GPU). Not upstream leaderboards."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from evo.generate import first_line, generate, qa_prompt
from evo.model import build_model, release
from evo.office.external_scaffold import ADAPTERS
from evo.util import load_config, repo_path, set_seed


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
    # letter answers A/B
    if len(gold) == 1 and gold.upper() in "ABCD":
        m2 = re.search(r"\b([ABCD])\b", pred.upper())
        if m2 and m2.group(1) == gold.upper():
            return 1.0
    return 0.0


def main() -> None:
    benches = ["serve_learn", "evo_arena", "path_bench"]
    cfg = load_config(repo_path("configs/office_gate2_mid_n_dual.yaml"))
    cfg["model_name"] = str(repo_path("models/Qwen2.5-1.5B-Instruct"))
    set_seed(int(cfg.get("seed", 0)))
    evo = None
    results = {}
    try:
        evo = build_model(cfg)
        for bid in benches:
            adapter = ADAPTERS[bid]()
            loaded = adapter.load_local()
            if not loaded.get("ok"):
                results[bid] = {"ok": False, "load": loaded}
                continue
            eval_items = list(adapter.iter_items("eval"))
            rows = []
            for item in eval_items:
                pred = first_line(generate(evo, qa_prompt(item["task"]), 48, 0.0, None))
                gold = str(item.get("gold", ""))
                em = _em(pred, gold)
                rows.append({"id": item["id"], "task": item["task"], "gold": gold, "pred": pred, "em": em})
            n = len(rows)
            rate = (sum(r["em"] for r in rows) / n) if n else 0.0
            results[bid] = {
                "ok": True,
                "bench_id": bid,
                "local_path": loaded.get("path"),
                "n_eval": n,
                "rate": rate,
                "pass_gate": rate >= 0.6,
                "upstream_claim": False,
                "rows": rows,
            }
    finally:
        release(evo)

    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    evidence = {
        "kind": "external_local_model_score",
        "gate": "0.6",
        "model": cfg["model_name"],
        "timestamp": ts,
        "benches": results,
        "all_pass_gate": all(v.get("pass_gate") for v in results.values() if v.get("ok")),
        "upstream_claim": False,
        "notes": (
            "Bare 1.5B scores on serve_learn/evo_arena/path_bench local toys. "
            "Not upstream ServeLearnBench / EvoArena / PATH-Bench."
        ),
    }
    out = repo_path("docs") / "EXTERNAL_LOCAL_MODEL_SCORE_2026-10-18.json"
    out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    run_out = repo_path("runs") / "external_local_model_score.json"
    run_out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    summary = {
        "docs": str(out),
        "all_pass_gate": evidence["all_pass_gate"],
        "rates": {k: v.get("rate") for k, v in results.items()},
        "n": {k: v.get("n_eval") for k, v in results.items()},
    }
    print(json.dumps(summary, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
