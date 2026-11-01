# STAGE_ANT_C136 — 蚁算 R50+ C131-C136

Updated: 2026-10-19T03:34:18+08:00 (Asia/Shanghai)

## Status
- **V6 design**: pass=True n=14
- **V6 smoke**: rate=1.0 claim=True (only if >=0.6)
- **Capture product demo**: pass=True oneshot_ok=True
- **Unified replace board**: pass=True rate=1.0 mean_ratio=3.425
- **U2C sandbox money_tool**: pass=True rate=1.0 absorb_claim=False
- **gen11**: HOLD (open only if fresh>=0.99; not met)
- **Gate**: 0.6 — Gate2/3 untouched

## Evidence
- `docs/r50/C131_V6_DESIGN_BATCH.json`
- `docs/r50/C132_VISION_V6_SMOKE.json`
- `docs/r50/C132b_VISION_GATE_V6_CLAIM.json` (only if claimed)
- `docs/r50/C133_CAPTURE_PRODUCT_DEMO.json`
- `docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json`
- `docs/r50/C134_UNIFIED_REPLACE_BOARD.json`
- `docs/r50/C135_U2C_SANDBOX_MONEY_TOOL.json`
- `docs/r50/C136_GEN11_HOLD.json`
- `docs/蚁算_CAPTURE_OFFICE_DEMO.md`
- `docs/蚁算_UNIFIED_REPLACE_BOARD.md`
- `docs/CHECKPOINT_NOW.md`

## Honesty
- No fake VL scores. V6 claim only when rate>=0.6 with real VL.
- U2C arithmetic tool-backed; absorb_claim=false.
- gen11 seal not opened.
- Prior V0–V5 / Gate2 / Gate3 untouched.
