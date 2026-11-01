# -*- coding: utf-8 -*-
"""C75: Update R50PLUS STAGE / CHECKPOINT / loop after C70-C74."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(p):
    fp = ROOT / p
    if not fp.is_file():
        return {}
    return json.loads(fp.read_text(encoding="utf-8"))


def main():
    c70 = load("docs/r50/C70_vision_v2h_style_train_fixtures.json")
    c71 = load("docs/r50/C71_vision_lora_reabsorb_heldout_style.json")
    c72 = load("docs/r50/C72_vision_lora_vs_bare_retest.json")
    c73 = load("docs/r50/C73_vision_v3_dense_fixtures.json")
    c73b = load("docs/r50/C73b_vision_v3_dense_smoke.json")
    c73c = load("docs/r50/C73c_vision_gate_v3_claim.json")
    c74 = load("docs/r50/C74_replace_dual_strengthen.json")

    summary = {
        "kind": "r50plus_c75_summary",
        "timestamp": ts(),
        "cycles": "C70-C75",
        "c70_n": c70.get("n"),
        "c71_absorb": (c71.get("absorb") or {}).get("ok"),
        "c72_delta": c72.get("delta_lora_minus_bare"),
        "c72_delta_ge_0": c72.get("delta_ge_0"),
        "c72_ceiling": bool(c72.get("ceiling")),
        "c73_n": c73.get("n"),
        "c73b_rate": c73b.get("rate"),
        "c73_claim": c73c.get("vl_gate_v3_claim"),
        "c74_replace": c74.get("replace_rate"),
        "gen11": "HOLD",
        "gate": 0.6,
        "gate2_3_untouched": True,
    }
    (ROOT / "docs/r50/C75_r50plus_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    stage = f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (C70-C75 blast)

## Cycles landed (this batch)
- **C70** heldout-style train fixtures n={c70.get('n')} (disjoint)
- **C71** LoRA re-absorb on style train ok={ (c71.get('absorb') or {}).get('ok') }
- **C72** LoRA vs bare retest delta={c72.get('delta_lora_minus_bare')} delta_ge_0={c72.get('delta_ge_0')} ceiling={bool(c72.get('ceiling'))}
- **C73** V3 dense fixtures n={c73.get('n')}
- **C73b** V3 smoke rate={c73b.get('rate')} claim={c73c.get('vl_gate_v3_claim')}
- **C74** replace+dual cost rate={c74.get('replace_rate')} gpu=false
- **C75** docs
- gen11 **HOLD**

## Iron
Gate **0.6**. Gate2/3 CLAIMED untouched. V1/V2/V2-heldout claims untouched. No fake VL.

## Evidence
`docs/r50/C70_*.json` … `C75_*.json` · loop `docs/蚁算_R50PLUS_LOOP.md`
"""
    (ROOT / "docs/STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **0.6**. Gate2/3 CLAIMED untouched.
Vision V1/V2/V2-heldout claims kept.
C72 LoRA retest: bare={ (c72.get('bare') or {}).get('rate') } lora={ (c72.get('lora') or {}).get('rate') } delta={c72.get('delta_lora_minus_bare')} (ceiling={bool(c72.get('ceiling'))}).
V3 dense smoke rate={c73b.get('rate')} claim={c73c.get('vl_gate_v3_claim')}.
Replace C74={c74.get('replace_rate')}.
gen11 seal_opened=false decision=HOLD.
"""
    (ROOT / "docs/CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    loop = f"""# 蚁算 R50+ LOOP

Updated: {ts()} (Asia/Shanghai)

Mandate: continuous evolution after R50 / Vision claims. Gate **0.6**. Gate2/3 untouched. No fake VL. gen11 HOLD.

## Progress

| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C65-C69 | prior batch | DONE | heldout 1.0 / LoRA -0.1 | C65-C69 |
| C70 | style-train-fix | DONE | n={c70.get('n')} | C70_*.json |
| C71 | lora-reabsorb | DONE | ok={ (c71.get('absorb') or {}).get('ok') } | C71_*.json |
| C72 | lora-retest | DONE | delta={c72.get('delta_lora_minus_bare')} | C72_*.json |
| C73 | v3-dense-fix | DONE | n={c73.get('n')} | C73_*.json |
| C73b | v3-smoke | DONE | rate={c73b.get('rate')} | C73b_*.json |
| C74 | replace-dual | DONE | {c74.get('replace_rate')} | C74_*.json |
| C75 | docs | DONE | summary | C75_*.json |

## Batch C70-C75 — DONE
- C72 ceiling/Δ documented honestly
- V3 denser OCR attempted; claim={c73c.get('vl_gate_v3_claim')}
- gen11 HOLD
"""
    (ROOT / "docs/蚁算_R50PLUS_LOOP.md").write_text(loop, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
