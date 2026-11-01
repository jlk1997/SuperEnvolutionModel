# Overnight queue (Epoch A → Gates)

ETAs are order-of-magnitude on RTX 4070 Laptop (8GB). Prefer one job at a time. **Do not lower competence 0.6.**

## Already green (do not redo unless regressing)

| Job | Command | Result |
| --- | --- | --- |
| Unit | `python -m evo unit` | 123 OK |
| LM M0 add | `python -m evo plast --stage m0 --config configs/evoplast_fit_add.yaml` | `m0.model.passed=true` |
| Census smoke | `python -m evo plast --stage census --config configs/evoplast_census_smoke.yaml` | 1/1 mlp×add |
| Census dry | `python -m evo plast --stage census --config configs/evoplast_census_dry.yaml` | 9-cell plan |

## Overnight-friendly (finish before morning)

### A. Plasticity census add×sites×seeds (~1–3 h)

```text
python -m evo plast --stage census --config configs/evoplast_census_add.yaml
```

3 seeds × {mlp, attn, attn_mlp} × skill=add. Logs: `runs/evoplast_census_add.json`.

### B. Office mid-power probe (~4–12 h, Gate 2 prep)

Raise exam budget toward n≈160 (Δ≈0.20) before jumping to n≈800:

```text
python -m evo office --config configs/office_census.yaml
```

After smoke is green, edit `day_ticks` / exam counts upward; see `docs/POWER_ANALYSIS.md`.

### C. Stream confirmation on 1.5B (~2–6 h, Gate 1 prep)

```text
python -m evo stream --config configs/stream_census.yaml
```

Retarget `model_name` to 1.5B (field `model_name_confirm`) before claiming Gate 1.

## Weekend / multi-night (do not start casually)

| Job | Why | ETA |
| --- | --- | --- |
| Gate 2 n≈800 × 3 seeds | Tiny Δ power 0.8 | ~24–48 h |
| Full `evoplast_census.yaml` stack cells | Second skill still failing on MLP | multi-hour + likely fails |
| `evoplast_fit_stack_attn.yaml` | Capacity experiment | ~30–90 min once |

## Start policy

1. Smokes green → start **one** overnight-friendly job (prefer A).
2. Capture stdout to `runs/<name>_overnight.log`.
3. Morning: read JSON `passed` / judge blocks; do not peek Gate 3 seals while tuning.
