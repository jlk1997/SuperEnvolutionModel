# Census_add interpretation (2026-10-16 23:43 CST)

Source: `runs/evoplast_census_add.json` (wall ~429.6s).  
Skill=`add`, gate competence **0.6**, base Qwen2.5-1.5B 4-bit.  
Strict `passed` for all 9 cells is **False** (6/9). The **scientific pattern** is stronger than the boolean.

## Seed × site matrix (passed / add_kept)

| seed | mlp | attn | attn_mlp |
| ---: | --- | --- | --- |
| 0 | True / 1.0 | False / 0.0 | True / 1.0 |
| 1 | True / 1.0 | False / 0.0 | True / 1.0 |
| 2 | True / 0.75 | False / 0.0 | True / 1.0 |

## Claims (falsifiable)

1. **MLP is sufficient** for within-life addition on this base: **3/3 seeds** pass with mlp-only.
2. **Attention-only is insufficient**: **0/3** pass (`add_rate=0` every seed).
3. **Attn+MLP matches MLP**: **3/3** pass — attention does not block when MLP is present; it is not the carrier alone.

This is early support for a **site-specific plasticity map** on an LM (Nature P0 flavor), still short of evolved genomes / AR papers.

## Non-claims

- Not stack M0; not Gate1/2; not dissolution; not multimodal.
- Overall census `passed=false` because attn cells fail by design of the sweep — do not “fix” by dropping attn from the matrix; report the pattern.

## Next

- `stack_attn` (attn+mlp LoRA) for second-skill report≥0.6 without lowering gate.
- Optional: evolve site allocation genes using census fitness = mlp_pass − λ·attn_only_waste.
