# 蚁算-视 VL Gate V8 Protocol — Low-contrast / Fax / Multi-stamp / Watermark

Updated: 2026-10-19T04:17:06+08:00 (Asia/Shanghai)

## Purpose
Harder than V7: **low-contrast paper**, **fax/carbon scan noise**, **stacked stamps**,
**skew/fold bands**, **watermark money distractors**, **handwritten scribble**.
Still scoped office OCR+atom (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **16** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v8_claim=true` only if PASS + real VL (C155)

## Hardening vs V7
- Paper fill ~ (210,205,195) on noisy bg; ink ~ (45,45,45) (lower contrast)
- Speckle + horizontal fax lines
- Two overlapping circular stamps (PAID + VOID ghost)
- Watermark big digits (777/666) behind line items — must be ignored
- Diagonal scribble lines simulating pen marks
- Tiny 8–9pt fonts; TARGET still present but muted
- Retain occlusion fold + coffee stain from V7 vocabulary

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V7 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v8`
- Manifest: `manifest.json`
