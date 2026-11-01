# -*- coding: utf-8 -*-
"""C123: Sync CHECKPOINT/STAGE + gen11 HOLD after C113-C122."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_rate(name, key="rate"):
    p = DOC / name
    if not p.exists():
        return None
    o = json.loads(p.read_text(encoding="utf-8"))
    if key in o:
        return o.get(key)
    if "trained" in o and isinstance(o["trained"], dict):
        return o["trained"].get("rate")
    return o.get("vl_gate_v5_claim")


def main():
    v5 = json.loads((DOC / "C121_VISION_V5_SMOKE.json").read_text(encoding="utf-8"))
    diag = json.loads((DOC / "C120_U2C_ABSORB_DIAGNOSIS.json").read_text(encoding="utf-8"))
    money = json.loads((DOC / "C122_PRODUCT_MONEY_TOOL.json").read_text(encoding="utf-8"))

    hold = {
        "cycle": "C124",
        "theme": "gen11_hold",
        "timestamp": ts(),
        "decision": "HOLD",
        "seal_opened": False,
        "reason": "Continue R50+ vision/product; do not open Gate3 gen11 burn pack",
        "gate2_3_untouched": True,
        "pass": True,
        "claim": False,
    }
    J(DOC / "C124_GEN11_HOLD.json", hold)

    ck = f"""# CHECKPOINT_NOW · {ts()} · 蚁算模型

**R50PLUS=YES** · HEAD pending C120-C124

Gate **0.6**. Gate2/3 untouched. gen11 **HOLD**.

## C113–C119 (already at e20742c)
- **C113** U2C grow pairs (~82)
- **C114/C114b** absorb push → trained=**0.0** (ceiling documented, no claim)
- **C115** capture harden tests=**1.0**
- **C116** V5 design n=12 (smoke deferred then)
- **C117** dissolve/cost refresh
- **C118** gen11 HOLD
- **C119** docs

## C120–C124 (this knife)
- **C120** U2C diagnosis: format_ok=9/9, arith_wrong=9/9 → data mix + 1.5B LoRA ceiling; adapter DID load; **no absorb claim**
- **C121** Vision V5 smoke: n={v5.get('n')} rate=**{v5.get('rate')}** vl_gate_v5_claim=**{v5.get('vl_gate_v5_claim')}** (scoped cluttered screenshot office)
- **C122** product money tool tests rate=**{money['tests']['rate']}** (tool-backed sum preferred)
- **C124** gen11 HOLD

## Product defaults
- Vision dense-table: **bare**
- Money math: **tool-backed** (`evo/office/money_tool.py`)
- U2C absorb gate: **not claimed**

## Untouched
- Gate2 / Gate3 text claims
- Vision V0–V4 claims
- gen11 seal closed
"""
    (ROOT / "docs" / "CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    stage = f"""# STAGE_ANT_C124 · 蚁算 R50+ after V5

Updated: {ts()} (Asia/Shanghai)

## Status
- **V5 claim**: `{v5.get('vl_gate_v5_claim')}` rate={v5.get('rate')} n={v5.get('n')} scope=`{v5.get('claim_scope')}`
- **U2C absorb**: ceiling documented (C120); product uses tool-backed money
- **gen11**: HOLD
- **Gate**: 0.6 · Gate2/3 untouched

## Evidence
- `docs/r50/C120_U2C_ABSORB_DIAGNOSIS.json`
- `docs/U2C_ABSORB_CEILING_DIAGNOSIS.md`
- `docs/r50/C121_VISION_V5_SMOKE.json`
- `docs/r50/C121b_VISION_GATE_V5_CLAIM.json`
- `docs/r50/C122_PRODUCT_MONEY_TOOL.json`
- `docs/r50/C124_GEN11_HOLD.json`
- `docs/CHECKPOINT_NOW.md`

## Next (optional)
- V5 heldout batch
- Wire money_tool into more office families
- Still HOLD gen11 until intentional seal protocol
"""
    (ROOT / "docs" / "STAGE_ANT_C124.md").write_text(stage, encoding="utf-8")

    # append brief to R50PLUS stage
    plus = ROOT / "docs" / "STAGE_ANT_R50PLUS.md"
    if plus.exists():
        text = plus.read_text(encoding="utf-8")
        if "C121 Vision V5" not in text:
            text += f"\n\n### C120–C124 · {ts()}\n- C120 U2C diagnosis (ceiling)\n- C121 V5 claim rate={v5.get('rate')}\n- C122 money tool\n- C124 gen11 HOLD\n"
            plus.write_text(text, encoding="utf-8")

    out = {
        "cycle": "C123",
        "theme": "docs_sync_c113_c124",
        "timestamp": ts(),
        "gate": GATE,
        "gate2_3_untouched": True,
        "v5_rate": v5.get("rate"),
        "v5_claim": v5.get("vl_gate_v5_claim"),
        "u2c_claim": False,
        "gen11": "HOLD",
        "files": [
            "docs/CHECKPOINT_NOW.md",
            "docs/STAGE_ANT_C124.md",
            "docs/STAGE_ANT_R50PLUS.md",
            "docs/r50/C124_GEN11_HOLD.json",
        ],
        "pass": True,
        "claim": False,
        "note": "Synced stale CHECKPOINT with C113-C124 facts.",
    }
    J(DOC / "C123_DOCS_SYNC.json", out)
    print(json.dumps({"cycle": "C123", "v5_claim": v5.get("vl_gate_v5_claim"), "gen11": "HOLD"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
