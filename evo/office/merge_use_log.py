"""Merge multiple office use_log runs into one graded XML corpus for C4.

Does not lower criterion 0.6. Exam ladder stays frozen.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from evo.office.use_log_xml import pairs_from_events, write_xml_use_log


def _repo() -> Path:
    return Path(__file__).resolve().parents[2]


def merge_xml_corpus(
    sources: list[str | Path],
    dest: str | Path,
    *,
    arm: str = "dual",
) -> dict[str, Any]:
    """Rebuild XML from each source events (or dual_xml.jsonl) and write merged dest."""
    dest_root = Path(dest)
    if not dest_root.is_absolute():
        dest_root = _repo() / dest_root
    dest_root.mkdir(parents=True, exist_ok=True)
    merged: list[dict] = []
    per_src = []
    for raw in sources:
        root = Path(raw)
        if not root.is_absolute():
            root = _repo() / root
        if not root.exists():
            per_src.append({"source": str(root), "ok": False, "why": "missing"})
            continue
        # prefer fresh events rebuild
        events_dir = root / "events"
        rows: list[dict] = []
        if events_dir.is_dir():
            for path in sorted(events_dir.glob(f"{arm}-*.jsonl")):
                rows.extend(pairs_from_events(path, ok_only=False))
            write_xml_use_log(root, arm=arm, seed=0)
        xml_path = root / f"{arm}_xml.jsonl"
        if xml_path.is_file() and not rows:
            for line in xml_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
        # tag source
        for row in rows:
            row = dict(row)
            row["source_run"] = root.name
            merged.append(row)
        ok_p = [r for r in rows if r.get("ok") and r.get("split") == "practice"]
        fam: dict[str, int] = defaultdict(int)
        for r in ok_p:
            fam[str(r.get("family") or "")] += 1
        per_src.append(
            {
                "source": str(root),
                "ok": True,
                "n_rows": len(rows),
                "n_ok_practice": len(ok_p),
                "family_counts": dict(fam),
            }
        )
    # de-dupe by run+task identity (same seed plans share prompts across runs —
    # keep both so n grows; still drop exact duplicate task_id within a run).
    best: dict[tuple, dict] = {}
    for row in merged:
        key = (
            row.get("source_run"),
            row.get("task_id") or row.get("index"),
            row.get("family"),
            row.get("split"),
        )
        prev = best.get(key)
        if prev is None or (row.get("ok") and not prev.get("ok")):
            best[key] = row
    uniq = list(best.values())
    out = dest_root / f"{arm}_xml.jsonl"
    with out.open("w", encoding="utf-8") as handle:
        for row in uniq:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    ok_practice = [r for r in uniq if r.get("ok") and r.get("split") == "practice"]
    fam_all: dict[str, int] = defaultdict(int)
    for r in ok_practice:
        fam_all[str(r.get("family") or "")] += 1
    # also write a fake events-less layout dissolve can load via dual_xml.jsonl
    meta = {
        "dest": str(dest_root),
        "arm": arm,
        "sources": per_src,
        "n_merged_rows": len(uniq),
        "n_ok_practice": len(ok_practice),
        "family_counts_ok_practice": dict(sorted(fam_all.items())),
        "out": str(out),
        "criterion": 0.6,
        "note": "merged XML corpus for C4 dissolve; exam ladder frozen",
    }
    (dest_root / f"{arm}_xml_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    # stub events empty dir so write_xml_use_log paths resolve
    (dest_root / "events").mkdir(exist_ok=True)
    return meta
