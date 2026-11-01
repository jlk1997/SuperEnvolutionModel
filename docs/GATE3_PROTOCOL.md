# GATE3_PROTOCOL — sealed pack + transfer (Gate 0.6)

Pre-registered. Amend only **before** opening a new seal. Post-hoc claims on burned packs are invalid.

## Pack generations (burn-on-open)

| Gen | Packs | Status |
| --- | --- | --- |
| first | grades, roster | **Burned** (~2026-10-09); fresh=trained=0; no claim |
| next | library, warehouse | **Burned** (2026-10-17); fresh=trained=1.0 ceiling; no claim |
| gen3 | ferry, bakery | **Burned** (2026-10-17); fresh=trained=0 at difficulty=4; no claim |
| gen4 | museum, pharmacy | **Burned** (2026-10-17); fresh=0.5 trained=0.25; no claim |
| gen5 | cinema, nursery | **Burned** (2026-10-17); fresh=trained=0.5; speed=true; no claim |
| gen6 | harbor, orchard | **Burned** (2026-10-17); table=0 report/file=1; no claim |
| gen7 | atelier, foundry | **Burned** (2026-10-18); table=0 after schema-random SFT; no claim |
| gen8 | marina, greenhouse | **Burned** (2026-10-18); table 0.5→1.0, overall 0.75→1.0; transfer CI fails; no claim |
| gen9 | lighthouse, tannery | **Burned** (2026-10-18); crash NameError mid-run after seal; no judge |
| gen10 | observatory, apiary | **Burned** (2026-10-18); Branch A PASS gate3_claim=true |

Opening writes 
uns/heldout_seal_<gen>.json and refuses a second open on that record. Retuning after a red judge on the same pair is **invalid**.

## Pre-registered pass criteria (falsifiable)

Claim Gate3 only when ctor: model, measured: true, evidence JSON + ROADMAP GATE3 block written, still **1.5B** / no VL / Gate **0.6**.

Let resh_rate / 	rained_rate be mean of heldout item flags. Let gain be paired bootstrap(trained, fresh). Let speed be held_touches <= dev_touches * 1.3 (touches = attempts until trailing window hits rate 0.8; window=1).

### Branch A — transfer (learning gain)
**All** of:
1. speed is true
2. resh_rate < 1.0 (room to improve; otherwise use Branch B)
3. gain.excludes_zero and gain.mean > 0

→ gate3_claim=true, pass_branch=transfer

### Branch B — ceiling / heritability (pre-registered alternate)
**All** of:
1. speed is true
2. resh_rate >= 0.6
3. **Ceiling clause:** resh_rate >= 0.99 AND 	rained_rate >= 0.99 AND bs(gain.mean) <= 1e-9

→ gate3_claim=true, pass_branch=heritability

### Fail
If neither branch holds → pass=false, gate3_claim=false. Burn the pack. Change only the learning rule; seal a **new** pair for the next attempt.

### Explicit non-claims
- Never claim Gate3 on **library/warehouse** or **grades/roster** after the fact (including by reinterpreting ceiling on those burns).
- Reference-only actor: seal may open but pass=false, measured=false.

## Learning rule under test (gen10 revision — committed before open)
gen9 seal opened then crashed (\_SCHEMA_WORDS\ missing after multi-seed patch) — **no judge, no claim, pack burned**.
Same Branch A CI plan as gen9: seeds=[0,1,2], heldout_items=4, column fix, atoms both, schema-random + warm atom SFT. Constant restored.

## gen10 design intent
New industries **observatory + apiary**. Burn-on-open via load_gen10_heldout.

## How to run (gen10)
python -m evo heldout --config configs/office_gate3_gen10.yaml

## Learning rule under test (gen9 revision — committed before open)
gen8 near-miss: gain=0.25 but n=8 CI includes 0. Scale flags via **seeds×items**.
1. Keep column-name fix (d<=3), prefer_atoms both ends, schema-random + warm atom SFT.
2. **seeds=[0,1,2]**, heldout_items=4 → n_flags=24 if pattern holds; CI should exclude 0 at gain≈0.25.
3. Eval difficulty=2. Branch A target: speed ∧ fresh<1 ∧ gain>0 ∧ CI excludes 0.

## gen9 design intent
New industries **lighthouse + tannery**. Burn-on-open via load_gen9_heldout.

## How to run (gen9)
python -m evo heldout --config configs/office_gate3_gen9.yaml

