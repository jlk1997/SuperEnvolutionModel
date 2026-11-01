# STAGE_ANT_C130 — 蚁算 R50+ C125-C130

Updated: 2026-10-19T03:22:17+08:00 (Asia/Shanghai)

## Status
- **V5 train claim**: untouched (prior True rate=1.0)
- **V5 heldout**: rate=1.0 claim=True (only if >=0.6)
- **money_tool → capture E2E**: pass=True rate=1.0
- **real screenshot office**: pass=True rate=1.0 use_vl=True
- **replace/cost refresh**: pass=True ratio=2.6
- **gen11**: HOLD
- **Gate**: 0.6 — Gate2/3 untouched

## Evidence
- `docs/r50/C125_VISION_V5_HELDOUT_FIXTURES.json`
- `docs/r50/C126_VISION_V5_HELDOUT_SMOKE.json`
- `docs/r50/C126b_VISION_GATE_V5_HELDOUT_CLAIM.json` (only if claimed)
- `docs/r50/C127_MONEY_TOOL_CAPTURE_E2E.json`
- `docs/r50/C128_REAL_SCREENSHOT_OFFICE.json`
- `docs/r50/C129_REPLACE_COST_REFRESH.json`
- `docs/r50/C130_GEN11_HOLD.json`
- `docs/CHECKPOINT_NOW.md`

## Honesty
- No fake VL scores. Heldout claim only when rate>=0.6.
- U2C arithmetic still tool-backed (C120 ceiling).
- gen11 seal not opened.
