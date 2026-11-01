"""Turn a genome into per-site learning rates and module names.

The reference organism and the LoRA trainer read the same map. A site whose
rate falls under the floor is not trained on that step.
"""

from __future__ import annotations

from evo.evolution.genome import SITES, Genome
from evo.model import LORA_SITES


FLOOR = 1e-4
# Above this, 4-bit LoRA on a 0.8B/2B base overshoots a one-token answer.
CAP = 8e-4


def optimizer_lr(genome: Genome, site: str) -> float:
    """AdamW step for one site, from the mid-timescale row of the plasticity map."""
    strength = genome.site_strength(site, "mid")
    mix = 0.3 + 0.7 * genome.unit("mem.mid_mix")
    return min(CAP, (10 ** (-5.0 + 3.0 * strength)) * mix)


def planned_writes(genome: Genome, floor: float = FLOOR) -> list[dict]:
    rows = []
    for site in SITES:
        rate = optimizer_lr(genome, site)
        if rate < floor:
            continue
        rows.append({"site": site, "modules": list(LORA_SITES[site]), "lr": rate})
    # MLP first. On this base it is the write that actually moves the loss.
    rows.sort(key=lambda row: {"mlp": 0, "delta": 1, "attn": 2}[row["site"]])
    return rows


def apply_planned_updates(evo, pairs: list[tuple[str, str]], genome: Genome, cfg: dict, epochs: int | None = None) -> dict:
    """One supervised pass per live site. Empty pairs do not touch the optimizer."""
    from evo.outer_loop import sft_policy

    plan = planned_writes(genome)
    keep = cfg.get("fit_sites")
    if keep:
        keep_set = set(keep)
        have = {row["site"] for row in plan}
        for site in keep_set:
            if site not in have and site in LORA_SITES:
                # Honor explicit fit_sites even when the hand genome rates attn/delta under the floor.
                plan.append({"site": site, "modules": list(LORA_SITES[site]), "lr": CAP})
        plan = [row for row in plan if row["site"] in keep_set]
    steps = 0
    used = []
    if not pairs:
        return {"steps": 0, "sites": [], "plan": plan}
    for row in plan:
        stats = sft_policy(
            evo,
            pairs,
            float(row["lr"]),
            int(cfg.get("fit_epochs", 1) if epochs is None else epochs),
            int(cfg.get("max_seq_len", 384)),
            adapter=str(cfg.get("adapter", "policy")),
            sites=list(row["modules"]),
        )
        steps += int(stats.get("steps") or 0)
        if int(stats.get("steps") or 0):
            used.append(row["site"])
    return {"steps": steps, "sites": used, "plan": plan}
