# 蚁算-视 VL Gate V8 Heldout Protocol

Updated: 2026-10-19T04:40:18+08:00 (Asia/Shanghai)

## Purpose
Disjoint heldout for V8 train (C158b rate=1.0). Different ids/amounts.
Hardening vocabulary retained: low-contrast, fax, watermark 666/777, multi-stamp.
Parse: C158b (NOISE+=666, colon-decimal, dup-amount safe).

## Gate
- rate = n_ok/n >= **0.6**, n >= 16
- Real VL only (Qwen3.5-2B)
- Claim: `vl_gate_v8_heldout_claim=true` only on PASS

## Honesty
- No overlap with train expected totals / ids
- Gate2/3 untouched. V0–V7 untouched. gen11 HOLD.
