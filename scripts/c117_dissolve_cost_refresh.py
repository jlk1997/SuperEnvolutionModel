# -*- coding: utf-8 -*-
"""C117: Refresh dissolve + cost dashboards after C113-C116."""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.dissolve_dashboard import build as build_dissolve

DOC = ROOT / "docs/r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def summarize(name):
    p = DOC / f"{name}.json"
    if not p.is_file():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    keys = (
        "pass", "claim", "rate", "trained", "bare", "delta_trained_minus_bare",
        "rate_gate_pass", "ocr_rate", "atom_rate", "test_rate", "n_fixtures",
        "vl_gate_v5_claim", "decision", "replace_rate", "ratio",
    )
    out = {k: d.get(k) for k in keys if k in d}
    if "trained" in d and isinstance(d["trained"], dict):
        out["trained_rate"] = d["trained"].get("rate")
    if "bare" in d and isinstance(d["bare"], dict):
        out["bare_rate"] = d["bare"].get("rate")
    if "tests" in d and isinstance(d["tests"], dict):
        out["test_rate"] = d["tests"].get("rate")
    if "smoke" in d and isinstance(d["smoke"], dict):
        out["smoke_rate"] = d["smoke"].get("rate")
    out["pass"] = d.get("pass")
    out["claim"] = d.get("claim")
    return out


def main():
    dash = build_dissolve()
    # compact family view
    families = {}
    rows = dash.get("families") or dash.get("rows") or []
    if isinstance(rows, list):
        for r in rows:
            fam = r.get("family")
            if fam:
                families[fam] = {"bare": r.get("bare_rate"), "D": r.get("dissolution"), "internalized": r.get("internalized")}
    elif isinstance(rows, dict):
        families = rows
    recent = {}
    for name in (
        "C113_U2C_GROW_PAIRS", "C114_U2C_ABSORB_PUSH", "C115_HARDEN_ANT_CAPTURE",
        "C116_V5_DESIGN_BATCH", "C110_REPLACE_HARDER_COST", "C107_VISION_V4_HELDOUT",
    ):
        s = summarize(name)
        if s is not None:
            recent[name] = s
    cost = None
    cp = DOC / "COST_LEDGER_BARE_VS_AGENT_C110.json"
    if cp.is_file():
        cost = json.loads(cp.read_text(encoding="utf-8"))
    # attach V4/V5 pointers
    vision = {
        "v4_heldout": summarize("C107_VISION_V4_HELDOUT"),
        "v5_design": summarize("C116_V5_DESIGN_BATCH"),
    }
    out = {
        "cycle": "C117",
        "theme": "dissolve_cost_refresh",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "families": families,
        "dashboard_full": dash,
        "recent_cycles": recent,
        "cost_c110": cost,
        "vision": vision,
        "pass": True,
        "claim": False,
        "note": "Dashboard refresh only. No Gate2/3 mint. No gen11 open.",
    }
    J(DOC / "C117_DISSOLVE_COST_REFRESH.json", out)
    J(ROOT / "docs" / f"DISSOLVE_DASHBOARD_C117_{datetime.now().strftime('%Y-%m-%d')}.json", {
        "cycle": "C117",
        "families": families,
        "vision": vision,
        "timestamp": ts(),
        "note": "Pointer refresh after C113-C116.",
    })
    print(json.dumps({"cycle": "C117", "pass": True, "families": list(families.keys()), "recent": list(recent.keys())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
