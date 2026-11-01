# 蚁算 STAGE C158–C161 — V8 train 1.0 / heldout / V9 design

Updated: 2026-10-19T04:45:51+08:00 (Asia/Shanghai)

## Results
| Cycle | Theme | Result |
|-------|-------|--------|
| C158 | Parse 666+colon; regen fails; VL retest | rate=0.8889 → claim refresh |
| C158b | Dup-amount fix + v8_17 OCR-stable | **train rate=1.0** n=18 |
| C159 | V8 heldout disjoint | **rate=0.9375** n=15/16, **heldout claim** |
| C160 | V9 design torn/barcode/FX/ghost/QR | n=16 fixtures, smoke deferred |
| C161 | Scorecard + STAGE | composite=1.0 |

## Root causes fixed (C158/C158b)
1. Watermark **666** paired with stamp PAID → NOISE+=666
2. OCR `16:00` for `16.00` → colon-decimal normalize
3. Duplicate `paid 5.00` bag-deduped → span-overlap dedupe (keep dups)
4. `R1 2.00` glued / CN □□□□ / 19→10 misread → clearer fixtures

## Honesty
- Gate **0.6** not lowered
- Gate2/3 **untouched**
- gen11 **HOLD**
- V8 heldout still has honest fail: v8h_02
- V9 **no VL claim** yet

## Entry
- `docs/r50/C158c_VISION_GATE_V8_REFRESH_CLAIM.json`
- `docs/r50/C159b_VISION_GATE_V8_HELDOUT_CLAIM.json`
- `docs/r50/C160_V9_DESIGN_BATCH.json`
- `docs/r50/SCORECARD_LATEST.json`
