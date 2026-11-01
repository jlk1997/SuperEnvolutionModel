# -*- coding: utf-8 -*-
"""C139: Product demo regression suite — capture + money_tool + V4/V5/V6 smoke pointers.
No VL load required. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import run_pipeline, MONEY_TOOL, validate_evidence
from evo.office.money_tool import sum_paid_from_text, sum_csv_text

GATE = 0.6
DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/product_demo_regression_c139"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


SMOKE_POINTERS = [
    ("V4", DOC / "C101_VISION_V4_MULTIHOP.json", "docs/r50/C101_VISION_V4_MULTIHOP.json"),
    ("V4_heldout", DOC / "C107_VISION_V4_HELDOUT.json", "docs/r50/C107_VISION_V4_HELDOUT.json"),
    ("V5", DOC / "C121_VISION_V5_SMOKE.json", "docs/r50/C121_VISION_V5_SMOKE.json"),
    ("V5_heldout", DOC / "C126_VISION_V5_HELDOUT_SMOKE.json", "docs/r50/C126_VISION_V5_HELDOUT_SMOKE.json"),
    ("V6", DOC / "C132_VISION_V6_SMOKE.json", "docs/r50/C132_VISION_V6_SMOKE.json"),
    ("V6_claim", DOC / "C132b_VISION_GATE_V6_CLAIM.json", "docs/r50/C132b_VISION_GATE_V6_CLAIM.json"),
]


def check_smoke_pointers():
    rows = []
    n_ok = 0
    for name, path, rel in SMOKE_POINTERS:
        exists = path.is_file()
        claimish = False
        rate = None
        if exists:
            try:
                o = json.loads(path.read_text(encoding="utf-8"))
                rate = o.get("rate")
                claimish = bool(
                    o.get("claim")
                    or o.get("vl_gate_v4_claim")
                    or o.get("vl_gate_v5_claim")
                    or o.get("vl_gate_v6_claim")
                    or o.get("gate_pass")
                    or (isinstance(rate, (int, float)) and rate >= GATE)
                )
            except Exception as e:
                rows.append({"name": name, "path": rel, "exists": True, "ok": False, "error": str(e)})
                continue
        ok = exists and (claimish or rate is not None)
        n_ok += int(ok)
        rows.append({
            "name": name, "path": rel, "exists": exists,
            "rate": rate, "claimish": claimish, "ok": ok,
        })
    return {"n": len(rows), "n_ok": n_ok, "rate": round(n_ok / len(rows), 4) if rows else 0.0, "rows": rows}


def money_tool_cases():
    cases = [
        ("item A paid 11.00 item C paid 19.00", 30.0, "text"),
        ("paid 1.5 paid 2.5 paid 3", 7.0, "text"),
        ("OPEN ONLY X 9.00 open Y 11.00 open", 0.0, "text"),
        ("amount,status\n12.5,paid\n8,open\n5.5,paid\n", 18.0, "csv"),
        ("latte paid 4.50 sandwich paid 12.00 juice open 3.00", 16.5, "text"),
    ]
    rows = []
    n_ok = 0
    for text, exp, kind in cases:
        got = sum_csv_text(text) if kind == "csv" else sum_paid_from_text(text)
        ok = abs(got - exp) < 0.08
        n_ok += int(ok)
        rows.append({"kind": kind, "exp": exp, "got": got, "ok": ok, "text": text[:50]})
    return {"n": len(rows), "n_ok": n_ok, "rate": round(n_ok / len(rows), 4), "rows": rows}


def capture_oneshot():
    outdir = RUN / "capture_oneshot"
    lines = [
        "REGRESSION INVOICE #ANT-C139",
        "latte paid 4.50",
        "sandwich paid 12.00",
        "juice open 3.00",
        "TOTAL PAID TARGET 16.50",
    ]
    expected = 16.50
    ev = run_pipeline(outdir, lines, expected, use_vl=False, title="ANT REGRESSION C139")
    errs = validate_evidence(ev)
    ok = (
        bool(ev.get("ok"))
        and bool(MONEY_TOOL)
        and abs(float(ev.get("paid_got", -1)) - expected) < 0.08
        and not errs
    )
    return {
        "ok": ok,
        "money_tool": bool(MONEY_TOOL),
        "paid_got": ev.get("paid_got"),
        "paid_expected": expected,
        "schema_errors": errs,
        "evidence_keys": sorted(ev.keys()),
    }


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)

    ptr = check_smoke_pointers()
    money = money_tool_cases()
    cap = capture_oneshot()

    parts = [ptr["rate"] >= GATE, money["rate"] >= GATE, cap["ok"]]
    rate = sum(1 for p in parts if p) / len(parts)
    out = {
        "cycle": "C139",
        "theme": "product_demo_regression_capture_money_v4v5v6",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "smoke_pointers": ptr,
        "money_tool": money,
        "capture_oneshot": cap,
        "rate": round(rate, 4),
        "pass": rate >= GATE and all(parts),
        "claim": False,
        "note": "Regression suite: pointers + money_tool + capture dry. No new VL claim.",
    }
    J(DOC / "C139_PRODUCT_DEMO_REGRESSION.json", out)
    J(RUN / "judge.json", out)
    # refresh demo pointer doc snippet
    md = ROOT / "docs" / "蚁算_CAPTURE_OFFICE_DEMO.md"
    if md.is_file():
        extra = (
            f"\n\n## Regression C139 ({ts()})\n"
            f"- pass: **{out['pass']}** rate={out['rate']}\n"
            f"- evidence: `docs/r50/C139_PRODUCT_DEMO_REGRESSION.json`\n"
            f"- V4/V5/V6 smoke pointers checked: {ptr['n_ok']}/{ptr['n']}\n"
        )
        # append only once marker
        body = md.read_text(encoding="utf-8")
        marker = "## Regression C139"
        if marker not in body:
            md.write_text(body.rstrip() + extra, encoding="utf-8")
    print(json.dumps({
        "cycle": "C139", "pass": out["pass"], "rate": out["rate"],
        "pointers": f"{ptr['n_ok']}/{ptr['n']}", "money": money["rate"], "capture": cap["ok"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
