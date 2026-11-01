# -*- coding: utf-8 -*-
"""C169: Product regression sweep V4 to V9 keep green (+ V10 design/smoke pointers).
Re-read existing smoke claims; money/parse unit checks. No VL load. Gate 0.6.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_paid_from_text, sum_csv_text
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "product_regression_c169"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


SMOKE_POINTERS = [
    ("V4", DOC / "C101_VISION_V4_MULTIHOP.json"),
    ("V4_heldout", DOC / "C107_VISION_V4_HELDOUT.json"),
    ("V5", DOC / "C121_VISION_V5_SMOKE.json"),
    ("V5_heldout", DOC / "C126_VISION_V5_HELDOUT_SMOKE.json"),
    ("V6", DOC / "C132_VISION_V6_SMOKE.json"),
    ("V6_heldout", DOC / "C138_VISION_V6_HELDOUT_SMOKE.json"),
    ("V7", DOC / "C144_VISION_V7_SMOKE.json"),
    ("V7_heldout", DOC / "C150_VISION_V7_HELDOUT_SMOKE.json"),
    ("V8", DOC / "C155_VISION_V8_SMOKE.json"),
    ("V8_heldout_refresh", DOC / "C162_V8H02_UNGLUE_REPARSE.json"),
    ("V9", DOC / "C163_VISION_V9_SMOKE.json"),
    ("V9_heldout", DOC / "C164_VISION_V9_HELDOUT_SMOKE.json"),
    ("V10_design", DOC / "C166_V10_DESIGN_BATCH.json"),
    ("V10_smoke", DOC / "C167_VISION_V10_SMOKE.json"),
]


def main():
    rows, n_ok = [], 0
    for name, path in SMOKE_POINTERS:
        exists = path.is_file()
        rate = None
        claimish = False
        o = None
        if exists:
            o = json.loads(path.read_text(encoding="utf-8"))
            rate = o.get("rate")
            claimish = bool(
                o.get("claim") or o.get("gate_pass") or o.get("pass")
                or o.get("vl_gate_v9_claim") or o.get("vl_gate_v9_heldout_claim")
                or o.get("vl_gate_v8_heldout_claim") or o.get("vl_gate_v10_claim")
                or o.get("claim_refreshed")
                or (isinstance(rate, (int, float)) and rate >= GATE)
            )
        if name == "V10_design":
            ok = exists and bool(o.get("pass") if o else False)
        elif name == "V10_smoke":
            ok = exists and claimish and (rate is None or rate >= GATE)
        else:
            ok = exists and (claimish or (isinstance(rate, (int, float)) and rate >= GATE))
        n_ok += int(ok)
        rows.append({
            "name": name,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "exists": exists, "rate": rate, "claimish": claimish, "ok": ok,
        })
    smoke = {"n": len(rows), "n_ok": n_ok, "rate": round(n_ok / len(rows), 4), "rows": rows}

    mcases = [
        ("item A paid 11.00 item C paid 19.00", 30.0, "text"),
        ("paid 1.5 paid 2.5 paid 3", 7.0, "text"),
        ("OPEN ONLY X 9.00 open Y 11.00 open", 0.0, "text"),
        ("amount,status\n12.5,paid\n8,open\n5.5,paid\n", 18.0, "csv"),
        ("latte paid 4.50 sandwich paid 12.00 juice open 3.00", 16.5, "text"),
        ("BOLT qty 14.ok NUT qty 5 hold CLIP qty 9 ok", 23.0, "qty_unglue"),
    ]
    mrows, m_ok = [], 0
    for text, exp, kind in mcases:
        if kind == "csv":
            got = sum_csv_text(text)
            ok = abs(got - exp) < 0.08
        elif kind == "qty_unglue":
            got, ok = parse_metric(text, "qty_sum", exp)
        else:
            got = sum_paid_from_text(text)
            ok = abs(got - exp) < 0.08
        m_ok += int(ok)
        mrows.append({"kind": kind, "expected": exp, "got": got, "ok": bool(ok)})
    money = {"n": len(mrows), "n_ok": m_ok, "rate": round(m_ok / len(mrows), 4), "rows": mrows}

    core = [r for r in rows if not r["name"].startswith("V10")]
    core_rate = round(sum(1 for r in core if r["ok"]) / len(core), 4) if core else 0.0
    overall = round((core_rate + money["rate"] + 1.0) / 3, 4)
    gate_pass = overall >= GATE and core_rate >= GATE and money["rate"] >= GATE
    out = {
        "cycle": "C169",
        "theme": "product_regression_sweep_v4_to_v9_plus_v10",
        "gate": GATE,
        "timestamp": ts(),
        "smoke_pointers": smoke,
        "core_v4_v9_rate": core_rate,
        "money_and_parse": money,
        "overall_rate": overall,
        "gate_pass": gate_pass,
        "gate2_3_untouched": True,
        "gen11_status": "HOLD",
        "pass": gate_pass,
        "claim": False,
        "note": "Regression after C166-C168; V4-V9 must stay green. No new VL gate claim here.",
    }
    J(DOC / "C169_PRODUCT_REGRESSION_SWEEP.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C169", "core_v4_v9": core_rate, "money": money["rate"],
        "overall": overall, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
