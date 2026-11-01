# -*- coding: utf-8 -*-
"""C82: Update STAGE / CHECKPOINT / R50PLUS loop for C76-C81."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(p):
    pp = ROOT / p
    return json.loads(pp.read_text(encoding="utf-8")) if pp.is_file() else {}


def main():
    c76 = load("docs/r50/C76_vision_v3_heldout_fixtures.json")
    c77 = load("docs/r50/C77_vision_v3_heldout_smoke.json")
    c77c = load("docs/r50/C77c_vision_gate_v3_heldout_claim.json")
    c78 = load("docs/r50/C78_vision_route_policy_smoke.json")
    c79 = load("docs/r50/C79_real_screenshot_ocr_path.json")
    c80 = load("docs/r50/C80_dual_cost_refresh.json")
    c81 = load("docs/r50/C81_gen11_hold.json")

    stage = f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (C76-C82 blast)

## Cycles landed (this batch)
- **C76** V3 heldout harder fixtures n={c76.get('n')} (disjoint from v3_dense)
- **C77** V3 heldout smoke rate={c77.get('rate')} claim={c77c.get('vl_gate_v3_heldout_claim')}
- **C78** vision route policy smoke rate={c78.get('rate')} (dense-table→bare; LoRA only weak)
- **C79** real screenshot OCR path: tesseract={c79.get('tesseract_probe',{}).get('feasible')} vl_rate={(c79.get('vl_ocr_eval') or {}).get('rate')} recommended={(c79.get('path_landed') or {}).get('recommended')}
- **C80** dual/cost refresh replace_rate={c80.get('replace_rate')} GPU=false
- **C81** gen11 decision={c81.get('decision')} seal_opened={c81.get('seal_opened')}
- **C82** docs

## Iron
Gate **0.6**. Gate2/3 CLAIMED untouched. V1/V2/V2-heldout/V3-dense claims untouched. No fake VL.
gen11 **HOLD** unless measured fresh≥0.99.

## Routing policy (productized)
`evo/office/vision_route.py`: dense_table / table_cells → **bare**; LoRA only on weak domains when adapter present.
Evidence: C66/C72 LoRA hurts dense tables.

## Evidence
`docs/r50/C76_*.json` … `C81_*.json` · loop `docs/蚁算_R50PLUS_LOOP.md`
"""
    (ROOT / "docs/STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **0.6**. Gate2/3 CLAIMED untouched.
Vision V1/V2/V2-heldout/V3-dense claims kept.
**V3 heldout claim={c77c.get('vl_gate_v3_heldout_claim')} rate={c77c.get('rate')} n={c77c.get('n')}** (bare).
Route policy landed: dense-table→bare; LoRA only weak domains (C78 rate={c78.get('rate')}).
OCR path: tesseract infeasible on jlk; VL OCR recommended (C79 vl_rate={(c79.get('vl_ocr_eval') or {}).get('rate')}).
Dual cost C80 replace={c80.get('replace_rate')}.
gen11 seal_opened=false decision={c81.get('decision')}.
"""
    (ROOT / "docs/CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    loop = f"""# 蚁算 R50+ LOOP

Updated: {ts()} (Asia/Shanghai)

Mandate: continuous evolution after R50 / Vision claims. Gate **0.6**. Gate2/3 untouched. No fake VL. gen11 HOLD unless fresh≥0.99.

## Progress

| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C65-C69 | prior batch | DONE | heldout 1.0 / LoRA -0.1 | C65-C69 |
| C70-C75 | prior batch | DONE | V3 dense 1.0 / LoRA ceiling | C70-C75 |
| C76 | v3-heldout-fix | DONE | n={c76.get('n')} | C76_*.json |
| C77 | v3-heldout-smoke | DONE | rate={c77.get('rate')} claim={c77c.get('vl_gate_v3_heldout_claim')} | C77_*.json |
| C78 | vision-route-policy | DONE | rate={c78.get('rate')} | C78_*.json |
| C79 | real-ocr-path | DONE | tess=False vl={(c79.get('vl_ocr_eval') or {}).get('rate')} | C79_*.json |
| C80 | dual-cost-refresh | DONE | replace={c80.get('replace_rate')} | C80_*.json |
| C81 | gen11-hold | DONE | HOLD | C81_*.json |
| C82 | docs | DONE | STAGE/CHECKPOINT | C82_*.json |

## Batch C76-C82 — DONE
- V3 heldout harder set claimed only if ≥0.6 (got {c77c.get('rate')})
- Routing policy code + smoke
- Honest OCR path (no tesseract; VL path works)
- gen11 HOLD
"""
    (ROOT / "docs/蚁算_R50PLUS_LOOP.md").write_text(loop, encoding="utf-8")

    summary = {
        "kind": "r50plus_c82_docs_checkpoint",
        "timestamp": ts(),
        "batch": "C76-C82",
        "v3_heldout_claim": c77c.get("vl_gate_v3_heldout_claim"),
        "v3_heldout_rate": c77c.get("rate"),
        "route_smoke_rate": c78.get("rate"),
        "ocr_tesseract_feasible": (c79.get("tesseract_probe") or {}).get("feasible"),
        "ocr_vl_rate": (c79.get("vl_ocr_eval") or {}).get("rate"),
        "dual_replace_rate": c80.get("replace_rate"),
        "gen11_decision": c81.get("decision"),
        "gate": 0.6,
        "gate2_3_untouched": True,
    }
    (ROOT / "docs/r50/C82_docs_checkpoint.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
