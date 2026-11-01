"""Persist graded office traces for Epoch C crystallizer intake (F3i / C1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def use_log_dir(cfg: dict, seed: int | None = None) -> Path:
    """runs/use_log/<run_name>[_sN] — one folder per seeded run."""
    name = str(cfg.get("run_name") or "office")
    if seed is not None:
        name = f"{name}_s{seed}"
    root = Path(cfg.get("use_log_root") or "runs/use_log")
    if not root.is_absolute():
        # Prefer repo root (parent of evo/) when cwd is elsewhere.
        here = Path(__file__).resolve().parents[2]
        root = here / root
    return root / name


def dump_arm_use_log(
    session: Any,
    cfg: dict,
    *,
    arm: str,
    seed: int,
) -> Path | None:
    """Write JSONL rows {family,prompt,trace,ok,split,...} from practice buffer + day_pairs.

    Buffer refuses exam (EpisodicBuffer.add); feedstock is practice dual writes.
    Returns path written, or None if skipped/empty.
    """
    if not _enabled(cfg, arm):
        return None
    rows = list(getattr(getattr(session, "buffer", None), "rows", None) or [])
    day_pairs = list(getattr(session, "day_pairs", []) or [])
    if not rows and not day_pairs:
        return None
    out_dir = use_log_dir(cfg, seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{arm}.jsonl"
    n = 0
    n_ok = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            tools = list(getattr(row, "tools", None) or [])
            family = tools[0] if tools else ""
            ok = bool(getattr(row, "ok", False))
            rec = {
                "family": family,
                "prompt": getattr(row, "prompt", "") or "",
                "trace": getattr(row, "code", "") or "",
                "ok": ok,
                "split": getattr(row, "split", "") or "practice",
                "index": int(getattr(row, "tick", 0) or 0),
                "arm": arm,
                "seed": int(seed),
            }
            handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
            if ok:
                n_ok += 1
    pairs_path = out_dir / f"{arm}_day_pairs.jsonl"
    with pairs_path.open("w", encoding="utf-8") as handle:
        for prompt, trace in day_pairs:
            handle.write(
                json.dumps(
                    {
                        "family": "",
                        "prompt": prompt,
                        "trace": trace,
                        "ok": True,
                        "split": "practice",
                        "arm": arm,
                        "seed": int(seed),
                        "source": "day_pairs",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    meta = {
        "arm": arm,
        "seed": int(seed),
        "n_rows": n,
        "n_ok": n_ok,
        "n_day_pairs": len(day_pairs),
        "practice_ok": list(getattr(session, "practice_flags", []) or []),
        "writes": len(getattr(session, "writes", []) or []),
        "run_name": cfg.get("run_name"),
        "criterion": 0.6,
        "note": "F3i/C1 use-log capture; gate 0.6 never lowered; exam refused by buffer",
    }
    (out_dir / f"{arm}_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return path


def _enabled(cfg: dict, arm: str) -> bool:
    if cfg.get("use_log") is False:
        return False
    if cfg.get("use_log") is True:
        return True
    if bool(cfg.get("use_log_dual_only", True)):
        return arm in ("dual", "dual_agent")
    return True