## Learning rule under test (gen8 revision — committed before open)
gen7 root cause fixed in code: table CSV prompts at difficulty <= 3 now **name columns**; d>=4 abbreviated.
1. prefer_atoms=true both ends.
2. Schema-random DEV table SFT + table-overweight warm atom SFT (as gen7).
3. Eval difficulty=2 (now with column names in prompt). Success: family_diag.table > 0; aim A/B.

## gen8 design intent
New industries **marina + greenhouse**. difficulty=2. Burn-on-open via load_gen8_heldout.

## How to run (gen8)
python -m evo heldout --config configs/office_gate3_gen8.yaml

## Learning rule under test (gen7 revision — committed before open)
gen6: table=0 forever under new schemas; DEV orders/expenses SFT insufficient.
1. prefer_atoms=true both ends.
2. **Schema-randomized DEV table SFT** (probe-style): synthetic packs with random column names; n>=16; difficulties [1,2,3]; never sealed packs.
3. Keep table-overweight abbrev curriculum on real DEV + warm atom-adapter SFT (rounds/epochs/lr as gen6).
4. Eval difficulty=2. Success: sealed family_diag.table > 0 (aim A or B overall).

## gen7 design intent
New industries **atelier + foundry**. difficulty=2. Burn-on-open via load_gen7_heldout.

## How to run (gen7)
python -m evo heldout --config configs/office_gate3_gen7.yaml

## Learning rule under test (gen6 revision — committed before open)
gen5 diagnosis: at d=2, **table always failed**, report/file always passed (fresh=trained=0.5 identical). Rules:
1. prefer_atoms=true on BOTH ends.
2. Abbreviated curriculum SFT into warm atom adapters; **table overweight** schedule (table,table,table,report,file); dev_items=24; sft_rounds=4; sft_epochs=4; atom_sft_lr=1e-3.
3. Eval difficulty=2. Family-level diag recorded in judge.
4. Aim Branch B (rates→≥0.99) or Branch A (trained>fresh with CI).

## gen6 design intent
New industries **harbor + orchard**. difficulty=2. Burn-on-open via load_gen6_heldout.

## How to run (gen6)
python -m evo heldout --config configs/office_gate3_gen6.yaml
## Learning rule under test (gen5 revision — committed before open)
gen4 falsified absorb-then-policy (trained atoms-off hurt: 0.5→0.25). gen5 rules:
1. **prefer_atoms=true on BOTH fresh and trained** (no absorb-then-policy).
2. **Abbreviated curriculum SFT into warm atom adapters** (table/report/file), difficulties [2,3], DEV orders+expenses, sft_rounds≥2; keep adapters in memory for trained (do not reload frozen disk weights).
3. Eval **difficulty=2**. Do not train on sealed labels before fresh pass.

## gen5 design intent
New industries **cinema + nursery**. difficulty=2. Burn-on-open via load_gen5_heldout.

## How to run (gen5)
python -m evo heldout --config configs/office_gate3_gen5.yaml
## Learning rule under test (gen4 revision — committed before open)
Highest-EV vs gen2 ceiling (d=1, fresh=1.0) and gen3 floor (d=4, fresh=0):
1. **Eval difficulty = 2** (mid abbreviated prompts; target fresh in (0.6, 0.99) or clear A/B).
2. **Abbreviated curriculum SFT** on DEV packs orders+expenses: cycle difficulties [2,3,4], families table/report/file, dev_items>=12, sft_rounds>=2.
3. **Absorb-then-policy:** fresh pass uses prefer_atoms=true (Epoch-C genome); after SFT, trained pass uses 	rained_prefer_atoms=false so policy absorb can produce Branch A gain.
4. Do **not** train on sealed labels before the fresh pass.

## gen4 design intent
New industries **museum + pharmacy** (not ferry/bakery/library/warehouse/grades/roster). difficulty=2. Burn-on-open via load_gen4_heldout.

## How to run
python -m evo heldout --config configs/office_gate3_gen4.yaml

## Result log
### 2026-10-17 library+warehouse (gen next) — no claim
fresh=1.0 trained=1.0 speed=true transfer=false (ceiling). Measured under **pre-amendment** criteria only → fail. Pack burned. Not eligible for Branch B retroactively.


### 2026-10-17 gen3 ferry+bakery — no claim
- Protocol already amended (a6bb0ed) before open. difficulty=4, prefer_atoms.
- fresh_rate=0.0 · trained_rate=0.0 · speed=false · transfer=false · ceiling=false · heritability=false
- judge.pass=false · gate3_claim=false · pass_branch=null
- Evidence: docs/GATE3_GEN3_JUDGE_2026-10-17.json
- Pack **burned**. Do not retune. Next: change learning rule only, then **gen4** seal.


