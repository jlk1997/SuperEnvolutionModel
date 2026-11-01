# Master plan V2 闂?after Epoch A / into Epoch B (2026-10-17)

Elevates the long-term plan from 闂佺偨鍎茬粭姊恔e Epoch A reproducible闂?to **falsifiable innovation**. Competence gate **0.6** never lowered.

## North star (unchanged)

Use-driven evolutionary model: experience 闂?internalized skill 闂?dissolve scaffolds 闂?induce new modalities.

## What Epoch A proved

- [x] Registry fail-fast on PRIMARY 1.5B
- [x] LM M0 **add** passes
- [x] Census + power docs + gate smokes (engineering)
- [x] Local git history; overnight queue

## Epoch B board (checkboxes)

### B.1 Plasticity map

| ID | Experiment | Status |
| --- | --- | --- |
| B1a | `evoplast_census_add` 3闁?闁煎鐗慸d site map | [x] mlp闂?attn闂?attn_mlp闂?(6/9) 闂?`CENSUS_ADD_INTERPRETATION.md` |
| B1b | Stack second skill report闂?.6 | [x] **CLEARED** via H-holdout offset (`evoplast_fit_stack_holdout`, birth=0 report=1.0 add_kept=1.0) |
| B1b闂?| Affine / transfer second skill | [x] **CLEARED** easy curriculum `affine_easy` second_report=0.75 (`affine23_easy` D=0) |
| B1c | Census interpretation doc | [x] |

### B.2 Gate power

| ID | Experiment | Status |
| --- | --- | --- |
| B2a | Stream 1.5B confirm | [ ] |
| B2b | Office mid-闁?toward n闂?60 | [~] n=24 fail; n闂?0/160 staged (`office_mid_n_80` / `_160`); **do not claim Gate2 early** |
| B2c | No Gate3 peek | [x] process |

### C.0 Crystallizer thin

| ID | Item | Status |
| --- | --- | --- |
| C0a | Capability atoms + dissolve API | [x] |
| C0b | Multi-atom D=0 (GPU) | [x] add6_mlp, add6_census_mlp_s0, offset47_holdout |
| C0c | Router prefers atoms over notes | [x] `evo.crystal.router` |
| C0d | Router wired into office act (`_notes`) | [x] strip notes when family_skill_map / skill matches internalized atom |
| C0e | Use-log 闂?crystallize production loop | [ ] |
| C0f | Router default in model office/stream generate | [ ] partial (notes path only) |

## Exit criteria 闂?闂佸憡甯楃粙鎺楀蓟婵犲嫮鐜绘俊銈傚亾鐟?OPEN

1. [x] Census site pattern across seeds  
2. [x] Stack clears report闂?.6 on 1.5B (holdout)  
3. [ ] Gate1/Gate2 CI excludes 0 at power-adequate n  
4. [x] Crystallizer: bare exam闂?.6 with D闂? (multi-atom)

Until Gate2 power clears: window stays **PARTIAL**.

## Compute policy

One heavy GPU job at a time; office reference chunks may run when GPU free; log under `runs/logs/`.
