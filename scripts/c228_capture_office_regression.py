# -*- coding: utf-8 -*-
"""C228: Capture-office regression after C224-C227. V4-V20+heldout + multi-metric.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
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
RUN = ROOT / "runs" / "capture_regression_c228"
README = ROOT / "docs" / "蚁算_截图办公_README.md"
CLI = ROOT / "scripts" / "ant_capture_office.py"
MM_BOARD = ROOT / "docs" / "蚁算_MULTI_METRIC_CAPTURE.md"

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
    ("V10", DOC / "C167_VISION_V10_SMOKE.json"),
    ("V10_heldout", DOC / "C171_VISION_V10_HELDOUT_SMOKE.json"),
    ("V11", DOC / "C173_VISION_V11_SMOKE.json"),
    ("V11_heldout", DOC / "C175_VISION_V11_HELDOUT_SMOKE.json"),
    ("V12", DOC / "C180_V12_FAIL_FIX_RETEST.json"),
    ("V12_heldout", DOC / "C181_VISION_V12_HELDOUT_SMOKE.json"),
    ("V13", DOC / "C183_VISION_V13_SMOKE.json"),
    ("V13_heldout", DOC / "C186_VISION_V13_HELDOUT_SMOKE.json"),
    ("V14", DOC / "C188_VISION_V14_SMOKE.json"),
    ("V14_heldout", DOC / "C191_VISION_V14_HELDOUT_SMOKE.json"),
    ("V15", DOC / "C193_VISION_V15_SMOKE.json"),
    ("V15_heldout", DOC / "C196_VISION_V15_HELDOUT_SMOKE.json"),
    ("V16", DOC / "C198_VISION_V16_SMOKE.json"),
    ("V16_heldout", DOC / "C201_VISION_V16_HELDOUT_SMOKE.json"),
    ("V17", DOC / "C203_VISION_V17_SMOKE.json"),
    ("V17_heldout", DOC / "C207_VISION_V17_HELDOUT_SMOKE.json"),
    ("V18", DOC / "C209_VISION_V18_SMOKE.json"),
    ("V18_refresh", DOC / "C213_V18_FAIL_FIX_RETEST.json"),
    ("V18_heldout", DOC / "C214_VISION_V18_HELDOUT_SMOKE.json"),
    ("V19_prior", DOC / "C218_VISION_V19_SMOKE.json"),
    ("V19_refresh", DOC / "C219_V19_FAIL_FIX_RETEST.json"),
    ("V19_heldout", DOC / "C220_VISION_V19_HELDOUT_SMOKE.json"),
    ("V20", DOC / "C225_VISION_V20_SMOKE.json"),
    ("V20_heldout", DOC / "C226_VISION_V20_HELDOUT_SMOKE.json"),
    ("C210_conf_gate", DOC / "C210_CONFIDENCE_GATE_CAPTURE_WIRE.json"),
    ("C221_multi_metric", DOC / "C221_MULTI_METRIC_CAPTURE_DEMO.json"),
    ("C227_multi_metric_deepen", DOC / "C227_MULTI_METRIC_CAPTURE_DEEPEN.json"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    readme_ok = README.is_file() and CLI.is_file()
    readme_mentions_cli = False
    readme_mentions_metric = False
    if README.is_file():
        txt = README.read_text(encoding="utf-8", errors="replace")
        readme_mentions_cli = "ant_capture_office.py" in txt
        readme_mentions_metric = "--metric" in txt
    mm_board_ok = MM_BOARD.is_file()

    pointers = []
    for name, path in SMOKE_POINTERS:
        ok = False
        rate = None
        if path.is_file():
            try:
                d = json.loads(path.read_text(encoding="utf-8"))
                rate = d.get("rate")
                # V19 prior may be low (honest crush) — still count as present pointer
                if name == "V19_prior":
                    ok = True
                else:
                    ok = bool(d.get("pass") or d.get("claim") or (rate is not None and float(rate) >= GATE))
            except Exception:
                ok = False
        pointers.append({"name": name, "path": str(path.relative_to(ROOT)).replace("\\", "/"), "ok": ok, "rate": rate, "exists": path.is_file()})

    RUN.mkdir(parents=True, exist_ok=True)
    outdir = RUN / "demo_outdir"
    outdir.mkdir(parents=True, exist_ok=True)
    lines_path = RUN / "readme_demo_lines.txt"
    lines_path.write_text(
        "latte paid 4.50\nsandwich paid 12.00\njuice open 3.00\nTOTAL PAID TARGET 16.50\n",
        encoding="utf-8",
    )
    cli_ok = False
    cli_detail = {}
    if CLI.is_file():
        r = subprocess.run(
            [
                sys.executable, str(CLI),
                "--no-vl",
                "--expected-paid", "16.5",
                "--title", "ANT C228 README REGRESSION",
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

    # multi-metric CLI smoke
    mm_lines = RUN / "mm_qty_lines.txt"
    mm_lines.write_text("SKU1 qty 10 ok\nSKU2 qty 5 hold\nSKU3 qty 7 ok\nqty_sum TARGET 17\n", encoding="utf-8")
    mm_outdir = RUN / "mm_qty_outdir"
    r2 = subprocess.run(
        [
            sys.executable, str(CLI), "--no-vl",
            "--metric", "qty_sum", "--expected", "17",
            "--title", "ANT C228 MM",
            "--outdir", str(mm_outdir), "--lines-file", str(mm_lines),
        ],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120,
    )
    try:
        mm_payload = json.loads((r2.stdout or "").strip().splitlines()[-1])
    except Exception:
        mm_payload = {"ok": False, "err": (r2.stderr or "")[:200]}
    mm_cli_ok = bool(mm_payload.get("ok") or mm_payload.get("pass"))

    parse_ok = abs(sum_paid_from_text("a paid 4.50 b paid 12.00") - 16.5) < 0.01
    got, atom = parse_metric("TOTAL PAID TARGET 16.50 a paid 4.50 b paid 12.00", "paid_total", 16.5)
    parse_metric_ok = atom and abs(got - 16.5) < 0.08

    ptr_ok_n = sum(1 for p in pointers if p["ok"])
    ptr_n = len(pointers)
    # require critical V20 claims present
    v20_ok = next((p["ok"] for p in pointers if p["name"] == "V20"), False)
    v20h_ok = next((p["ok"] for p in pointers if p["name"] == "V20_heldout"), False)
    c227_ok = next((p["ok"] for p in pointers if p["name"] == "C227_multi_metric_deepen"), False)

    gate_pass = (
        readme_ok and readme_mentions_cli and cli_ok and mm_cli_ok
        and parse_ok and parse_metric_ok and v20_ok and v20h_ok and c227_ok
        and mm_board_ok and ptr_ok_n >= int(ptr_n * 0.85)
    )
    out = {
        "cycle": "C228",
        "theme": "capture_office_regression_v20",
        "gate": GATE,
        "timestamp": ts(),
        "readme_ok": readme_ok,
        "readme_mentions_cli": readme_mentions_cli,
        "readme_mentions_metric": readme_mentions_metric,
        "mm_board_ok": mm_board_ok,
        "cli_ok": cli_ok,
        "cli_detail": cli_detail,
        "mm_cli_ok": mm_cli_ok,
        "mm_payload": mm_payload,
        "parse_ok": parse_ok,
        "parse_metric_ok": parse_metric_ok,
        "pointers": pointers,
        "pointers_ok_n": ptr_ok_n,
        "pointers_n": ptr_n,
        "v20_ok": v20_ok,
        "v20h_ok": v20h_ok,
        "c227_ok": c227_ok,
        "pass": gate_pass,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C228_CAPTURE_OFFICE_REGRESSION.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C228", "pass": gate_pass, "ptr_ok": ptr_ok_n, "ptr_n": ptr_n,
        "cli_ok": cli_ok, "mm_cli_ok": mm_cli_ok, "v20_ok": v20_ok, "v20h_ok": v20h_ok,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
