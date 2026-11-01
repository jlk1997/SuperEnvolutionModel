# EPOCH_B_EXIT — falsifiable exit criteria (Gate 0.6)

Updated: 2026-10-17 16:40 Asia/Shanghai

Living ledger of freeze/unfreeze: **docs/EPOCH_B_LEDGER.md**.

Competence gate **0.6 never lowered**. This doc is the checklist that closes Epoch B.
Marketing language is forbidden; every box is checkable from a file under 
uns/.

## Must-have (ALL required to mark B COMPLETE)

| ID | Criterion | Evidence file / command | Status |
| --- | --- | --- | --- |
| B-X1 | Stack second skill @>=0.6 beyond add (holdout or birth) | 
uns/capabilities/offset47_holdout bare_rate=1.0 | [x] |
| B-X2 | Third stack family or transfer skill @>=0.6 | ffine23_easy bare_rate=0.75 report | [x] |
| B-X3 | Multi-atom D=0 (add + offset + affine) | 
uns/capabilities/index.json + dissolve reports | [x] |
| B-X4 | Census site map documented across seeds | docs/CENSUS_ADD_INTERPRETATION.md | [x] |
| B-X5 | Office LM signal **informative** (not ceiling-tie) on smoke | judge informative=true in v3–v8 summaries | [x] |
| B-X6 | Office LM **exam dual_rate > agent_rate** AND both >0 | runs/office_bx6_recontrast_s0/.../summary.json dual=0.75 agent=0.25 | [x] rates 2026-10-17; Gate2 still blocked by CI/forget/present |
| B-X7 | Gate2 claim only after B-X6 + power path toward n≈160 | never set gate2_claim=true from proxy | [x] Gate2 claimed 2026-10-17 full slate; see docs/GATE2_OFFICE_JUDGE_2026-10-17.json |
| B-X8 | No Gate3 peek during B | process / MASTER_PLAN | [x] |

## Soft (nice-to-have before C entry; not blockers)

| ID | Criterion | Status |
| --- | --- | --- |
| B-S1 | Mid-n office power sketch | [x] gate2_mid_n_dual observational 2026-10-18 dual=0.8125 agent=0.125 CI n=16; no new Gate2 claim |
| B-S2 | Router strips notes when atom internalized (office _notes) | [x] |
| B-S3 | Practice bootstrap teaches (practice dual >> exam) | [x] v3–v8 practice ~6–8/8 |

## Kill switches (B stays PARTIAL / FAIL)

1. After **≥3** distinct model tool-format / SFT fixes (F3b–F3h), exam dual and agent still both 0 **and** writes do not move exam → document **office LM tool path FAIL on 1.5B**; escalate to larger local base (Qwen3.5-2B weights exist) or freeze office LM and enter C via use-log from practice dual writes only.
2. Affine-hard (non-easy) never clears → keep easy curriculum as B-X2 evidence; do not invent a third hard skill.
3. Any Gate2 claim from open-book / notes proxy → **invalid**; revert docs.

## Current closure read (2026-10-17 13:47 Asia/Shanghai)

- Cleared: B-X1..X5, B-X8, B-S2, B-S3.
- **CLOSED: Gate3 CLAIMED** 2026-10-18 gen10 (Branch A transfer). Evidence: docs/GATE3_GEN10_JUDGE_2026-10-18.json. Power mid-n optional.
- **Kill switch #1 (1.5B):** FIRED earlier — F3b–F3h exam dual=agent=0 on Qwen2.5-1.5B-Instruct.
- **Kill switch #2 (2B):** FIRED 2026-10-17 13:47 — \office_model_signal_smoke_2b\ summary:
  - agent exam=**0.0** practice=0/8
  - dual exam=**0.0** practice=2/8 writes=1
  - judge: dual_rate=0.0 agent_rate=0.0 informative=true; **not** dual>agent with rates>0
  - Evidence: uns/office_model_signal_smoke_2b_s0/20261017-134601/summary.json  - Document: **office LM exam path FAIL on Qwen3.5-2B smoke as well**.
