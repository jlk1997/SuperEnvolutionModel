# 蚁算-视 VL Gate V1

Updated: 2026-10-18T22:39:11+08:00 (Asia/Shanghai)

Gate **0.6**. V0 untouched. Gate2/3 text claims untouched.

## Status: CLAIMED (scoped)

| Field | Value |
| --- | --- |
| vl_gate_v1_claim | **true** |
| rate | **0.8333** (10/12) |
| min_n | 8 (ran 12) |
| weights | models/Qwen3.5-2B |
| scope | `r50_v1_smoke_readable_office_drawn_n>=8_softmatch_qwen35_2b` |

## Root cause of prior fail (C47 rate=0.375)
`r50_cycle_engine.png()` wrote solid-color PNGs and stuffed gold into `tEXt` metadata.
Qwen correctly answered "blank white image".

## Fix
`scripts/regen_vision_v1_readable_fixtures.py` — high-contrast PIL text/tables/UI (Arial/Consolas).
Smoke: `scripts/vision_v1_smoke_real_vl.py` → `docs/r50/C52_vision_v1_smoke_readable.json`.

## Honest failures (2)
- `office-caption-002`: gold phrasing vs natural caption soft-match miss
- `office-hard-ui-001`: gold phrasing vs natural caption soft-match miss

## Iron
- No open-domain leaderboard claim
- No burned Gate3 packs
- No Gate2/3 unclaim
