# -*- coding: utf-8 -*-
"""C96: Dissolve dashboard refresh after C91-C95 (honest, no gate mint)."""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.dissolve_dashboard import build as build_dissolve

DOC = ROOT / "docs" / "r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    dash = build_dissolve()
    # attach recent cycle pointers
    recent = {}
    for name in ("C91_E2E_MULTIHOP", "C92_LIVE_U2C_GROWTH", "C93_REPLACE_STRESS", "C94_DESKTOP_CAPTURE", "C95_GEN11_HOLD"):
        p = DOC / f"{name}.json"
        if p.is_file():
            d = json.loads(p.read_text(encoding="utf-8"))
            recent[name] = {k: d.get(k) for k in ("pass", "ocr_rate", "atom_rate", "crystal_rate", "bare_rate", "replace_rate", "capture_ok", "decision", "dissolve_D") if k in d or k in ("pass",)}
            recent[name]["pass"] = d.get("pass")
    families = dash.get("families") or dash.get("by_family") or dash
    out = {
        "cycle": "C96",
        "theme": "dissolve_refresh",
        "gate": GATE,
        "dashboard": dash,
        "recent_cycles": recent,
        "pass": True,
        "timestamp": ts(),
        "note": "Refresh only; Gate2/3 untouched.",
    }
    J(DOC / "C96_DISSOLVE_REFRESH.json", out)
    J(ROOT / "docs" / "DISSOLVE_DASHBOARD_C96_2026-10-19.json", dash if isinstance(dash, dict) else {"raw": dash})
    print(json.dumps({"cycle": "C96", "pass": True, "keys": list(recent.keys())}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
