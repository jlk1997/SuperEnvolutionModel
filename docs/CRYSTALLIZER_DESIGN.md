# Capability Crystallizer (Epoch B/C.0)

## Goal

Replace “agent + retrieval notes + LLM” with **named capability atoms**: verified successes written into LoRA slots such that **bare** generation clears the same 0.6 gate without scaffold text. Dissolution metric D = max(0, scaffold_rate − bare_rate) → 0.

## Non-goals (this thin slice)

- Multimodal, full office fleet, lowering 0.6, silent fallbacks.

## API

```python
from evo.crystal import crystallize_from_adapter, crystallize_from_pairs, run_ablation

atom = crystallize_from_adapter(
    "add6", "add", "runs/evoplast_adapter",
    bare_rate=1.0, birth=0.0, sites=["mlp"], criterion=0.6,
)
report = run_ablation(prompts, answers, act, grade, criterion=0.6)
# report["internalized"] when bare clears 0.6 and D <= 0.05
```

Atoms live under `runs/capabilities/<name>/` with `capability.json` + adapter files. Index: `runs/capabilities/index.json`.

## Ablation arms

| Arm | Weights | Prompt |
| --- | --- | --- |
| scaffold / retrieval-agent | base or frozen | task + retrieved successful note |
| crystallized bare | capability LoRA | task only |

Success for dissolution: bare_rate ≥ 0.6 and D ≤ 0.05 on held-out prompts.

## Wiring next

1. Promote `evoplast_fit_add` / census mlp adapters via `crystallize_from_adapter`.
2. Office stream: on ledger-approved absorb, call crystallize; nightly ablation job.
3. Product path: capability router selects atoms instead of growing prompt scaffolds.

## Falsifiers

- Bare never reaches 0.6 while scaffold does → not crystallized (keep agent notes).
- Bare ≥ 0.6 but only on train prompts → leak; must use held-out exam odds (same as fit report_x).
