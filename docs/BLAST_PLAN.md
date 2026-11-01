# BLAST_PLAN — Epoch B→C checkable queue

Updated: 2026-10-17 12:57 Asia/Shanghai

Gate **0.6**. No Gate2 without exam dual_rate > agent_rate and both >0.

## Live status

| Item | State |
| --- | --- |
| v8 | DONE exam dual=agent=0; practice dual 6/8; informative; no Gate2 |
| affine_easy | PASS atom affine23_easy bare=0.75 D=0 |
| v9 F3h | **DONE** exam dual=0 agent=0 practice dual 8/8 writes=4; B-X6 still red |
| F3i C1 | **RUNNING** dual-only use-log (PID gpu_heavy=36304, ~2.9GB VRAM) |
| 2B config | READY configs/office_model_signal_smoke_2b.yaml — not started |
| GPU | single-job; 4070 8GB |

## North star (docs of record)

- Exit B: docs/EPOCH_B_EXIT.md (B-X6 blocker + kill#1 escalate)
- Playbook C: docs/EPOCH_C_PLAYBOOK.md
- Stage %: docs/STAGE_ASSESSMENT.md

## Queue (highest leverage first)

1. ~~v9 F3h~~ DONE — B-X6 still red; escalate to C use-log.
2. **F3i use-log capture (C1)** — dual-only; persist 
uns/use_log/office_use_log_dual_f3i_s0/.
3. C2–C3 crystallize first office-family atom from graded ok pairs (table/file).
4. Optional **2B smoke** after F3i frees GPU — one detached trial; still no Gate2 without dual>agent>0.
5. Epoch D multimodal — blocked until C COMPLETE.

## Kill / discipline

- One heavy GPU job; pid+log under runs/logs/.
- FAST checkpoints: snapshot + detach; do not AwaitShell multi-hour.
- Open-book proxy never Gate2.
- Gate 0.6 never lowered.

## Progress log

- 02:15–09:11 F3 v1–v8: exam floor; practice teachable.
- 08:14 affine_easy PASS.
- 11:11 v9 start → NameError _pick (stream truncated).
- 11:20 stream.py restored; v9 restart; EPOCH_B_EXIT + EPOCH_C_PLAYBOOK landed.
- 12:02 v9 DONE exam 0/0; practice dual 8/8 writes=4.
- 2026-10-17 12:51 F3i started (use_log module + dual-only config); B-X6 kill#1 escalate written; 2B config staged.
- 2026-10-17 12:57 C2/C3 interim from F3i events: office_table_uselog + office_report_uselog notes_only (bare=null); F3i still alive step~9.
- 2026-10-17 13:31 F3i DONE 8/8; C3 notes atoms; C4 table bare=0 x2; **2B smoke ALIVE** (B-X6 escalate).
- 2026-10-17 13:48 2B DONE exam dual=agent=0 practice dual 2/8 → **kill#2**; freeze office exam; C4 v3 XML dissolve started (gpu_heavy=18808).
- 2026-10-17 13:59 C4 v3 XML still bare=0; started **F3j** dual grow steps=32 (gpu_heavy=26276).
- 2026-10-17 14:51 **C4/C5 table PASS** bare=1.0 D=0 (merged XML n=7). Start report dissolve v6. Exam stays frozen.
- 2026-10-17 15:01 **report C4/C5 PASS** bare=1.0 D=0 (merged n=12). Started **file v7** dissolve.
- 2026-10-17 15:12 **file C4/C5 PASS** bare=1.0 D=0. Triple family clear. Start C6 router atom smoke (not exam).
- 2026-10-17 15:29 **C6b PASS** 8/8 _route_generate; **Epoch C product-path COMPLETE**. B still partial. Start shell grow; D preview doc only.
- 2026-10-17 15:44 shell grow seed2: shell ok=0; hardening tests+reproduce_c; **shell-only enrich** started.
- 2026-10-17 15:58 shell_only 0/32 ok; reference shell 4/4 → **SHELL LM KILL**. Hardening reproduce OK. GPU idle.

- 2026-10-18 ~11:43 Asia/Shanghai **Gate2 mid-n observational DONE** (RESTART n=16 dual/agent). dual=**0.8125** agent=**0.125** CI n=16 mean=0.6875 [0.4375, 0.875] excludes_zero; gate2_claim=false; above_schedules N/A (narrowed arms). Evidence: docs/GATE2_MID_N_OBSERVATIONAL_2026-10-18.json. Prior Gate2 claim stands.
- 2026-10-18 shadow/auto/external_scaffold CPU DONE. Next: wire one local external bench if dataset on disk; else stubs. D deferred (no VL).
- 2026-10-18 ~18:46 Asia/Shanghai **external scaffold all-four wire DONE** (CPU). serve_learn/evo_arena/path_bench local toys smoke rate=1.0 n_eval=4; upstream_claim=false. Evidence: docs/EXTERNAL_SCAFFOLD_2026-10-18.json. Fleet frozen. D deferred (no VL).
- 2026-10-18 ~18:50 Asia/Shanghai **external 1.5B bare observational** serve_learn=0.5 evo_arena=0.25 path_bench=0.5 all_pass_gate=False; upstream_claim=false. docs/EXTERNAL_LOCAL_MODEL_SCORE_2026-10-18.json

- 2026-10-18 ~19:04 Asia/Shanghai **external honest train-only SFT** serve 0.5→1.0 arena 0.25→0.75 path 0.5→1.0 all_pass_gate_trained=True honest_splits=True upstream_claim=false. docs/EXTERNAL_LOCAL_SFT_SCORE_2026-10-18.json. Studio hygiene synced to ROADMAP G2/G3 pass. Non-VL knives closed → OPEN_ONLY_VL / IDLE_WAITING_VL.
