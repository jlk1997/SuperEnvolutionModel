# Office diagnosis — dual never beats agent (2026-10-17)

Gate **0.6** unchanged. Evidence: `runs/office_mid_n_160_s0/.../summary.json` and judge path.

## Symptom

Staged reference papers n=24/80/**160**: judge `ci.mean=0.0`, `excludes_zero=false`, `pass=false`.

## Root causes (falsifiable)

### R1 — Quality ceiling (primary)

With `actor: reference`, `_reply` → `scripted_reply(task.calls)` for **every** arm. Exam rates:

| arm | ok_rate | writes | train_tokens |
| --- | ---: | ---: | ---: |
| agent | **1.0** | 0 | 0 |
| dual | **1.0** | 80 | **0** |
| dual_agent | 1.0 | 80 | 0 |
| others | ≈1.0 | — | 0 |

Paired dual−agent is 1−1=0 on every item → **mean=0 is a ceiling tie**, not proof that dual cannot learn.

**Falsify R1:** Under reference, if agent exam rate drops below dual while dual stays high, mean>0 appears without model weights.

### R2 — Writes do not train under reference

`OrganismSession` learning paths require `actor==model`. dual `writes=80` but `train_tokens=0`. Absorption book updates do not change scripted success.

**Falsify R2:** `actor: model` + write_gate → train_tokens>0 and dual exam moves relative to agent.

### R3 — Cost path also tied

`tokens_per_ok` identical (168) for agent and dual → `close and tokens` branch cannot fire (`dual <= agent/3` fails).

### R4 — Judge silent on non-informative papers

Prior judge returned mean=0 with no `ceiling_tie` / `informative` flag → overnight logs looked like method failure.

## Fixes (priority)

| ID | Fix | Lever | Status |
| --- | --- | --- | --- |
| F1 | `reference_gate: notes_open_book` — agent/dual_agent need retrieval traces; dual keeps scripted (internalization proxy) | Unblocks mean>0 under reference; dissolution-aligned | **IMPLEMENTED** |
| F2 | Judge `ceiling_tie` + `informative` | Stops misreading ceiling as method kill | **IMPLEMENTED** |
| F3 | `actor: model` signal smoke / mid-n | Real Gate2 LM contrast | overnight next |
| F4 | Token accounting so dual post-absorb is cheaper | Cost beat path | later |

## Anti-patterns

- Do **not** lower competence 0.6 or Gate2 Δ thresholds to force a pass.
- Do **not** claim Gate2 from F1 alone (reference proxy ≠ LM dual).
- Do **not** peek Gate3 seals while tuning F3.

## Next measurements

1. Short smoke `office_open_book_smoke` — expect `informative=true`, `ci.mean>0` (reference proxy).
2. Overnight `office_model_signal_smoke` — expect non-ceiling rates; then scale n.
## F1 smoke result (2026-10-17 01:48)

`office_open_book_smoke`: `ci.mean=1.0`, `agent_rate=0`, `dual_rate=1`, `informative=true`, `proxy_beat_agent=true`, `gate2_claim=false`, `pass=false`.

R1 falsified under proxy. Real Gate2 still requires F3 model actor.

## F3 model signal smoke (2026-10-17 02:15)

`office_model_signal_smoke`: `informative=true`, `ceiling_tie=false`, `dual_rate=0`, `agent_rate=0`, exam 0/8 all arms (including oracle). Writes rare; `train_tokens` accounting was 0 (`train_tokens_each` default).

**Interpretation:** LM cannot emit parseable tool calls yet — floor, not dual-vs-agent race. **No Gate2.**

**F3b:** `TOOL_CALL_PRIMER` in `_model_reply`; config `office_model_signal_smoke_v2.yaml` queued.

## F3b/F3c

- F3b primer: still dual=agent=0.
- F3c `practice_bootstrap`: gold scripted on **practice** only for dual/continual/shift when parse fails; exam stays pure model. Logs raw fails to `office_model_turns.log`.


## F3c result (v3)

dual/continual/shift/continual_sft: practice_ok=8/8 via bootstrap; exam 0/8; dual writes=4 train_tokens=6400. agent/oracle/dual_agent practice still 0 (no bootstrap). Judge: informative, dual_rate=agent_rate=0 on exam. **No Gate2.**

## F3d (v4 running)

Omit `tools=` in chat_template when primer on — model was emitting schema JSON fragments instead of XML tool_call.

## F3z — atom adapter key retarget (2026-10-17 17:40)

**Bug:** _model_reply loaded capability policy/adapter_model.safetensors (keys lora_*.policy) into PEFT adapter tom_policy via set_peft_model_state_dict **without renaming keys**. Weight norms unchanged → base/policy behavior; exam stayed 0 while dissolve bare=1.0 (eval uses training adapter name policy).

**Fix:** retarget .policy./.skill2. → .atom_policy./.atom_skill2. before load.

**Smoke (1.5B):** dual exam 3/4; dual+agent both exam 0.75. **No Gate2** (dual ≯ agent).