### 2026-10-17 gen4 museum+pharmacy — no claim
- Pre-seal commit 3bd30e7: abbreviated curriculum SFT + absorb-then-policy; d=2.
- fresh_rate=**0.5** · trained_rate=**0.25** · gain mean=**-0.25**
- speed=false · transfer=false · ceiling=false · heritability=false
- gate3_claim=false · Evidence: docs/GATE3_GEN4_JUDGE_2026-10-17.json
- Learning takeaway: dropping atoms on trained **hurt** vs fresh atoms. Next: keep atoms both sides and/or SFT into atom adapters; gen5 new industries.


### 2026-10-17 gen5 cinema+nursery — no claim
- Pre-seal 8a4979: atoms both + warm atom-adapter abbrev SFT; d=2.
- fresh_rate=**0.5** · trained_rate=**0.5** · gain=0 · speed=**true**
- transfer/ceiling/heritability=false · gate3_claim=false
- Evidence: docs/GATE3_GEN5_JUDGE_2026-10-17.json · pack burned
- Atom SFT loss low but rates unchanged vs fresh. Next: stronger atom lift (more pairs/lr/epochs) or d≈1.5–2 sweet-spot probe on **gen6**.


### 2026-10-17 gen6 harbor+orchard — no claim
- Pre-seal 5530e13: table-overweight atom SFT (dev_items=24, rounds=4, epochs=4, lr=1e-3); atoms both; d=2.
- fresh=trained=**0.5** · family_diag: **table=0.0**, report=1.0, file=1.0 (both passes)
- gain=0 · speed=false · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN6_JUDGE_2026-10-17.json
- Diagnosis: 0.5 floor is **deterministic table-fail**, not coin-flip. Heavy DEV table SFT did not transfer to new industry schemas. Next: schema-randomized DEV table SFT (rebind column names like probe) then **gen7**.


### 2026-10-18 gen7 atelier+foundry — no claim
- Pre-seal 3c9481c: schema-random DEV table SFT n=24 + table overweight; atoms both; d=2.
- fresh=trained=**0.5** · family_diag table=**0** report=1 file=1 · gate3_claim=false · burned
- Evidence: docs/GATE3_GEN7_JUDGE_2026-10-18.json
- Diagnosis: scripted gold passes foreign schema (not CSV/headers/judge). d=2/3 prompts **omit column names** → model must memorize pack lexemes; schema SFT cannot transfer. Proposed fix (pre-gen8): name columns in difficulty<=3 table prompts; keep d>=4 hard.


### 2026-10-18 gen8 marina+greenhouse — no claim (table lift yes)
- Pre-seal d85539f: table d<=3 names columns + schema-random SFT; atoms both; d=2.
- fresh_rate=**0.75** · trained_rate=**1.0** · gain mean=0.25 but CI low=0 (excludes_zero=false)
- family_diag table **0.5→1.0** · report=1 · file=1 · speed=**true**
- gate3_claim=false · burned · Evidence: docs/GATE3_GEN8_JUDGE_2026-10-18.json
- Next: more heldout items / seeds for transfer CI power, or push fresh to ceiling for Branch B; gen9.


### 2026-10-18 gen9 lighthouse+tannery — crash, no claim
- Seal opened; fresh routes completed; crashed in schema SFT: NameError _SCHEMA_WORDS.
- No judge JSON. Pack burned. Do not reopen. Fixed constant → gen10.


### 2026-10-18 gen10 observatory+apiary — **Gate3 CLAIMED (transfer)**
- Pre-seal 3e8ea4 (+ SCHEMA_WORDS). seeds=[0,1,2] n=24. Column fix + atoms + schema SFT.
- fresh=**0.75** trained=**1.0** · table 0.5→1.0 · speed=true
- gain mean=0.25 CI [0.083, 0.417] excludes_zero=true · pass_branch=transfer · gate3_claim=**true**
- Evidence: docs/GATE3_GEN10_JUDGE_2026-10-18.json

## Learning rule under test (gen11 heritability — committed before open)

**Status: PRE_REGISTERED_NOT_OPENED** (2026-10-18T20:26:08+08:00). Evidence: `docs/GATE3_GEN11_HERITABILITY_RULE_2026-10-18.json`.

Planned packs: **archives, kiln**. Branch B target (ceiling/heritability). Seeds=[0,1,2], heldout_items=4, difficulty=2, prefer_atoms fresh, warm atom + schema-random SFT, compose_prefetch=true.

Do **not** open `heldout_seal_gen11` until GPU free and this rule is committed. Opening burns the pair.

