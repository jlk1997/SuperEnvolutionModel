# -*- coding: utf-8 -*-
"""C127: Wire money_tool into capture→office E2E with evidence. Gate 0.6. No Gate2/3."""
from __future__ import annotations
import json, sys, shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import run_pipeline, MONEY_TOOL, parse_paid
from evo.office.money_tool import sum_paid_from_text, sum_csv_text

DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/money_tool_capture_c127"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)

    unit = []
    cases = [
        ("item A paid 11.00 item C paid 19.00", 30.0),
        ("paid 1.5 paid 2.5 paid 3", 7.0),
        ("OPEN ONLY X 9.00 open Y 11.00 open paid_total TARGET 0.00", 0.0),
        ("amount,status\n12.5,paid\n8,open\n5.5,paid\n", 18.0),
    ]
    n_unit_ok = 0
    for text, exp in cases:
        if "amount,status" in text:
            got_tool = sum_csv_text(text)
        else:
            got_tool = sum_paid_from_text(text)
        got_parse = parse_paid(text) if "amount,status" not in text else got_tool
        ok = abs(got_tool - exp) < 0.08 and (abs(got_parse - exp) < 0.08 or "amount,status" in text)
        n_unit_ok += int(ok)
        unit.append({"text": text[:50], "exp": exp, "tool": got_tool, "parse": got_parse, "ok": ok})

    # E2E capture path without VL (dry) — proves money_tool field on evidence
    e2e_cases = [
        {
            "name": "invoice_paid",
            "lines": [
                "INVOICE #C127-01",
                "item A paid 11.00",
                "item B open 3.00",
                "item C paid 19.00",
                "TOTAL PAID TARGET 30.00",
            ],
            "expected": 30.0,
        },
        {
            "name": "open_only_zero",
            "lines": [
                "OPEN ONLY",
                "X 9.00 open",
                "Y 11.00 open",
                "paid_total TARGET 0.00",
            ],
            "expected": 0.0,
        },
        {
            "name": "triple_paid",
            "lines": [
                "PO-C127",
                "line1 paid 4.00",
                "line2 paid 6.00",
                "line3 paid 5.50",
                "TOTAL PAID TARGET 15.50",
            ],
            "expected": 15.50,
        },
    ]
    e2e_rows = []
    n_e2e_ok = 0
    for c in e2e_cases:
        outdir = RUN / c["name"]
        ev = run_pipeline(outdir, c["lines"], c["expected"], use_vl=False, title=f"C127 {c['name']}")
        ok = bool(ev.get("ok")) and bool(ev.get("money_tool")) and abs(float(ev.get("paid_got", -1)) - c["expected"]) < 0.08
        n_e2e_ok += int(ok)
        e2e_rows.append({
            "name": c["name"],
            "ok": ok,
            "paid_got": ev.get("paid_got"),
            "paid_expected": c["expected"],
            "money_tool": ev.get("money_tool"),
            "money_policy": ev.get("money_policy"),
            "errors": ev.get("errors"),
        })

    unit_rate = n_unit_ok / len(unit) if unit else 0.0
    e2e_rate = n_e2e_ok / len(e2e_rows) if e2e_rows else 0.0
    rate = min(unit_rate, e2e_rate)
    out = {
        "cycle": "C127",
        "theme": "money_tool_wired_into_capture_office_e2e",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "money_tool_imported": bool(MONEY_TOOL),
        "unit": {"n": len(unit), "n_ok": n_unit_ok, "rate": round(unit_rate, 4), "rows": unit},
        "e2e_capture_dry": {"n": len(e2e_rows), "n_ok": n_e2e_ok, "rate": round(e2e_rate, 4), "rows": e2e_rows},
        "rate": round(rate, 4),
        "pass": rate >= GATE and bool(MONEY_TOOL),
        "claim": False,
        "note": "Product path: capture→parse_paid uses evo.office.money_tool. Evidence fields money_tool/money_policy.",
    }
    J(DOC / "C127_MONEY_TOOL_CAPTURE_E2E.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C127", "rate": round(rate, 4), "pass": out["pass"], "money_tool": bool(MONEY_TOOL)}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
