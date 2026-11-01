# 蚁算-视 VL Gate V4 Protocol — Multi-hop Vision→Office

Updated: 2026-10-19 (Asia/Shanghai)

## Purpose
Scoped claim for **multi-hop** vision→office: image OCR → parse → table/file/report atoms → dissolve (scaffold_steps=0).
This is harder than V1–V3 single-shot OCR/caption.

## Gate
- Numeric gate: **0.6**
- n ≥ **8** fixtures (drawn readable office OR real desktop+office panel)
- Success per item: `ocr_ok` AND `atom_ok` (all hops in that item)
- Overall `rate = n_ok / n` must be ≥ 0.6 to PASS
- Claim only if PASS and protocol followed; tag `vl_gate_v4_claim=true` scoped

## Honesty
- Real VL weights required (`models/Qwen3.5-2B` or successor). No synthetic OCR pretending to be VL.
- Softmatch allowed for OCR stem/alias (same as V2/V3).
- Must report `ocr_rate`, `atom_rate`, `rate`, `dissolve_D`, per-row hops.
- Not open-domain vision. Not a Gate2/3 rewrite.
- Prior V0–V3 claims untouched. Gate2/3 CLAIMED untouched.

## Fixtures
- Mix of invoice / warehouse / shell-log / tax-table / PO / expense / payroll-snippet / shipping
- Prefer high-contrast readable drawn text (history: solid-color blanks fail VL)
- Heldout items must not be byte-identical to prior claimed sets

## Non-goals
- Does not mint Gate2 or Gate3
- Does not open gen11 seal
- Dense-table LoRA not required; product default remains **bare**

## V4 Heldout (C107+)
- Fixtures: evo/office/fixtures/vision_images_v4_heldout
- Disjoint from C101 train
- Claim: vl_gate_v4_heldout_claim=true only if n>=8 rate>=0.6
- Updated: 2026-10-19T02:03:13+08:00
