# 蚁算 STAGE C153–C157 — V7 linen fix / V8 / week sandbox

Updated: 2026-10-19T04:26:44+08:00 (Asia/Shanghai)

## Results
| Cycle | Theme | Result |
|-------|-------|--------|
| C153 | Fix lineN/rowN index-as-amount; V7 retest | **rate=1.0** n=16, claim refresh |
| C154 | V8 design (fax/low-con/multistamp/watermark) | n=18 fixtures |
| C155 | V8 real VL smoke | **rate=0.7222** n=13/18, **vl_gate_v8_claim=true** |
| C156 | Week sandbox 7 days | rate=1.0, week_paid=1526.0 |
| C157 | Scorecard refresh | see SCORECARD_LATEST |

## Root cause (C153)
`line1 paid 5.50` / `row1 paid 2.75` matched trailing index as amount-THEN-status → fake paid 1+2. Fixed with leading `\b` in `vision_metric_parse.iter_amount_status_pairs`.

## Honesty
- Gate **0.6** not lowered
- Gate2/3 **untouched**
- gen11 **HOLD**
- V8 fails left honest: v8_03, v8_11, v8_15, v8_16, v8_17 (still above gate)
- Prior V0–V7 heldout claims retained

## Entry
- `docs/r50/C153_V7_LINEN_FIX_RETEST.json`
- `docs/r50/C155b_VISION_GATE_V8_CLAIM.json`
- `docs/r50/C156_WEEK_SANDBOX.json`
- `docs/r50/SCORECARD_LATEST.json`