- **Freeze:** do not spend more GPU on larger-base office *exam* ladder this blast unless new tool-format breakthrough. Continue Epoch C via use_log → XML-pair dissolve (C4 v3) without Gate2 claims.
- Innovation = **COMPLETE** (Gate2 + Gate3). **Epoch B COMPLETE.**

## Gate3 gen10 (2026-10-18) — CLAIMED

Pre-seal multi-seed CI. observatory+apiary d=2. seeds=[0,1,2] n=24.
- fresh_rate=0.75 trained_rate=1.0 · gain mean=0.25 CI[0.083,0.417] excludes_zero
- speed=true · pass_branch=**transfer** · gate3_claim=**true**
- Evidence: docs/GATE3_GEN10_JUDGE_2026-10-18.json
- gen9 lighthouse/tannery: crash-burned without judge (do not reopen)

## Gate3 gen8 (2026-10-18)

Pre-seal d85539f (column-name fix). marina+greenhouse d=2.
- fresh=0.75 trained=1.0 · table 0.5→1.0 · speed=true · transfer CI fails · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN8_JUDGE_2026-10-18.json

## Gate3 gen7 (2026-10-18)

Pre-seal 3c9481c. atelier+foundry d=2. Schema-random table SFT.
- fresh=trained=0.5 · table=0 · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN7_JUDGE_2026-10-18.json
- Block: d=2/3 table prompts omit column names

## Gate3 gen6 (2026-10-17)

Pre-seal 5530e13. harbor+orchard d=2. Table-overweight atom SFT.
- fresh=trained=0.5 · table=0 report=1 file=1 · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN6_JUDGE_2026-10-17.json

## Gate3 gen5 (2026-10-17)

Pre-seal 8a4979. cinema+nursery d=2. Atoms both + warm atom-adapter abbrev SFT.
- fresh_rate=0.5 trained_rate=0.5 gain=0 speed=true · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN5_JUDGE_2026-10-17.json

## Gate3 gen4 (2026-10-17)

Pre-seal 3bd30e7. museum+pharmacy d=2. Curriculum SFT + absorb-then-policy.
- fresh_rate=0.5 trained_rate=0.25 gain=-0.25 · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN4_JUDGE_2026-10-17.json

## Gate3 gen3 (2026-10-17)

Protocol Branch A/B committed **before** open (6bb0ed). Packs **ferry + bakery**, difficulty=4.
- fresh_rate=0.0 trained_rate=0.0 · all checks false · gate3_claim=false
- Evidence: docs/GATE3_GEN3_JUDGE_2026-10-17.json · pack burned
- library/warehouse still **not** claimable under Branch B retroactively

## Gate3 (2026-10-17 library/warehouse)

Opened **library + warehouse** (heldout_generation: next). actor=model, prefer_atoms, 1.5B.
- fresh_rate=**1.0** trained_rate=**1.0** n=8 · speed=**true** · transfer=**false** (gain 0 ceiling)
- judge.pass=**false** · gate3_claim=**false** · pack **burned**
- Evidence: docs/GATE3_OFFICE_JUDGE_2026-10-17.json
- Do not retune on this pair. Next: harder/gen3 seal or protocol heritability-ceiling clause before unsealing.

## Gate2 (2026-10-17)

Office judge **pass=true** + **gate2_claim=true** on full REQUIRED_ARMS (`office_gate2_full_slate`, dual_rate=0.625 agent_rate=0.125, CI low=0.125). Evidence: docs/GATE2_OFFICE_JUDGE_2026-10-17.json + runs/office_gate2_full_slate_s{0,1} summaries.

## Epoch B COMPLETE (2026-10-18)

Marked COMPLETE after Gate3 Branch A claim on gen10 (n=24, gate3_claim=true) with Gate2 already claimed and B-X1..X8 cleared per ledger. Evidence: docs/GATE3_GEN10_JUDGE_2026-10-18.json + docs/GATE2_OFFICE_JUDGE_2026-10-17.json. Still 1.5B; no VL; Gate 0.6.

## Definition: Epoch B COMPLETE

All of B-X1..B-X8 checked, OR explicit written kill on B-X6 with approved escalate path recorded in docs/STAGE_ASSESSMENT.md. Until then: do **not** write "Epoch B done".
