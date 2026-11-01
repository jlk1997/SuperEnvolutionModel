# -*- coding: utf-8 -*-
"""C133: Package ant_capture_office as clearer product demo + one-shot evidence.
Gate 0.6. No Gate2/3. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys, textwrap
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import run_pipeline, MONEY_TOOL, validate_evidence

GATE = 0.6
DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/capture_product_demo_c133"
DEMO_MD = ROOT / "docs" / "蚁算_CAPTURE_OFFICE_DEMO.md"
README_SNIP = ROOT / "docs" / "蚁算_CAPTURE_ONESHOT.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ONESHOT_LINES = [
    "DEMO INVOICE #ANT-C133",
    "latte paid 4.50",
    "sandwich paid 12.00",
    "juice open 3.00",
    "TOTAL PAID TARGET 16.50",
]
EXPECTED = 16.50


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)

    # one-shot dry evidence (deterministic, no VL required)
    outdir = RUN / "oneshot_dry"
    ev = run_pipeline(outdir, ONESHOT_LINES, EXPECTED, use_vl=False, title="ANT CAPTURE DEMO")
    schema_errs = validate_evidence(ev)
    ok = bool(ev.get("ok")) and bool(ev.get("money_tool")) and abs(float(ev.get("paid_got", -1)) - EXPECTED) < 0.08 and not schema_errs

    # copy evidence to docs-facing path
    evidence_path = DOC / "C133_CAPTURE_ONESHOT_EVIDENCE.json"
    J(evidence_path, {
        "product": "ant_capture_office",
        "timestamp": ts(),
        "oneshot": True,
        "use_vl": False,
        "expected_paid": EXPECTED,
        "evidence": ev,
        "schema_errors": schema_errs,
        "ok": ok,
        "cli": "python scripts/ant_capture_office.py --expected-paid 16.5 --title \"ANT CAPTURE DEMO\"",
        "lib": "scripts/ant_capture_office_lib.py",
        "money_tool": bool(MONEY_TOOL),
    })

    demo_md = f"""# 蚁算 Capture Office 产品演示

Updated: {ts()} (Asia/Shanghai)

## 一句话
截屏/面板 → OCR（可选 VL）→ **money_tool 求和** → 办公原子 → 证据 JSON。脚手架步数固定低，不走 agent 图。

## 一键命令
```bash
cd E:\\envolution
python scripts/ant_capture_office.py --expected-paid 16.5 --title "ANT CAPTURE DEMO"
```

可选：
- `--no-vl` 跳过视觉（本演示默认 dry 已证明 money_tool）
- `--outdir PATH` 指定输出
- `--lines-file PATH` 自定义行文本
- `--dry-run` 仅构建面板与证据骨架

## 证据字段（schema）
`entry, timestamp, gate, capture_ok, size, use_vl, scaffold_steps, agent_graph, ocr_ok, paid_got, paid_expected, paid_ok, atom_ok, ok, pass, rate, errors`  
另含 `money_tool` / `money_policy`（C127+）。

## 本轮 one-shot
- expected_paid: **{EXPECTED}**
- paid_got: **{ev.get('paid_got')}**
- money_tool: **{ev.get('money_tool')}**
- ok: **{ok}**
- evidence: `docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json`

## 诚实边界
- 金额算术走 **tool**，不靠 1.5B LoRA 心算（C120 天花板）
- 稠密表视觉路由优先 **bare**
- 不冒充 Gate2/3；gen11 HOLD
"""
    DEMO_MD.write_text(demo_md, encoding="utf-8")

    oneshot_md = f"""# 蚁算 Capture One-Shot

```bash
python scripts/ant_capture_office.py --expected-paid 16.5 --title "ANT CAPTURE DEMO"
```

Evidence: `docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json`  
Result: paid_got={ev.get('paid_got')} expected={EXPECTED} ok={ok} money_tool={bool(MONEY_TOOL)}
Updated: {ts()}
"""
    README_SNIP.write_text(oneshot_md, encoding="utf-8")

    rate = 1.0 if ok else 0.0
    out = {
        "cycle": "C133",
        "theme": "capture_office_product_demo_oneshot",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "money_tool": bool(MONEY_TOOL),
        "oneshot_ok": ok,
        "paid_got": ev.get("paid_got"),
        "paid_expected": EXPECTED,
        "schema_errors": schema_errs,
        "demo_doc": str(DEMO_MD.relative_to(ROOT)).replace("\\", "/"),
        "oneshot_doc": str(README_SNIP.relative_to(ROOT)).replace("\\", "/"),
        "evidence": str(evidence_path.relative_to(ROOT)).replace("\\", "/"),
        "rate": rate,
        "pass": rate >= GATE,
        "claim": False,
        "note": "Product packaging + honest dry one-shot. VL optional at CLI.",
    }
    J(DOC / "C133_CAPTURE_PRODUCT_DEMO.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C133", "ok": ok, "rate": rate, "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
