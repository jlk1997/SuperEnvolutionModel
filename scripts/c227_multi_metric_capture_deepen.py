# -*- coding: utf-8 -*-
"""C227: Product deepen — multi-metric capture CLI + docs + demo evidence.
Adds --metric / --expected to ant_capture_office (keeps --expected-paid compat).
Demo all office metrics under confidence gate. Gate 0.6.
Gate2/3 untouched. gen11 HOLD. No new VL claim.
"""
from __future__ import annotations
import json, re, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import tool_metric, confidence_gated_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs/multi_metric_capture_c227"
BOARD = ROOT / "docs" / "蚁算_MULTI_METRIC_CAPTURE.md"
README = ROOT / "docs" / "蚁算_截图办公_README.md"
LIB = ROOT / "scripts" / "ant_capture_office_lib.py"
CLI = ROOT / "scripts" / "ant_capture_office.py"

SUPPORTED = [
    "paid_total", "qty_sum", "refund_done", "tax_base_paid",
    "payroll_active", "ship_ok_qty", "open_pri_sum",
]

CASES = [
    ("mm_paid", "paid_total",
     ["a paid 46.00", "b paid 47.50", "c open 12.00", "TOTAL PAID TARGET 93.50"], 93.5, 120.0),
    ("mm_qty", "qty_sum",
     ["SKU1 qty 41 ok", "SKU2 qty 19 hold", "SKU3 qty 37 ok", "qty_sum TARGET 78"], 78.0, 60.0),
    ("mm_refund", "refund_done",
     ["itemR1 21.25 done", "itemR2 23.50 done", "itemR3 9.00 open", "refund_done TARGET 44.75"], 44.75, 50.0),
    ("mm_tax", "tax_base_paid",
     ["T1 82.00 paid", "T2 30.00 open", "T3 65.00 paid", "tax_base_paid TARGET 147.00"], 147.0, 100.0),
    ("mm_pay", "payroll_active",
     ["A 1310 active", "B 220 leave", "C 1170 active", "payroll_active TARGET 2480"], 2480.0, 2000.0),
    ("mm_ship", "ship_ok_qty",
     ["P1 32 ok", "P2 17 hold", "P3 31 ok", "ship_ok_qty TARGET 63"], 63.0, 80.0),
    ("mm_sla", "open_pri_sum",
     ["S1 pri 24 open", "S2 pri 31 closed", "S3 pri 31 open", "open_pri_sum TARGET 55"], 55.0, 86.0),
    ("mm_zero", "paid_total",
     ["OPEN ONLY V20", "X 61.00 open", "Y 64.00 open", "paid_total TARGET 0.00"], 0.0, 125.0),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_cli_lib():
    """Idempotent: add --metric / --expected support to capture lib."""
    src = LIB.read_text(encoding="utf-8")
    if "--metric" in src and "metric_got" in src:
        return {"patched": False, "reason": "already_present"}

    # Extend run_pipeline signature
    if "def run_pipeline(outdir, lines, expected_paid, use_vl, title=\"ANT CAPTURE OFFICE\"):" in src:
        src = src.replace(
            "def run_pipeline(outdir, lines, expected_paid, use_vl, title=\"ANT CAPTURE OFFICE\"):",
            "def run_pipeline(outdir, lines, expected_paid, use_vl, title=\"ANT CAPTURE OFFICE\", metric=\"paid_total\", expected=None):",
        )

    # After paid parse block, inject multi-metric path if not present
    needle = "paid, gate_meta = parse_paid(text, model_guess=None, return_meta=True)"
    if needle in src and "metric_got" not in src:
        inject = '''paid, gate_meta = parse_paid(text, model_guess=None, return_meta=True)
    # C227 multi-metric: when metric != paid_total, confidence-gated tool wins
    metric_name = metric or "paid_total"
    exp_val = float(expected_paid if expected is None else expected)
    if metric_name != "paid_total" and MONEY_TOOL and CONFIDENCE_GATE:
        gated_m = confidence_gated_metric(text or "", metric_name, model_guess=None, expected=exp_val, tol=0.08)
        paid = float(gated_m.get("value") if gated_m.get("value") is not None else 0.0)
        gate_meta = gated_m
    elif metric_name != "paid_total" and MONEY_TOOL:
        tv = tool_metric(text or "", metric_name)
        paid = float(tv) if tv is not None else 0.0
        gate_meta = {"source": "tool_metric", "metric": metric_name, "value": paid}
'''
        src = src.replace(needle, inject, 1)

    # Update paid_ok / evidence to include metric fields
    if '"paid_got": paid,' in src and '"metric":' not in src.split('"paid_got": paid,')[1][:200]:
        src = src.replace(
            '"paid_got": paid,\n        "paid_expected": float(expected_paid), "paid_ok": paid_ok,',
            '"paid_got": paid,\n        "metric": metric_name if "metric_name" in dir() else "paid_total",\n'
            '        "metric_got": paid,\n'
            '        "paid_expected": float(exp_val if "exp_val" in dir() else expected_paid), "paid_ok": paid_ok,',
            1,
        )
        # also fix paid_ok to use exp_val
        src = src.replace(
            "paid_ok = abs(paid - float(expected_paid)) < 0.08",
            "exp_for_ok = float(exp_val) if \"exp_val\" in dir() else float(expected_paid)\n"
            "    paid_ok = abs(paid - exp_for_ok) < 0.08",
            1,
        )

    # argparse
    if 'ap.add_argument("--dry-run"' in src and "--metric" not in src:
        src = src.replace(
            'ap.add_argument("--dry-run", action="store_true", help="Force --no-vl and default lines")',
            'ap.add_argument("--dry-run", action="store_true", help="Force --no-vl and default lines")\n'
            '    ap.add_argument("--metric", type=str, default="paid_total",\n'
            '                    help="Office metric: paid_total|qty_sum|refund_done|tax_base_paid|payroll_active|ship_ok_qty|open_pri_sum")\n'
            '    ap.add_argument("--expected", type=float, default=None,\n'
            '                    help="Expected metric value (defaults to --expected-paid for paid_total)")',
        )
    if "evidence = run_pipeline(outdir, lines, args.expected_paid, use_vl=use_vl, title=args.title)" in src:
        src = src.replace(
            "evidence = run_pipeline(outdir, lines, args.expected_paid, use_vl=use_vl, title=args.title)",
            "exp = args.expected if args.expected is not None else args.expected_paid\n"
            "    evidence = run_pipeline(outdir, lines, args.expected_paid, use_vl=use_vl, title=args.title,\n"
            "                           metric=args.metric, expected=exp)",
        )
    # CLI print enrichment
    if '"paid_got": evidence.get("paid_got"),' in src and '"metric":' not in src.split("print(json.dumps")[1][:400]:
        src = src.replace(
            '"paid_got": evidence.get("paid_got"),\n        "errors": evidence.get("errors"),\n        "pass": evidence.get("pass"),',
            '"paid_got": evidence.get("paid_got"),\n'
            '        "metric": evidence.get("metric", "paid_total"),\n'
            '        "metric_got": evidence.get("metric_got", evidence.get("paid_got")),\n'
            '        "errors": evidence.get("errors"),\n        "pass": evidence.get("pass"),',
        )

    # fix CSV export to use metric name
    if 'f"metric,value\\npaid_total,{paid:.2f}\\n"' in src:
        src = src.replace(
            'f"metric,value\\npaid_total,{paid:.2f}\\n"',
            'f"metric,value\\n{(metric_name if \'metric_name\' in dir() else \'paid_total\')},{paid:.2f}\\n"',
        )

    LIB.write_text(src, encoding="utf-8")
    return {"patched": True, "reason": "c227_multi_metric_cli"}


def write_docs():
    BOARD.write_text(
        f"""# 蚁算多指标截图办公（C227）

Updated: {ts()} (Asia/Shanghai)

## 一句话
一次 capture 会话可按 `--metric` 评估：`paid_total` / `qty_sum` / `refund_done` /
`tax_base_paid` / `payroll_active` / `ship_ok_qty` / `open_pri_sum`。
模型与工具不一致时 **置信门控强制走 tool**。

## CLI

```bash
python scripts/ant_capture_office.py --no-vl --metric qty_sum --expected 78 \\
  --lines-file path/to/lines.txt --outdir runs/demo_qty
```

兼容：未传 `--metric` 时仍为 `paid_total`；`--expected-paid` 仍可用。

## 指标表
| metric | 工具语义 |
| --- | --- |
| paid_total | 求和 status=paid |
| qty_sum | 求和 `qty N ok` |
| refund_done | 求和 `N done` |
| tax_base_paid | 求和 `N paid`（税基） |
| payroll_active | 求和 `N active` |
| ship_ok_qty | 求和 `N ok` |
| open_pri_sum | 求和 `pri N open` |

## 门控
Gate **0.6**。Gate2/3 不动。gen11 HOLD。
""",
        encoding="utf-8",
    )
    if README.is_file():
        txt = README.read_text(encoding="utf-8", errors="replace")
        if "--metric" not in txt:
            txt += f"""

## 多指标（C227）
支持 `--metric` 与 `--expected`。详见 `docs/蚁算_MULTI_METRIC_CAPTURE.md`。

```bash
python scripts/ant_capture_office.py --no-vl --metric refund_done --expected 44.75 \\
  --lines-file runs/multi_metric_capture_c227/mm_refund_lines.txt \\
  --outdir runs/multi_metric_capture_c227/cli_refund
```

Updated C227: {ts()}
"""
            README.write_text(txt, encoding="utf-8")
    return True


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    patch_info = patch_cli_lib()
    write_docs()

    # unit: confidence gate across metrics
    rows, n_ok = [], 0
    for cid, metric, lines, expected, wrong in CASES:
        text = " ".join(lines)
        tool = tool_metric(text, metric)
        gated = confidence_gated_metric(text, metric, model_guess=wrong, expected=expected, tol=0.08)
        agree = confidence_gated_metric(text, metric, model_guess=expected, expected=expected, tol=0.08)
        ok = (
            gated.get("value") is not None
            and abs(float(gated["value"]) - expected) < 0.08
            and gated.get("decision") in ("force_tool", "fallback_tool", "disagree_force_tool", "trust_model", "agree_prefer_tool")
        )
        # for disagree case must force tool
        if abs(float(wrong) - expected) > 0.08:
            ok = ok and gated.get("decision") in ("force_tool", "disagree_force_tool", "fallback_tool")
        n_ok += int(ok)
        rows.append({
            "id": cid, "metric": metric, "expected": expected,
            "tool": tool, "gated_value": gated.get("value"),
            "gated_decision": gated.get("decision"),
            "agree_decision": agree.get("decision"),
            "ok": ok,
        })
        # write lines file for CLI demo
        lp = RUN / f"{cid}_lines.txt"
        lp.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # CLI demos (no-vl) for a few metrics
    cli_rows = []
    for cid, metric, lines, expected, _wrong in CASES[:4]:
        outdir = RUN / f"cli_{cid}"
        lp = RUN / f"{cid}_lines.txt"
        r = subprocess.run(
            [
                sys.executable, str(CLI),
                "--no-vl",
                "--metric", metric,
                "--expected", str(expected),
                "--expected-paid", str(expected),
                "--title", f"ANT C227 {metric}",
                "--outdir", str(outdir),
                "--lines-file", str(lp),
            ],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        try:
            payload = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:
            payload = {"ok": False, "raw": (r.stdout or "")[:200], "err": (r.stderr or "")[:200]}
        cli_ok = bool(payload.get("ok") or payload.get("pass"))
        cli_rows.append({"id": cid, "metric": metric, "cli_ok": cli_ok, "payload": payload, "returncode": r.returncode})

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    cli_ok_n = sum(1 for c in cli_rows if c["cli_ok"])
    cli_pass = cli_ok_n == len(cli_rows) and len(cli_rows) > 0
    gate_pass = n >= 6 and rate >= GATE and cli_pass and BOARD.is_file()
    out = {
        "cycle": "C227",
        "theme": "multi_metric_capture_deepen",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "rows": rows,
        "cli_rows": cli_rows,
        "cli_pass": cli_pass,
        "patch": patch_info,
        "supported_metrics": SUPPORTED,
        "board": str(BOARD.relative_to(ROOT)).replace("\\", "/"),
        "pass": gate_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C227 product deepen multi-metric CLI+docs+demo; no VL claim",
    }
    J(DOC / "C227_MULTI_METRIC_CAPTURE_DEEPEN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C227", "rate": rate, "cli_pass": cli_pass,
        "patch": patch_info, "pass": gate_pass,
        "cli_ok_n": cli_ok_n, "cli_n": len(cli_rows),
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
