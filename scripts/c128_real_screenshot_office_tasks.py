# -*- coding: utf-8 -*-
"""C128: More real-screenshot office tasks via capture+money_tool. Optional VL if free."""
from __future__ import annotations
import json, sys, shutil, gc
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import run_pipeline

DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/real_screenshot_office_c128"
GATE = 0.6
WEIGHTS = ROOT / "models/Qwen3.5-2B"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


TASKS = [
    {
        "id": "rs_cafe",
        "title": "CAFE RECEIPT H",
        "lines": ["CAFE #441", "latte paid 4.50", "muffin open 3.00", "tea paid 3.50", "TOTAL PAID TARGET 8.00"],
        "expected": 8.0,
    },
    {
        "id": "rs_parts",
        "title": "PARTS TICKET H",
        "lines": ["PARTS 902", "bolt paid 2.25", "nut paid 1.75", "washer open 0.50", "TOTAL PAID TARGET 4.00"],
        "expected": 4.0,
    },
    {
        "id": "rs_consult",
        "title": "CONSULT INV H",
        "lines": ["CONSULT", "hour1 paid 80.00", "hour2 paid 80.00", "travel open 20.00", "TOTAL PAID TARGET 160.00"],
        "expected": 160.0,
    },
    {
        "id": "rs_subs",
        "title": "SUBS LEDGER H",
        "lines": ["SUBS", "planA paid 9.99", "planB paid 14.99", "trial open 0.00", "TOTAL PAID TARGET 24.98"],
        "expected": 24.98,
    },
    {
        "id": "rs_zero",
        "title": "OPEN QUEUE H",
        "lines": ["OPEN ONLY", "ticket 12.00 open", "ticket 8.00 open", "paid_total TARGET 0.00"],
        "expected": 0.0,
    },
    {
        "id": "rs_freight",
        "title": "FREIGHT H",
        "lines": ["FREIGHT", "leg1 paid 33.00", "leg2 paid 17.00", "hold open 5.00", "TOTAL PAID TARGET 50.00"],
        "expected": 50.0,
    },
]


def gpu_free_mib():
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        return float((r.stdout or "0").strip().split("\n")[0])
    except Exception:
        return 0.0


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    free = gpu_free_mib()
    use_vl = free >= 2500 and WEIGHTS.is_dir()
    rows = []
    n_ok = 0
    for t in TASKS:
        outdir = RUN / t["id"]
        ev = run_pipeline(outdir, t["lines"], t["expected"], use_vl=use_vl, title=t["title"])
        ok = bool(ev.get("ok")) and abs(float(ev.get("paid_got", -999)) - t["expected"]) < 0.08
        n_ok += int(ok)
        rows.append({
            "id": t["id"],
            "ok": ok,
            "paid_got": ev.get("paid_got"),
            "paid_expected": t["expected"],
            "money_tool": ev.get("money_tool"),
            "capture_ok": ev.get("capture_ok"),
            "use_vl": use_vl,
            "ocr_preview": (ev.get("ocr_text") or "")[:160],
            "errors": ev.get("errors"),
        })
        gc.collect()

    n = len(rows)
    rate = n_ok / n if n else 0.0
    out = {
        "cycle": "C128",
        "theme": "real_screenshot_office_tasks_money_tool",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "use_vl": use_vl,
        "gpu_free_mib": free,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "pass": rate >= GATE,
        "claim": False,
        "rows": rows,
        "note": "Desktop blend panels + money_tool sums. VL used only if GPU free>=2500.",
    }
    J(DOC / "C128_REAL_SCREENSHOT_OFFICE.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C128", "rate": round(rate, 4), "use_vl": use_vl, "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
