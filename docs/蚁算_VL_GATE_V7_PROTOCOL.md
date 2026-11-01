# 蚁算-视 VL Gate V7 Protocol — Occlusion / Tiny Font / Stamped Receipt

Updated: 2026-10-19T03:49:27+08:00 (Asia/Shanghai)

## Purpose
Harder than V6: **occlusion** (stamps, bands), **tiny fonts** on line items,
and **stamped receipt** chrome. Still scoped office OCR+atom (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **14** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v7_claim=true` only if PASS + real VL (C144)

## Hardening vs V6
- Line-item fonts ~9–10pt; TARGET kept readable but smaller than V6
- Red circular RECEIVED/PAID stamps overlapping mid-panel
- Semi-transparent occlusion bands & coffee-stain ellipses
- Receipt stub chrome + torn-edge noise
- Retain multi-window distractors (WIN-B void / WIN-C chat)

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V6 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v7`
- Manifest: `manifest.json`
