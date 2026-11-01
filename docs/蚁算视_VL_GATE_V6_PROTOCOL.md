# 蚁算-视 VL Gate V6 Protocol — Noisy UI / Multi-Window / CN+EN

Updated: 2026-10-19T03:27:25+08:00 (Asia/Shanghai)

## Purpose
Harder than V5: **noisy UI chrome**, **multi-window panels**, and **Chinese+English mixed**
office sheets. Tests OCR + atom under distractors (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **12** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v6_claim=true` only if PASS + real VL (C132)

## Hardening vs V5
- Three windows (WIN-A gold / WIN-B noise / WIN-C chrome)
- Fake taskbar + red badges + overlapping labels
- Mixed CN titles with EN metrics (`订单` / `发票` + paid/open)
- Smaller fonts, more distractor numbers (999 / void / DRAFT)
- Desktop blend noise retained

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V5 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v6`
- Manifest: `manifest.json`
