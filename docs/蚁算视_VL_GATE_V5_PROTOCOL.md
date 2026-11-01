# 蚁算-视 VL Gate V5 Protocol — Cluttered Real-Screenshot Office

Updated: 2026-10-19T02:57:00+08:00 (Asia/Shanghai)

## Purpose
Harder than V4: **cluttered / multi-zone** office panels on (or blended with) real desktop
screenshots. Tests OCR + multi-hop office under visual noise (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **10** fixtures
- Per item: `ocr_ok` AND `atom_ok` (parse metric + write atom artifact)
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim tag: `vl_gate_v5_claim=true` only if PASS + real VL weights used
- Heldout claim separate: `vl_gate_v5_heldout_claim`

## Hardening vs V4
- Smaller fonts / denser lines
- Multiple invoices or tables in one panel
- Mixed EN + short CN labels allowed
- Desktop wallpaper / UI chrome noise (blend), not blank solid-color
- Softmatch OCR stems still allowed; numeric atom must be exact within 0.08

## Honesty
- Real VL (`models/Qwen3.5-2B` or successor). No synthetic OCR pretending to be VL.
- Prior V0–V4 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Product dense-table route remains **bare**.

## Non-goals
- Not open-domain AGI vision
- Does not mint Gate2/3 or open gen11

## Fixtures
- Path: `evo/office/fixtures/vision_images_v5`
- Manifest: `manifest.json` with gold metric + expected value
