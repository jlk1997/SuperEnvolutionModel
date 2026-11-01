# -*- coding: utf-8 -*-
"""C145: Wire confidence-gated money into main capture path + regression.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import parse_paid, run_pipeline, CONFIDENCE_GATE, MONEY_TOOL
from evo.office.money_tool import confidence_gated_money

GATE = 0.6
DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/c145_confidence_gate_capture"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASES = [
    {
        "id": "disagree_use_tool",
        "text": "latte paid 4.50 sandwich paid 12.00 juice open 3.00 TOTAL PAID TARGET 16.50",
        "model_guess": 19.5,
        "expect": 16.5,
        "expect_agree": False,
    },
    {
        "id": "agree_high",
        "text": "A paid 10.00 B paid 5.00 TOTAL PAID TARGET 15.00",
        "model_guess": 15.0,
        "expect": 15.0,
        "expect_agree": True,
    },
    {
        "id": "noise_999",
        "text": "WIN-B old total 999.00 item paid 5.00 paid 6.00 TOTAL PAID TARGET 11.00",
        "model_guess": 999.0,
        "expect": 11.0,
        "expect_agree": False,
    },
    {
        "id": "open_zero",
        "text": "OPEN ONLY X 9.00 open Y 11.00 open paid_total TARGET 0.00",
        "model_guess": 20.0,
        "expect": 0.0,
        "expect_agree": False,
    },
    {
        "id": "auto_guess",
        "text": "alpha paid 3.25 beta paid 7.75 open 1 TOTAL PAID TARGET 11.00",
        "model_guess": None,
        "expect": 11.0,
        "expect_agree": True,
    },
    {
        "id": "pipeline_offline",
        "pipeline": True,
        "lines": ["CAPTURE GATE", "item A paid 8.00", "item B paid 4.50", "item C open 2.00", "TOTAL PAID TARGET 12.50"],
        "expected_paid": 12.50,
    },
]


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    rows = []
    n_ok = 0
    for c in CASES:
        if c.get("pipeline"):
            outdir = RUN / "pipeline_offline"
            ev = run_pipeline(outdir, c["lines"], c["expected_paid"], use_vl=False, title="C145 GATE")
            ok = bool(ev.get("pass") and ev.get("confidence_gated") and abs(float(ev.get("paid_got", -1)) - c["expected_paid"]) < 0.08)
            rows.append({"id": c["id"], "ok": ok, "evidence_keys": sorted(ev.keys()), "paid_got": ev.get("paid_got"), "confidence_gate": ev.get("confidence_gate")})
            n_ok += int(ok)
            continue
        val, meta = parse_paid(c["text"], model_guess=c["model_guess"], return_meta=True)
        ok = abs(val - c["expect"]) < 0.08 and meta.get("source") == "money_tool" and meta.get("agree") == c["expect_agree"]
        rows.append({"id": c["id"], "ok": ok, "value": val, "meta": meta})
        n_ok += int(ok)

    n = len(rows)
    rate = n_ok / n if n else 0.0
    wired = bool(CONFIDENCE_GATE and MONEY_TOOL)
    out = {
        "cycle": "C145",
        "theme": "confidence_gate_wired_into_capture_main_path",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "wired": wired,
        "module": "scripts/ant_capture_office_lib.py",
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "rows": rows,
        "pass": wired and rate >= GATE,
        "claim": False,
        "innovation": True,
        "note": "Main capture path now uses confidence_gated_money; disagree->tool.",
    }
    J(DOC / "C145_CONFIDENCE_GATE_CAPTURE_WIRE.json", out)
    J(RUN / "judge.json", out)
    # short product note
    md = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"
    md.write_text(
        f"# 蚁算 confidence-gated capture\n\nUpdated: {ts()} (Asia/Shanghai)\n\n"
        f"- Wired: `{wired}`\n- Regression rate: `{rate}`\n"
        f"- Policy: disagree → money_tool; agree → still prefer tool\n"
        f"- Evidence: docs/r50/C145_CONFIDENCE_GATE_CAPTURE_WIRE.json\n"
        f"- Gate2/3 untouched. gen11 HOLD.\n",
        encoding="utf-8",
    )
    print(json.dumps({"cycle": "C145", "wired": wired, "rate": round(rate, 4), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())