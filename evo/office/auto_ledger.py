"""Promote task families from audited assist successes into auto_families.

ARCHITECTURE: auto only opens families already verified. This ledger counts
applied, non-refused tool rows per family in audit.jsonl (or an explicit
promote.json). Shadow proposals (applied=false) do not promote; assist/auto
applies do. Gate 0.6 — CPU path; no model actor required.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


DEFAULT_MIN_N = 1
LEDGER_NAME = "promote.json"


def load_ledger(path: Path) -> dict:
    if not path.is_file():
        return {"families": {}, "min_n": DEFAULT_MIN_N}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("families", {})
    data.setdefault("min_n", DEFAULT_MIN_N)
    return data


def save_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def record_success(path: Path, family: str, n: int = 1) -> dict:
    """Explicit assist accept: bump family success count."""
    if not family:
        raise ValueError("family required")
    data = load_ledger(path)
    fam = data["families"].setdefault(family, {"successes": 0})
    fam["successes"] = int(fam.get("successes", 0)) + int(n)
    save_ledger(path, data)
    return data


def count_applied_by_family(audit_path: Path) -> Counter:
    """Count applied tool rows (non-finish) per family from audit.jsonl."""
    counts: Counter = Counter()
    if not audit_path.is_file():
        return counts
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if not row.get("applied"):
            continue
        if row.get("name") in (None, "", "finish"):
            continue
        if row.get("refused"):
            continue
        family = row.get("family")
        if family:
            counts[family] += 1
    return counts


def eligible_families(
    *,
    ledger_path: Path | None = None,
    audit_path: Path | None = None,
    min_n: int | None = None,
) -> set[str]:
    """Union of ledger successes and audit applied counts meeting min_n."""
    threshold = DEFAULT_MIN_N if min_n is None else int(min_n)
    totals: Counter = Counter()
    if ledger_path is not None:
        data = load_ledger(ledger_path)
        if min_n is None:
            threshold = int(data.get("min_n", DEFAULT_MIN_N))
        for name, meta in (data.get("families") or {}).items():
            totals[name] += int(meta.get("successes", 0))
    if audit_path is not None:
        totals.update(count_applied_by_family(audit_path))
    return {name for name, n in totals.items() if n >= threshold}


def license_auto_families(eligible: set[str]) -> set[str]:
    """Copy for License(auto_families=...)."""
    return set(eligible)
