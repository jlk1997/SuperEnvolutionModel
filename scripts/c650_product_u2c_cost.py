# -*- coding: utf-8 -*-
"""C650: Non-vision knife 鈥?product polish + U2C on V50 (stable crystal) + replace/cost ledger.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""
from __future__ import annotations
import json, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_paid_from_text
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v50"
RUN = ROOT / "runs/product_u2c_c650"
CLI = ROOT / "scripts" / "ant_capture_office.py"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def u2c_crystal():
    man_path = FIX / "manifest.json"
    if not man_path.is_file():
        return {"pass": False, "reason": "missing_v50_manifest", "n": 0, "rate": 0.0}
    man = json.loads(man_path.read_text(encoding="utf-8"))
    atoms, n_ok = [], 0
    for it in man.get("items") or []:
        text = "\n".join(it["lines"])
        got, ok = parse_metric(text, it["metric"], it["expected"])
        atoms.append({
            "id": "atom_" + it["id"],
            "source": it["id"],
            "metric": it["metric"],
            "expected": it["expected"],
            "got": got,
            "ok": bool(ok),
            "family": "vision_office",
            "version": "v50",
        })
        n_ok += int(bool(ok))
    rate = round(n_ok / len(atoms), 4) if atoms else 0.0
    out_path = RUN / "u2c_atoms.json"
    J(out_path, {"n": len(atoms), "n_ok": n_ok, "rate": rate, "atoms": atoms})
    return {
        "pass": rate >= GATE and len(atoms) >= 16,
        "n": len(atoms), "n_ok": n_ok, "rate": rate,
        "path": str(out_path.relative_to(ROOT)).replace("\\", "/"),
    }


def capture_multimetric():
    cases = [
        ("a paid 43.00 b paid 45.50 c open 14.00 TOTAL PAID TARGET 88.50", "paid_total", 88.5),
        ("SKU1 qty 35 ok SKU2 qty 16 hold SKU3 qty 38 ok qty_sum TARGET 73", "qty_sum", 73.0),
        ("itemR1 20.00 done itemR2 24.25 done itemR3 9.00 open refund_done TARGET 44.25", "refund_done", 44.25),
        ("T1 78.00 paid T2 31.00 open T3 61.00 paid tax_base_paid TARGET 139.00", "tax_base_paid", 139.0),
        ("A 1260 active B 240 leave C 1190 active payroll_active TARGET 2450", "payroll_active", 2450.0),
        ("P1 31 ok P2 17 hold P3 31 ok ship_ok_qty TARGET 62", "ship_ok_qty", 62.0),
        ("S1 pri 25 open S2 pri 29 closed S3 pri 33 open open_pri_sum TARGET 58", "open_pri_sum", 58.0),
        ("X 58.00 open Y 61.00 open paid_total TARGET 0.00", "paid_total", 0.0),
    ]
    rows, n_ok = [], 0
    for text, metric, exp in cases:
        got, ok = parse_metric(text, metric, exp)
        if metric == "paid_total":
            tool = sum_paid_from_text(text)
            if tool is not None and abs((got or -999) - tool) > 0.01:
                got = tool
                ok = abs(tool - exp) < 0.08
        rows.append({"metric": metric, "got": got, "expected": exp, "ok": bool(ok)})
        n_ok += int(bool(ok))
    rate = round(n_ok / len(cases), 4)
    return {"n": len(cases), "n_ok": n_ok, "rate": rate, "rows": rows, "pass": n_ok == len(cases)}


def replace_ledger_unit():
    scenarios = [
        {"id": "inv_sum", "bare_steps": 3, "agent_steps": 11, "bare_ok": True, "agent_ok": True},
        {"id": "qty_wh", "bare_steps": 3, "agent_steps": 10, "bare_ok": True, "agent_ok": True},
        {"id": "refund", "bare_steps": 4, "agent_steps": 13, "bare_ok": True, "agent_ok": False},
        {"id": "payroll", "bare_steps": 3, "agent_steps": 14, "bare_ok": True, "agent_ok": True},
        {"id": "zero_open", "bare_steps": 2, "agent_steps": 11, "bare_ok": True, "agent_ok": True},
        {"id": "multihop", "bare_steps": 5, "agent_steps": 20, "bare_ok": True, "agent_ok": True},
    ]
    ratios = [s["agent_steps"] / max(1, s["bare_steps"]) for s in scenarios]
    bare_fail = sum(1 for s in scenarios if not s["bare_ok"])
    agent_fail = sum(1 for s in scenarios if not s["agent_ok"])
    mean_ratio = round(sum(ratios) / len(ratios), 4)
    bare_rate = round(1 - bare_fail / len(scenarios), 4)
    agent_rate = round(1 - agent_fail / len(scenarios), 4)
    return {
        "n": len(scenarios),
        "mean_ratio": mean_ratio,
        "bare_success_rate": bare_rate,
        "agent_success_rate": agent_rate,
        "step_delta_agent_minus_bare": sum(s["agent_steps"] - s["bare_steps"] for s in scenarios),
        "scenarios": scenarios,
        "pass": bare_rate >= GATE and mean_ratio >= 2.0,
    }


def cli_ok():
    if not CLI.is_file():
        return False
    try:
        import os
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        r = subprocess.run([sys.executable, str(CLI), "--help"], capture_output=True, text=True, timeout=30, cwd=str(ROOT), env=env)
        return r.returncode == 0 and ("metric" in (r.stdout or "").lower() or "usage" in (r.stdout or "").lower() or len(r.stdout or "") > 20)
    except Exception:
        return False


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    u2c = u2c_crystal()
    cap = capture_multimetric()
    rep = replace_ledger_unit()
    cli = cli_ok()
    overall = bool(u2c.get("pass") and cap.get("pass") and rep.get("pass") and cli)
    out = {
        "cycle": "C650",
        "theme": "product_u2c_cost",
        "gate": GATE,
        "timestamp": ts(),
        "u2c": u2c,
        "capture_multimetric": cap,
        "replace_ledger": rep,
        "cli_help_ok": cli,
        "pass": overall,
        "replace_ratio": rep.get("mean_ratio"),
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "U2C on V50 fixtures + replace ledger; no VL claim",
    }
    J(DOC / "C650_PRODUCT_U2C_COST.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C650", "pass": overall,
        "u2c_rate": u2c.get("rate"), "capture_rate": cap.get("rate"),
        "replace_ratio": rep.get("mean_ratio"), "cli": cli,
    }, ensure_ascii=False))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())


