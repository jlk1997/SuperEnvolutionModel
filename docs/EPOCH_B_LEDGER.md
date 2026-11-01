# EPOCH_B_LEDGER — honest open items (Gate 0.6)

Updated: 2026-10-17 21:15 Asia/Shanghai

## Gate2 FULL SLATE — PASS (`office_gate2_full_slate`)

Evidence:
- summaries: `runs/office_gate2_full_slate_s0/.../summary.json`, `..._s1/...`
- aggregate judge: `runs/office_gate2_full_slate_judge.json`
- ROADMAP `<!-- GATE2_START -->` block via write_gate

Config: dual `prefer_atoms=true` only; agent/oracle/dual_agent demos/scaffold; shift/continual/continual_sft bare model. seeds=[0,1] steps=8. 1.5B. No VL.

### Aggregate rates (exam)

| Arm | seed0 | seed1 | notes |
| --- | ---: | ---: | --- |
| dual | 0.75 | 0.50 | atoms |
| agent | 0.25 | 0.00 | demos, no atoms |
| oracle | 0.25 | 0.00 | |
| dual_agent | 0.25 | 0.00 | |
| shift | 0.00 | 0.00 | |
| continual | 0.00 | 0.00 | |
| continual_sft | 0.00 | 0.00 | |

Judge: dual_rate=**0.625** agent_rate=**0.125** | CI n=8 mean=0.5 **low=0.125** high=0.875 excludes_zero | **pass=true** | **gate2_claim=true**

| Check | Result |
| --- | --- |
| present | true (all 7 REQUIRED_ARMS) |
| beat_agent | true |
| above_schedules | true (dual ≥ shift/continual) |
| forget | true |
| safety | true |

### Still open (not Gate2 blockers in judge, but honesty)

- Power: full-slate n=8; mid-n observational DONE 2026-10-18 (dual=0.8125 agent=0.125 CI n=16 [0.4375,0.875]; still << n~160/800). Evidence: docs/GATE2_MID_N_OBSERVATIONAL_2026-10-18.json
- Innovation / Gate3: **CLAIMED** gen10 Branch A transfer n=24; Epoch B COMPLETE
- D deferred (no VL)

## Scores

- B **100% COMPLETE** (Gate2 + Gate3 transfer claim 2026-10-18)
- C = 100%
- Innovation **COMPLETE** (Gate2 + Gate3 gen10)
- D deferred
