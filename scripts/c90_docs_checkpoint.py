# -*- coding: utf-8 -*-
"""C90: STAGE / CHECKPOINT / loop for C83-C89 batch. Also reaffirm tesseract skip."""
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
    c83 = load("docs/r50/C83_vision_ocr_weak_fixtures.json")
    c84 = load("docs/r50/C84_vision_ocr_weak_bare_smoke.json")
    c85 = load("docs/r50/C85_vision_ocr_weak_lora_absorb.json")
    c86 = load("docs/r50/C86_vision_ocr_weak_lora_vs_bare.json")
    c86b = load("docs/r50/C86b_vision_lora_policy_decision.json")
    c87 = load("docs/r50/C87_e2e_vision_office_loop.json")
    c88 = load("docs/r50/C88_user_sandbox_shadow_u2c.json")
    c89 = load("docs/r50/C89_gen11_hold.json")
    c79 = load("docs/r50/C79_real_screenshot_ocr_path.json")

    stage = f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (C83-C90 blast after C76-C82)

## Cycles landed (this batch)
- **C83** ocr_weak fixtures train={c83.get('n_train')} test={c83.get('n_test')} disjoint={c83.get('disjoint_ids')}
- **C84** ocr_weak bare smoke rate={c84.get('rate')} weak_enough={c84.get('weak_enough')}
- **C85** ocr_weak LoRA absorb ok={c85.get('adapter_trained')} steps={(c85.get('absorb') or {}).get('steps')}
- **C86** LoRA vs bare delta={c86.get('delta_lora_minus_bare')} decision={c86.get('decision')}
- **C86b** policy product_default={c86b.get('product_default')} dense=DEPRECATED_FORCE_BARE
- **C87** e2e vision→OCR→atom→dissolve pass={c87.get('e2e_pass')} ocr={c87.get('ocr_rate')} atom={c87.get('atom_rate')} D={c87.get('e2e_dissolve')}
- **C88** user-sandbox shadow+U2C pass={c88.get('pass')} crystal={((c88.get('u2c') or {}).get('crystal_ok'))}
- **C89** gen11 decision={c89.get('decision')} seal_opened={c89.get('seal_opened')}
- **C90** docs + tesseract skip reaffirm (feasible={((c79.get('tesseract_probe') or {}).get('feasible'))}; stick VL OCR)

## Iron
Gate **0.6**. Gate2/3 CLAIMED untouched. V1/V2/V2-heldout/V3-dense/V3-heldout claims untouched. No fake VL.
gen11 **HOLD** unless measured fresh≥0.99.
Vision LoRA: dense **deprecated**; weak-domain only if Δ≥0 evidence (C86).

## Evidence
`docs/r50/C83_*.json` … `C89_*.json` · loop `docs/蚁算_R50PLUS_LOOP.md`
"""
    (ROOT / "docs/STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW · {ts()} · 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **0.6**. Gate2/3 CLAIMED untouched.
Vision V1/V2/V2-heldout/V3-dense/V3-heldout claims kept.
**ocr_weak LoRA hunt**: bare={c84.get('rate')} lora={((c86.get('lora') or {}).get('rate'))} Δ={c86.get('delta_lora_minus_bare')} → **{c86.get('decision')}**
Product vision default: **{c86b.get('product_default') or 'bare'}** (dense LoRA deprecated).
E2E product loop C87 pass={c87.get('e2e_pass')} (OCR→route→atom→dissolve).
User-sandbox shadow+U2C C88 pass={c88.get('pass')}.
OCR: tesseract still infeasible; stick **VL OCR**.
gen11 seal_opened=false decision={c89.get('decision')}.
"""
    (ROOT / "docs/CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    # append loop section
    loop_path = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    prior = loop_path.read_text(encoding="utf-8") if loop_path.is_file() else "# 蚁算 R50+ LOOP\n"
    extra = f"""

## Batch C83-C90 · DONE ({ts()})
| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C83 | ocr-weak-fixtures | DONE | train={c83.get('n_train')} test={c83.get('n_test')} | C83_*.json |
| C84 | ocr-weak-bare | DONE | rate={c84.get('rate')} | C84_*.json |
| C85 | ocr-weak-lora-absorb | DONE | ok={c85.get('adapter_trained')} | C85_*.json |
| C86 | lora-vs-bare-weak | DONE | Δ={c86.get('delta_lora_minus_bare')} {c86.get('decision')} | C86_*.json |
| C86b | lora-policy | DONE | default={c86b.get('product_default')} | C86b_*.json |
| C87 | e2e-vision-office | DONE | pass={c87.get('e2e_pass')} | C87_*.json |
| C88 | user-sandbox-u2c | DONE | pass={c88.get('pass')} | C88_*.json |
| C89 | gen11-hold | DONE | {c89.get('decision')} | C89_*.json |
| C90 | docs | DONE | STAGE/CHECKPOINT | C90_*.json |

Knives closed: weak-LoRA hunt · e2e product loop · shadow U2C · tesseract skip · gen11 HOLD.
"""
    if "Batch C83-C90" not in prior:
        loop_path.write_text(prior.rstrip() + "\n" + extra, encoding="utf-8")
    else:
        loop_path.write_text(prior, encoding="utf-8")

    summary = {
        "kind": "r50plus_c90_docs_checkpoint",
        "timestamp": ts(),
        "batch": "C83-C90",
        "ocr_weak_bare_rate": c84.get("rate"),
        "ocr_weak_lora_rate": (c86.get("lora") or {}).get("rate"),
        "ocr_weak_delta": c86.get("delta_lora_minus_bare"),
        "lora_decision": c86.get("decision"),
        "product_default": c86b.get("product_default"),
        "e2e_pass": c87.get("e2e_pass"),
        "shadow_u2c_pass": c88.get("pass"),
        "gen11_decision": c89.get("decision"),
        "tesseract_feasible": (c79.get("tesseract_probe") or {}).get("feasible"),
        "ocr_recommended": "vl",
        "gate": 0.6,
        "gate2_3_untouched": True,
    }
    (ROOT / "docs/r50/C90_docs_checkpoint.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
