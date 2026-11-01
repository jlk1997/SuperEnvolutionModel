"""Rebuild use-log pairs as canonical XML tool_call traces for SFT/dissolve.

Root cause of C4 bare=0 (2026-10-17): dump_arm_use_log / trace_text stores raw
code/cmd strings, but office actor emits <tool_call><function=...> XML.
Training on naked traces cannot teach the eval format. Gate 0.6 unchanged.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _repo() -> Path:
    return Path(__file__).resolve().parents[2]


def format_tool_xml(name: str, arguments: dict) -> str:
    from evo.computer.actions import format_call
    from evo.computer.license import normalize_shell

    args = dict(arguments or {})
    if str(name or "") == "shell" and "cmd" in args:
        args["cmd"] = normalize_shell(str(args.get("cmd") or ""))
    return format_call(str(name or "finish"), args)


def pairs_from_events(
    events_path: Path,
    *,
    family: str | None = None,
    split: str = "practice",
    ok_only: bool = True,
) -> list[dict[str, Any]]:
    """One row per task: prompt + concatenated XML tool calls from EventBus."""
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
            name = str(ev.get("name") or "")
            args = dict(ev.get("arguments") or {})
            # skip empty / error-only / refused / not-applied rows — keep SFT clean
            if not name and not args:
                continue
            if ev.get("refused"):
                continue
            if ev.get("applied") is False:
                continue
            # shell family: ignore python fences the model emits after success
            fam = str((starts.get(tid) or {}).get("family") or "")
            if fam == "shell" and name == "python":
                continue
            if name:
                tools[tid].append(format_tool_xml(name, args))
        elif kind == "check":
            checks[tid] = ev
    rows: list[dict[str, Any]] = []
    for tid, start in starts.items():
        chk = checks.get(tid) or {}
        fam = str(start.get("family") or chk.get("family") or "")
        sp = str(start.get("split") or chk.get("split") or "practice")
        ok = bool(chk.get("ok", False))
        if family and fam != family:
            continue
        if split and sp != split:
            continue
        if ok_only and not ok:
            continue
        seq = tools.get(tid) or []
        # Drop consecutive duplicate tool_call blocks (e.g. cp then copy after alias).
        deduped: list[str] = []
        for block in seq:
            if deduped and deduped[-1] == block:
                continue
            deduped.append(block)
        xml = "\n".join(deduped).strip()
        prompt = str(start.get("prompt") or "").strip()
        if not prompt or not xml:
            continue
        rows.append(
            {
                "family": fam,
                "prompt": prompt,
                "trace": xml,
                "ok": ok,
                "split": sp,
                "index": int(start.get("index") or 0),
                "arm": start.get("arm") or "",
                "task_id": tid,
                "source": "events_xml",
                "n_calls": len(tools.get(tid) or []),
            }
        )
    return rows


def write_xml_use_log(
    use_log_dir: str | Path,
    *,
    arm: str = "dual",
    seed: int = 0,
) -> dict[str, Any]:
    """Write <arm>_xml.jsonl (+ meta) next to existing use_log dumps."""
    root = Path(use_log_dir)
    if not root.is_absolute():
        root = _repo() / root
    events = root / "events" / f"{arm}-s{seed}.jsonl"
    if not events.is_file():
        # glob fallback
        cand = sorted((root / "events").glob(f"{arm}-*.jsonl")) if (root / "events").is_dir() else []
        events = cand[0] if cand else events
    existing = root / f"{arm}_xml.jsonl"
    rows = pairs_from_events(events, ok_only=False)
    # Preserve pre-merged corpus when events are empty (merged_xml dirs).
    if not rows and existing.is_file():
        kept = [json.loads(l) for l in existing.read_text(encoding="utf-8").splitlines() if l.strip()]
        ok_practice = [r for r in kept if r.get("ok") and r.get("split") == "practice"]
        meta = {
            "arm": arm,
            "seed": seed,
            "events": str(events),
            "n_rows": len(kept),
            "n_ok_practice": len(ok_practice),
            "out": str(existing),
            "note": "preserved existing XML (no events to rebuild)",
            "criterion": 0.6,
        }
        (root / f"{arm}_xml_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return meta
    out = root / f"{arm}_xml.jsonl"
    with out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    ok_practice = [r for r in rows if r.get("ok") and r.get("split") == "practice"]
    by_fam: dict[str, int] = defaultdict(int)
    for r in ok_practice:
        by_fam[str(r["family"])] += 1
    meta = {
        "arm": arm,
        "seed": seed,
        "events": str(events),
        "n_rows": len(rows),
        "n_ok_practice": len(ok_practice),
        "family_counts_ok_practice": dict(sorted(by_fam.items())),
        "out": str(out),
        "note": "XML tool_call pairs for dissolve SFT; fixes C4 format mismatch",
        "criterion": 0.6,
    }
    (root / f"{arm}_xml_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def load_xml_pairs(
    use_log_dir: str | Path,
    family: str,
    *,
    arm: str = "dual",
    min_n: int = 2,
) -> list[tuple[str, str]]:
    root = Path(use_log_dir)
    if not root.is_absolute():
        root = _repo() / root
    path = root / f"{arm}_xml.jsonl"
    if not path.is_file():
        write_xml_use_log(root, arm=arm)
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("family") != family:
            continue
        if not row.get("ok") or row.get("split") != "practice":
            continue
        rows.append((str(row["prompt"]), str(row["trace"])))
    if len(rows) < min_n:
        raise ValueError(f"need >= {min_n} XML ok practice pairs for {family}, got {len(rows)}")
    return rows
