# Envolution

**Vision:** a use-driven evolutionary model that internalizes skills while it is used, dissolves agent scaffolding over time, and grows multimodal ability from experience — not another thicker agent framework.

## Setup

```text
cd E:\envolution
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Local weights live under `models/`. Primary checkpoint:

`models/Qwen2.5-1.5B-Instruct` (must contain `config.json` + a real `*.safetensors` weight file).

Resolution and fail-fast checks: `evo/registry.py` (`PRIMARY`, `require_ready`). Missing weights raise; there is **no** silent fallback to incomplete Qwen3.5-0.8B.

## Quick commands

```text
# Unit tests (CPU)
python -m evo unit

# LM M0 — addition only (cleared on 1.5B)
python -m evo plast --stage m0 --config configs/evoplast_fit_add.yaml

# LM M0 — stack (addition + hard affine second skill; gate 0.6)
python -m evo plast --stage m0 --config configs/evoplast_fit.yaml
# harder affines + solo second phase:
python -m evo plast --stage m0 --config configs/evoplast_fit_stack_hard.yaml

# Plasticity census dry plan / smoke
python -m evo plast --stage census --config configs/evoplast_census_dry.yaml
python -m evo plast --stage census --config configs/evoplast_census_smoke.yaml

# Studio UI
python -m evo studio
```

Or run `scripts\reproduce_a.ps1`.

## Stage

See [docs/STAGE_ASSESSMENT.md](docs/STAGE_ASSESSMENT.md) and [docs/MASTER_PLAN_V2.md](docs/MASTER_PLAN_V2.md).

## Gates and power

- Roadmap gates: `docs/ROADMAP.md` (GATE1–3 markers)
- Power / n / hours: `docs/POWER_ANALYSIS.md`
- Plasticity paper draft: `docs/PAPER_EVOPLAST.md`
- Runtime recipes: `docs/RUNTIME.md`

**Success fields:** for LM M0 judge `m0.model.passed` / `m0.lm_passed`, not top-level `m0.passed` alone (that is the reference organism).

## Full census (long)

```text
python -m evo plast --stage census --config configs/evoplast_census.yaml
```

3 seeds × {mlp, attn, attn_mlp} × skill — often multi-hour on a 4070 Laptop. Prefer smoke first.

## License / research status

Research codebase. Language-model census numbers are not citable until preregistered papers clear their intervals.
