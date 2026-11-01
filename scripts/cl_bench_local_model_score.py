"""Score cl_bench local continual toy on 1.5B (GPU). Not upstream CL-Bench."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from evo.generate import first_line, generate, qa_prompt
from evo.model import build_model, release
from evo.office.external_scaffold import ClBenchLocalAdapter
from evo.util import load_config, repo_path, set_seed


def _norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^0-9a-z.\-]+", " ", s)
    return " ".join(s.split())


def main() -> None:
    cfg = load_config(repo_path("configs/office_gate2_mid_n_dual.yaml"))
    cfg["model_name"] = str(repo_path("models/Qwen2.5-1.5B-Instruct"))
    set_seed(int(cfg.get("seed", 0)))
    adapter = ClBenchLocalAdapter()
    loaded = adapter.load_local()
    if not loaded.get("ok"):
        raise SystemExit(f"load failed: {loaded}")
    eval_items = list(adapter.iter_items("eval"))
    evo = None
    rows = []
    try:
        evo = build_model(cfg)
        for item in eval_items:
            pred = first_line(generate(evo, qa_prompt(item["task"]), 32, 0.0, None))
            gold = str(item.get("gold", ""))
            em = 1.0 if _norm(pred) == _norm(gold) or gold in pred else 0.0
            # also accept leading number match
            if em < 1.0:
                m = re.search(r"-?\d+(?:\.\d+)?", pred)
                if m and _norm(m.group(0)) == _norm(gold):
                    em = 1.0
            rows.append({"id": item["id"], "task": item["task"], "gold": gold, "pred": pred, "em": em})
    finally:
        release(evo)
    n = len(rows)
    rate = (sum(r["em"] for r in rows) / n) if n else 0.0
    evidence = {
        "kind": "cl_bench_local_model_score",
        "gate": "0.6",
        "model": cfg["model_name"],
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "local_path": loaded.get("path"),
        "n_eval": n,
        "rate": rate,
        "pass_gate": rate >= 0.6,
        "upstream_claim": False,
        "rows": rows,
        "notes": "Bare 1.5B score on heldout_math continual toy eval split. Not CL-Bench leaderboard.",
    }
    out = repo_path("docs") / "CL_BENCH_LOCAL_MODEL_SCORE_2026-10-18.json"
    out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    run_out = repo_path("runs") / "cl_bench_local_model_score.json"
    run_out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": evidence["pass_gate"], "rate": rate, "n": n, "docs": str(out)}, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
