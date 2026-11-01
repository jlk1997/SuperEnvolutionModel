# Power analysis for Gates 1–3 (Epoch A-4)

Preregistered effect sizes and paper sizes for the office / stream gates.
**Do not lower competence gates (0.6) to buy power.** Buy items and seeds instead.

Computed with `evo.stats.power_paired` / `evo.office.judge.exam_size_for_power`
(80 sims × 80 alpha boots unless noted).

## What the roadmaps already recorded

| Gate | Status (prior runs) | Observed | n | Note |
| --- | --- | --- | --- | --- |
| Gate 1 (stream / continual write) | not passed | mean 0.0, CI [0.0, 0.0] | 24 | Learning writes did not beat agent on that paper |
| Gate 2 (office dual vs agent) | not passed | mean ~0.17, CI [0.0, 0.5] | 6 | Underpowered; roadmap asked ~800 items for power 0.8 at Δ≈0.05–0.10 |
| Gate 3 (held-out transfer) | not passed | mean 0.0, CI [0.0, 0.0] | 4 | Seal path; need larger transfer paper |

## Effect-size targets (preregister)

| Contrast | p_new | p_base | Δ | Power target | Smallest n (sim) |
| --- | ---: | ---: | ---: | ---: | --- |
| Gate2 dual>agent (tiny) | 0.55 | 0.45 | 0.10 | 0.80 | **n≈800–1200** (candidate list in judge tops out at 240 → power≈0.44; extend paper) |
| Gate2 dual>agent (mid) | 0.65 | 0.45 | 0.20 | 0.80 | **n≈160** (`exam_size_for_power`) |
| Acceleration (plast LM) | 0.75 | 0.45 | 0.30 | 0.80 | **n≈60 families** (`families_for_power`) |

### Simulated power grid (excerpt)

| label | n | p_new | p_base | power |
| --- | ---: | ---: | ---: | ---: |
| gate2_small_delta | 6 | 0.55 | 0.45 | 0.062 |
| gate2_mid | 6 | 0.65 | 0.45 | 0.15 |
| accel_reg | 6 | 0.75 | 0.45 | 0.275 |
| gate3_transfer_tiny | 6 | 0.35 | 0.25 | 0.025 |
| gate2_small_delta | 24 | 0.55 | 0.45 | 0.087 |
| gate2_mid | 24 | 0.65 | 0.45 | 0.263 |
| accel_reg | 24 | 0.75 | 0.45 | 0.588 |
| gate3_transfer_tiny | 24 | 0.35 | 0.25 | 0.075 |
| gate2_small_delta | 48 | 0.55 | 0.45 | 0.087 |
| gate2_mid | 48 | 0.65 | 0.45 | 0.438 |
| accel_reg | 48 | 0.75 | 0.45 | 0.85 |
| gate3_transfer_tiny | 48 | 0.35 | 0.25 | 0.1 |
| gate2_small_delta | 100 | 0.55 | 0.45 | 0.212 |
| gate2_mid | 100 | 0.65 | 0.45 | 0.787 |
| accel_reg | 100 | 0.75 | 0.45 | 0.975 |
| gate3_transfer_tiny | 100 | 0.35 | 0.25 | 0.287 |
| gate2_small_delta | 200 | 0.55 | 0.45 | 0.425 |
| gate2_mid | 200 | 0.65 | 0.45 | 0.938 |
| accel_reg | 200 | 0.75 | 0.45 | 1.0 |
| gate3_transfer_tiny | 200 | 0.35 | 0.25 | 0.512 |
| gate2_small_delta | 400 | 0.55 | 0.45 | 0.762 |
| gate2_mid | 400 | 0.65 | 0.45 | 1.0 |
| accel_reg | 400 | 0.75 | 0.45 | 1.0 |
| gate3_transfer_tiny | 400 | 0.35 | 0.25 | 0.85 |
| gate2_small_delta | 800 | 0.55 | 0.45 | 0.963 |
| gate2_mid | 800 | 0.65 | 0.45 | 1.0 |
| accel_reg | 800 | 0.75 | 0.45 | 1.0 |
| gate3_transfer_tiny | 800 | 0.35 | 0.25 | 1.0 |

## Seeds

- **Minimum publishable:** seeds `[0, 1, 2]` (already in census YAMLs).
- Report the **paired** dual−agent (or continual−agent) mean with bootstrap CI pooled across seeds, or per-seed then meta.
- Do **not** peek at held-out Gate 3 packs while tuning Gate 1–2.

## Hours on RTX 4070 Laptop (order-of-magnitude)

Assumes ~15–25s per office exam item with 1.5B 4-bit LoRA; training arms multiply wall time.

| Job | Estimate |
| --- | --- |
| `office_smoke` (reference) | minutes |
| Current `office_census` (small n) | ~1-3h (underpowered) — **underpowered for Gate 2** |
| Gate 2 paper n≈800 × 3 seeds (exam-only lower bound) | ~13.3 h |
| Gate 2 full with training arms | ~24-48h (train+exam+arms) |
| `stream_census` on 0.5B | ~2-6h |
| Full `evoplast_census` 3×3×stack | ~1.5-3h (stack cells longer) |

**Overnight policy:** only start jobs whose expected wall time is known; prefer `*_smoke` then scale `exam_tasks` / `heldout_items` / `power_target_n`.

## YAML fields (patched into census configs)

```yaml
# Power / paper size (A-4)
power_target: 0.8
power_p_new: 0.55          # expected dual/continual success
power_p_base: 0.45         # expected agent baseline
power_min_n: 24            # never publish below this even if smoke passes
power_required_n: 800      # Gate 2 preregistered size at tiny Δ; raise exam budget toward this
seeds: [0, 1, 2]
```

Stream Gate 1 keeps a smaller first paper but must **state** it is exploratory until `power_required_n` is met on 1.5B confirmation.

## Commands (do not auto-start >48h here)

```text
python -m evo office --config configs/office_smoke.yaml
python -m evo office --config configs/office_census.yaml
python -m evo stream --config configs/stream_smoke.yaml
python -m evo stream --config configs/stream_census.yaml
```

Raise `exam_tasks` / day budgets toward `power_required_n` only after smoke is green.

## Extended tiny-Δ (0.55 vs 0.45) beyond judge candidates

| n | power |
| ---: | ---: |
| 400 | 0.762 |
| 600 | 0.875 |
| 800 | 0.963 |
| 1200 | 1.0 |

Gate 2 preregister: **n≥800** items pooled across seeds when expecting only +0.10 over agent.
