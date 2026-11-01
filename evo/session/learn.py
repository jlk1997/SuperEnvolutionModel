"""Commit a verified batch into an adapter. Reference runs pass evo=None and only record the decision."""

from __future__ import annotations

from evo.session.sites import sites_for


def commit_pairs(
    evo,
    pairs: list[tuple[str, str]],
    cfg: dict,
    dest: str,
    phase: str = "day",
    adapter: str | None = None,
    sites: list[str] | None = None,
    epochs: int = 1,
) -> dict:
    chosen_sites = [] if dest in {"drop", "retrieval", "fast"} else list(sites or sites_for(phase, dest))
    chosen = adapter or ("memory" if dest == "core" else "policy")
    info = {"wrote": False, "sites": chosen_sites, "phase": phase, "adapter": chosen, "steps": 0, "kept": False}
    if evo is None or not pairs or not chosen_sites:
        return info
    from evo.outer_loop import sft_policy

    cleaned = [(prompt, code) for prompt, code in pairs if str(code).strip()]
    if not cleaned:
        return info
    stats = sft_policy(
        evo,
        cleaned,
        float(cfg.get("outer_lr", 5e-4)),
        int(epochs),
        int(cfg.get("max_seq_len", 384)),
        adapter=chosen,
        sites=chosen_sites,
    )
    info["steps"] = int(stats.get("steps") or 0)
    info["wrote"] = info["steps"] > 0
    return info


def commit_shadow(evo, pairs, cfg: dict, dest: str, phase: str, live: str, ablation, train=None, sites: list[str] | None = None, epochs: int = 1) -> dict:
    """Train `cand`. Copy it onto `live` only when the bare attempt passes and the optimizer stepped.

    `train(adapter) -> {steps}` lets a test skip the real optimizer. A missing model never counts as a pass.
    """
    chosen_sites = [] if dest in {"drop", "retrieval", "fast"} else list(sites or sites_for(phase, dest))
    info = {"wrote": False, "kept": False, "sites": chosen_sites, "phase": phase, "adapter": live, "steps": 0, "why": ""}
    if evo is None:
        info["why"] = "reference is not the model"
        return info
    if not pairs or not chosen_sites:
        info["why"] = "nothing to train"
        return info
    snap = evo.snapshot(live)
    try:
        if train is None:
            from evo.model import adapter_state, add_named_adapter, load_adapter_state

            add_named_adapter(evo, "cand")
            load_adapter_state(evo.model, "cand", adapter_state(evo.model, live))
            trained = commit_pairs(evo, pairs, cfg, dest, phase, adapter="cand", sites=chosen_sites, epochs=epochs)
        else:
            trained = train("cand") or {}
        steps = int(trained.get("steps") or 0)
        info["steps"] = steps
        passed = steps > 0 and bool(ablation("cand"))
        if passed:
            if train is None:
                from evo.model import adapter_state, load_adapter_state

                load_adapter_state(evo.model, live, adapter_state(evo.model, "cand"))
            elif hasattr(evo, "promote"):
                evo.promote()
            info["wrote"] = True
            info["kept"] = True
            info["why"] = "ablation passed"
            return info
        evo.restore(live, snap)
        info["why"] = "ablation missed" if steps else "optimizer did not step"
        return info
    except Exception:
        evo.restore(live, snap)
        raise
