# STAGE_ANT_C165 — 蚁算 C162–C165

Updated: 2026-10-19T05:05:52+08:00 (Asia/Shanghai)

## Status: STAGE_READY

| Cycle | Theme | Result |
|------|------|--------|
| C162 | v8h_02 unglue 14.ok + heldout reparse | rate **1.0** (was 0.9375) refresh claim |
| C163 | Vision V9 real VL smoke | rate **1.0** n=16/16 **CLAIM** |
| C164 | Vision V9 heldout disjoint | rate **1.0** n=16/16 **CLAIM** |
| C165 | Product regression V4→V9 | overall **1.0** PASS |

## Honesty
- Gate 0.6 respected; claims only when rate≥0.6
- Gate2/3 text claims **untouched**
- gen11 **HOLD** (no seal opened)
- C160 fixture arg-order bug fixed before V9 smoke (manifest regenerated)
- C162 is cheap reparse of saved OCR (no new VL); V8 heldout claim refreshed to 1.0

## Artifacts
- docs/r50/C162_V8H02_UNGLUE_REPARSE.json
- docs/r50/C162b_VISION_GATE_V8_HELDOUT_REFRESH_CLAIM.json
- docs/r50/C163_VISION_V9_SMOKE.json / C163b_VISION_GATE_V9_CLAIM.json
- docs/r50/C164_VISION_V9_HELDOUT_SMOKE.json / C164b_VISION_GATE_V9_HELDOUT_CLAIM.json
- docs/r50/C165_PRODUCT_REGRESSION_SWEEP.json
- parse: evo/office/vision_metric_parse.py (C162 unglue)

## Next
- V10 design or V9 failure-stress if needed
- gen11 remains HOLD until explicit open
