# U2C Absorb Ceiling Diagnosis · C120

Updated: 2026-10-19T03:04:01+08:00 (Asia/Shanghai)

## What happened
- C108 trained_rate≈**0.33** (n_eval=3, tiny).
- C114 / C114b push → trained_rate=**0.0** (n_eval=9).

## Root cause (ranked)
1. **Data mix / domain hard**: status-filter CSV arithmetic + larger floats.
2. **1.5B LoRA ceiling**: learns `key=` format, not correct sums.
3. **Grader exactness**: wrong numbers = hard fail (secondary).
4. **Adapter load**: NOT broken — trained ≠ bare predictions.

## Product rule
- Money math → **tool-backed sum** (not LoRA guess).
- Crystal/reuse path stays; **no absorb gate claim**.
- Gate2/3 untouched. gen11 HOLD.

Evidence: `docs/r50/C120_U2C_ABSORB_DIAGNOSIS.json`
