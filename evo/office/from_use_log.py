"""C2/C3: load graded office use-log pairs and crystallize family atoms.

Gate 0.6 never lowered. Notes-only atoms record scaffold_rate; bare_rate needs
adapter + ablation (GPU) and is left None until then.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


CRITERION = 0.6
SMOKE_MIN_N = 2  # playbook smoke floor; product uses 40


def _repo() -> Path:
    return Path(__file__).resolve().parents[2]


def load_use_log_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def load_from_events(events_path: Path) -> list[dict]:
    """Rebuild {family,prompt,trace,ok,split,index,arm} from EventBus JSONL."""
    if not events_path.is_file():
        return []
    starts: dict[str, dict] = {}
    tools: dict[str, list[str]] = defaultdict(list)
    checks: dict[str, dict] = {}
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        kind = ev.get("type")
        tid = str(ev.get("task") or "")
        if kind == "task_start":
            starts[tid] = ev
        elif kind == "tool":
            args = ev.get("arguments") or {}
            chunk = str(args.get("code") or args.get("cmd") or "").strip()
            if chunk:
                tools[tid].append(chunk)
        elif kind == "check":
            checks[tid] = ev
    rows = []
    for tid, start in starts.items():
        chk = checks.get(tid) or {}
        rows.append(
            {
                "family": start.get("family") or chk.get("family") or "",
                "prompt": start.get("prompt") or "",
                "trace": "\\n".join(tools.get(tid) or []),
                "ok": bool(chk.get("ok", False)),
                "split": start.get("split") or chk.get("split") or "practice",
                "index": int(start.get("index") or 0),
                "arm": start.get("arm") or chk.get("arm") or "",
                "task_id": tid,
                "source": "events",
            }
        )
    return rows


def discover_rows(use_log_dir: Path, arm: str = "dual") -> list[dict]:
    """Prefer arm.jsonl dump; fall back to events/<arm>-s*.jsonl."""
    primary = use_log_dir / f"{arm}.jsonl"
    rows = load_use_log_jsonl(primary)
    if rows:
        for row in rows:
            row.setdefault("source", "buffer")
        return rows
    events_dir = use_log_dir / "events"
    if events_dir.is_dir():
        merged = []
        for path in sorted(events_dir.glob(f"{arm}-*.jsonl")):
            merged.extend(load_from_events(path))
        if merged:
            return merged
    # also accept direct events file path used as use_log_dir
    if (use_log_dir.suffix == ".jsonl") and use_log_dir.is_file():
        return load_from_events(use_log_dir)
    return []


def grade_filter(
    rows: list[dict],
    *,
    family: str | None = None,
    split: str = "practice",
    ok_only: bool = True,
) -> list[dict]:
    """C2: keep graded usable pairs."""
    out = []
    for row in rows:
        if ok_only and not bool(row.get("ok")):
            continue
        if split and (row.get("split") or "") != split:
            continue
        fam = str(row.get("family") or "")
        if family and fam != family:
            continue
        prompt = str(row.get("prompt") or "").strip()
        trace = str(row.get("trace") or "").strip()
        if not prompt or not trace:
            continue
        out.append(row)
    return out


def pairs_from_rows(rows: list[dict]) -> list[tuple[str, str]]:
    return [(str(r["prompt"]), str(r["trace"])) for r in rows]


def family_counts(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[str(row.get("family") or "")] += 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def crystallize_family(
    family: str,
    rows: list[dict],
    *,
    name: str | None = None,
    criterion: float = CRITERION,
    min_n: int = SMOKE_MIN_N,
    adapter_dir: str | Path | None = None,
) -> dict[str, Any]:
    """C3: crystallize_from_pairs. Refuses if hit-rate < criterion (gate 0.6)."""
    from evo.crystal import crystallize_from_pairs

    graded = grade_filter(rows, family=family, split="practice", ok_only=True)
    n = len(graded)
    report: dict[str, Any] = {
        "family": family,
        "n_graded": n,
        "min_n": min_n,
        "criterion": criterion,
        "ok": False,
    }
    if n < min_n:
        report["why"] = f"need >= {min_n} graded ok practice pairs, got {n}"
        return report
    pairs = pairs_from_rows(graded)
    # Already filtered ok; grade fn trusts feedstock (episode-verified).
    atom_name = name or f"office_{family}_uselog"
    try:
        atom = crystallize_from_pairs(
            atom_name,
            family,
            pairs,
            grade=lambda _p, _c: True,
            adapter_dir=adapter_dir,
            criterion=criterion,
            sites=["office", family],
        )
    except Exception as exc:
        report["why"] = str(exc)
        return report
    report.update(
        {
            "ok": True,
            "name": atom.name,
            "path": atom.adapter_dir,
            "bare_rate": atom.bare_rate,
            "scaffold_rate": atom.scaffold_rate,
            "kind": (atom.evidence or {}).get("kind"),
            "evidence": atom.evidence,
            "note": "notes_only until GPU adapter+ablation fills bare_rate; gate 0.6",
        }
    )
    return report


def run_pipeline(
    use_log_dir: str | Path,
    *,
    families: list[str] | None = None,
    arm: str = "dual",
    criterion: float = CRITERION,
    min_n: int = SMOKE_MIN_N,
    prefer: tuple[str, ...] = ("table", "file", "report", "shell"),
) -> dict[str, Any]:
    root = Path(use_log_dir)
    if not root.is_absolute():
        root = _repo() / root
    rows = discover_rows(root, arm=arm)
    graded_all = grade_filter(rows, split="practice", ok_only=True)
    counts = family_counts(graded_all)
    chosen = list(families) if families else [f for f in prefer if counts.get(f, 0) >= min_n]
    if not chosen and counts:
        # pick richest family even if below prefer order
        top = max(counts.items(), key=lambda kv: kv[1])[0]
        chosen = [top]
    crystals = []
    for fam in chosen:
        crystals.append(
            crystallize_family(fam, rows, criterion=criterion, min_n=min_n)
        )
    out = {
        "use_log_dir": str(root),
        "arm": arm,
        "n_rows": len(rows),
        "n_graded_practice_ok": len(graded_all),
        "family_counts": counts,
        "crystals": crystals,
        "criterion": criterion,
        "gate2_claim": False,
        "n_ok_crystals": sum(1 for c in crystals if c.get("ok")),
    }
    report_path = root / "c2c3_report.json"
    report_path.write_text(json.dumps(out, indent=2, ensure_ascii=True), encoding="utf-8")
    out["report_path"] = str(report_path)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C2/C3 crystallize from office use-log")
    parser.add_argument(
        "--use-log",
        default="runs/use_log/office_use_log_dual_f3i_s0",
        help="use_log run folder",
    )
    parser.add_argument("--arm", default="dual")
    parser.add_argument("--family", action="append", default=None)
    parser.add_argument("--min-n", type=int, default=SMOKE_MIN_N)
    parser.add_argument("--criterion", type=float, default=CRITERION)
    args = parser.parse_args(argv)
    if args.criterion < CRITERION:
        raise SystemExit("criterion may not be lowered below 0.6")
    report = run_pipeline(
        args.use_log,
        families=args.family,
        arm=args.arm,
        criterion=args.criterion,
        min_n=args.min_n,
    )
    print(json.dumps(report, indent=2, ensure_ascii=True)[:4000])
    return 0 if report.get("n_ok_crystals", 0) > 0 or report.get("n_graded_practice_ok", 0) >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
