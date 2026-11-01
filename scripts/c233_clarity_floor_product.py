# -*- coding: utf-8 -*-
"""C233: Product deepen — pin clarity_floor into capture README + office floor doc.
CPU-only. No new VL claim. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
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
RUN = ROOT / "runs/clarity_floor_product_c233"
README = ROOT / "docs" / "蚁算_截图办公_README.md"
FLOOR = ROOT / "docs" / "蚁算_CLARITY_FLOOR.md"
CLI = ROOT / "scripts" / "ant_capture_office.py"
DESIGN = DOC / "C230_VISION_V21_DESIGN.json"

FLOOR_BODY = """# 蚁算 Clarity Floor（截图办公可读性地板）

Updated: {ts} (Asia/Shanghai)

## Why
C218 jpeg_q22 + photocopy/3 crushed digits → V19 prior rate≈0.056.
V20+ enforce a **clarity floor** so VL gates test document understanding,
not jpeg destruction.

## Mandatory floor
| Knob | Min / Max | V21 value |
| --- | --- | --- |
| jpeg quality | >= **58** | 60 |
| photocopy downsample | max **/2** (not /3) | /2 |
| Gaussian blur radius | <= **0.5** | 0.45 |
| Text band protect | y≈70–250 | no glyph-wipe overlays on TARGET lines |

## Product rule
Capture-office demos and Vision V20+ fixtures MUST respect this floor.
Gate remains **0.6**. Gate2/3 untouched. gen11 HOLD.
"""


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pin_readme():
    if not README.is_file():
        return {"ok": False, "reason": "missing_readme"}
    txt = README.read_text(encoding="utf-8", errors="replace")
    marker = "## Clarity floor"
    block = (
        "\n## Clarity floor\n"
        "- jpeg_q >= 58 (V21 uses 60); photocopy max /2; blur <= 0.5\n"
        "- Protect TARGET text band; see docs/蚁算_CLARITY_FLOOR.md\n"
        "- Lesson: C218 jpeg crush → honest fail; do not reopen crush path\n"
    )
    if marker in txt:
        # refresh: replace from marker to next ## or EOF lightly
        return {"ok": True, "patched": False, "reason": "already_present"}
    README.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return {"ok": True, "patched": True}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    FLOOR.write_text(FLOOR_BODY.format(ts=ts()), encoding="utf-8")
    readme_pin = pin_readme()
    design = {}
    if DESIGN.is_file():
        design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cf = design.get("clarity_floor") or {}

    # CPU capture smoke
    outdir = RUN / "demo_outdir"
    outdir.mkdir(parents=True, exist_ok=True)
    lines_path = RUN / "demo_lines.txt"
    lines_path.write_text(
        "latte paid 5.50\nsandwich paid 13.00\njuice open 4.00\nTOTAL PAID TARGET 18.50\n",
        encoding="utf-8",
    )
    cli_ok = False
    cli_detail = {}
    if CLI.is_file():
        r = subprocess.run(
            [
                sys.executable, str(CLI), "--no-vl",
                "--expected-paid", "18.5",
                "--title", "ANT C233 CLARITY FLOOR",
                "--outdir", str(outdir),
                "--lines-file", str(lines_path),
            ],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        try:
            cli_detail = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:
            cli_detail = {"raw": (r.stdout or "")[:300], "err": (r.stderr or "")[:300]}
        cli_ok = bool(cli_detail.get("ok") or cli_detail.get("pass"))

    parse_ok = abs(sum_paid_from_text("a paid 5.50 b paid 13.00") - 18.5) < 0.01
    got, atom = parse_metric("TOTAL PAID TARGET 18.50 a paid 5.50 b paid 13.00", "paid_total", 18.5)
    parse_metric_ok = atom and abs(got - 18.5) < 0.08
    floor_doc_ok = FLOOR.is_file() and "jpeg" in FLOOR.read_text(encoding="utf-8")
    readme_mentions = False
    if README.is_file():
        rt = README.read_text(encoding="utf-8", errors="replace")
        readme_mentions = "Clarity floor" in rt or "clarity floor" in rt.lower() or "jpeg_q" in rt

    gate_pass = (
        floor_doc_ok and readme_pin.get("ok") and readme_mentions
        and cli_ok and parse_ok and parse_metric_ok
        and float(cf.get("jpeg_q") or 0) >= 58
        and int(cf.get("photocopy_div") or 99) <= 2
    )
    out = {
        "cycle": "C233",
        "theme": "clarity_floor_product_pin",
        "gate": GATE,
        "timestamp": ts(),
        "floor_doc": str(FLOOR.relative_to(ROOT)).replace("\\", "/"),
        "floor_doc_ok": floor_doc_ok,
        "readme_pin": readme_pin,
        "readme_mentions": readme_mentions,
        "clarity_floor": cf,
        "cli_ok": cli_ok,
        "cli_detail": cli_detail,
        "parse_ok": parse_ok,
        "parse_metric_ok": parse_metric_ok,
        "rate": 1.0 if gate_pass else 0.0,
        "pass": gate_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C233 product pin clarity floor; no VL claim",
    }
    J(DOC / "C233_CLARITY_FLOOR_PRODUCT.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C233", "pass": gate_pass, "cli_ok": cli_ok,
        "floor_doc_ok": floor_doc_ok, "readme_mentions": readme_mentions,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
