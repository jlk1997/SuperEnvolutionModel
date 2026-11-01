# -*- coding: utf-8 -*-
"""C106: Update STAGE/CHECKPOINT/loop for C100-C105. Read evidence JSONs honestly."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs"
R50 = DOC / "r50"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(name):
    p = R50 / name
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c100 = load("C100_V4_PROTOCOL.json") or {}
    c101 = load("C101_VISION_V4_MULTIHOP.json") or {}
    c102 = load("C102_DESKTOP_OFFICE_E2E.json") or {}
    c103 = load("C103_U2C_GROW_ABSORB_REUSE.json") or {}
    c104 = load("C104_REPLACE_HARDER.json") or {}
    c105 = load("C105_GEN11_HOLD.json") or {}

    now = ts()
    stage = f"""# STAGE_ANT_R50PLUS

Updated: {now} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (C100-C106 blast after C91-C99)

## Cycles landed (this batch C100-C106)
- **C100** V4 protocol registered exists={c100.get('protocol_exists')} pass={c100.get('pass')}
- **C101** Vision V4 multihop n={c101.get('n')} rate={c101.get('rate')} ocr={c101.get('ocr_rate')} atom={c101.get('atom_rate')} claim={c101.get('vl_gate_v4_claim')} pass={c101.get('pass')}
- **C102** desktop→office E2E capture={c102.get('capture_ok')} ocr={c102.get('ocr_ok')} atom={c102.get('atom_ok')} paid={c102.get('paid_got')} pass={c102.get('pass')}
- **C103** U2C grow n={c103.get('n_sessions')} crystal={c103.get('crystal_rate')} reuse_ok={c103.get('reuse_ok')} pass={c103.get('pass')}
- **C104** replace harder bare={c104.get('bare_rate')} replace={c104.get('replace_rate')} step_ratio={c104.get('step_ratio_agent_over_bare')} pass={c104.get('pass')}
- **C105** gen11 decision={c105.get('decision')} seal_opened={c105.get('seal_opened')}
- **C106** docs STAGE/CHECKPOINT/loop

## Iron
Gate **0.6**. Gate2/3 CLAIMED untouched. V1/V2/V2-heldout/V3-dense/V3-heldout claims untouched.
Vision V4 scoped claim only if C101 `vl_gate_v4_claim=true` (n≥8 rate≥0.6).
gen11 **HOLD** unless measured fresh≥0.99.
Vision LoRA: dense deprecated; product default **bare**.
No fake VL.

## Evidence
`docs/r50/C100_*.json` … `C105_*.json` · protocol `docs/蚁算视_VL_GATE_V4_PROTOCOL.md` · loop `docs/蚁算_R50PLUS_LOOP.md`
"""
    (DOC / "STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {now} — 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **0.6**. Gate2/3 CLAIMED untouched.
Vision V1/V2/V2-heldout/V3-dense/V3-heldout claims kept.
**C101 Vision V4**: n={c101.get('n')} rate={c101.get('rate')} vl_gate_v4_claim={c101.get('vl_gate_v4_claim')} (scoped multihop).
**C102 desktop office E2E**: capture={c102.get('capture_ok')} atom={c102.get('atom_ok')} paid={c102.get('paid_got')}.
**C103 U2C**: sessions={c103.get('n_sessions')} crystal={c103.get('crystal_rate')} reuse_ok={c103.get('reuse_ok')}.
**C104 replace harder**: bare={c104.get('bare_rate')} replace={c104.get('replace_rate')} ratio≈{c104.get('step_ratio_agent_over_bare')}.
Product vision default: **bare**.
gen11 seal_opened={c105.get('seal_opened')} decision={c105.get('decision')}.
"""
    (DOC / "CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    loop_path = DOC / "蚁算_R50PLUS_LOOP.md"
    prev = loop_path.read_text(encoding="utf-8") if loop_path.is_file() else "# 蚁算 R50PLUS LOOP\n\n"
    add = f"""
## C100-C106 @ {now}
- C100 protocol pass={c100.get('pass')}
- C101 V4 rate={c101.get('rate')} claim={c101.get('vl_gate_v4_claim')}
- C102 desktop E2E pass={c102.get('pass')} paid={c102.get('paid_got')}
- C103 U2C crystal={c103.get('crystal_rate')} reuse_ok={c103.get('reuse_ok')}
- C104 replace bare={c104.get('bare_rate')} ratio={c104.get('step_ratio_agent_over_bare')}
- C105 gen11 {c105.get('decision')} seal={c105.get('seal_opened')}
"""
    loop_path.write_text(prev.rstrip() + "\n" + add, encoding="utf-8")

    # dissolve refresh pointer
    dissolve = {
        "cycle": "C106",
        "theme": "docs_stage_checkpoint_dissolve_pointer",
        "gate": 0.6,
        "pointers": ["C100", "C101", "C102", "C103", "C104", "C105"],
        "v4_claim": c101.get("vl_gate_v4_claim"),
        "dissolve_D_vision_multihop": c101.get("dissolve_D"),
        "timestamp": now,
        "pass": True,
    }
    R50.mkdir(parents=True, exist_ok=True)
    (R50 / "C106_DOCS.json").write_text(json.dumps(dissolve, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOC / "DISSOLVE_DASHBOARD_C106_2026-10-19.json").write_text(
        json.dumps({
            "cycle": "C106",
            "families": {"table": {"bare": 1.0, "D": 0.0}, "report": {"bare": 1.0, "D": 0.0},
                         "file": {"bare": 1.0, "D": 0.0}, "shell": {"bare": 1.0, "D": 0.0}},
            "vision_v4_multihop": {"rate": c101.get("rate"), "D": c101.get("dissolve_D"), "claim": c101.get("vl_gate_v4_claim")},
            "timestamp": now,
            "note": "Pointer refresh; text four-family D unchanged at 0 unless remeasured.",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "cycle": "C106",
        "pass": True,
        "v4_claim": c101.get("vl_gate_v4_claim"),
        "c101_rate": c101.get("rate"),
        "c102_pass": c102.get("pass"),
        "c103_pass": c103.get("pass"),
        "c104_pass": c104.get("pass"),
        "gen11": c105.get("decision"),
        "timestamp": now,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
