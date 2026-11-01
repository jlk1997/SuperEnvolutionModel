"""GPU C4/C5: SFT an office-family adapter from use-log pairs, then bare vs scaffold.

Criterion 0.6 never lowered. Writes dissolution.json onto the capability atom.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from evo.office.from_use_log import CRITERION, discover_rows, grade_filter, pairs_from_rows


def _repo() -> Path:
    return Path(__file__).resolve().parents[2]


def _heldout_tasks(family: str, n: int, seed0: int = 9000) -> list[dict]:
    from evo.office.families import make_task
    from evo.office.packs import pack_by_name

    pack = pack_by_name("orders")
    tasks = []
    for i in range(n):
        task = make_task(pack, family, seed0 + i, variant=0, difficulty=1)
        task["split"] = "exam"
        tasks.append(task)
    return tasks


def _run_episode_ok(task: dict, reply_fn, workspace: Path, cfg: dict) -> bool:
    from evo.computer.episode import run_episode
    from evo.computer.license import License

    lic = License(
        grants=set(cfg.get("grants") or ["python", "shell", "read", "write", "http"]),
        max_steps=int(cfg.get("max_steps", 6)),
    )
    result = run_episode(task, reply_fn, workspace, lic)
    return bool(result.get("ok"))


def run_dissolve(
    use_log_dir: str | Path,
    family: str = "table",
    *,
    atom_name: str | None = None,
    cfg: dict | None = None,
    heldout_n: int = 4,
    epochs: int = 2,
) -> dict:
    import tempfile

    import torch

    from evo.crystal.ablate import dissolution_score
    from evo.crystal.atom import CapabilityAtom
    from evo.crystal.crystallize import crystallize_from_adapter
    from evo.model import build_model, release
    from evo.registry import require_ready
    from evo.session.learn import commit_pairs

    root = Path(use_log_dir)
    if not root.is_absolute():
        root = _repo() / root
    cfg = dict(cfg or {})
    cfg.setdefault("model_name", "e:/envolution/models/Qwen2.5-1.5B-Instruct")
    cfg.setdefault("lora_rank", 8)
    cfg.setdefault("lora_alpha", 16)
    cfg.setdefault("lora_dropout", 0.0)
    cfg.setdefault("lora_preset", "full")
    cfg.setdefault("max_seq_len", 768)
    cfg.setdefault("max_new_code", 160)
    cfg.setdefault("outer_lr", 5e-4)
    cfg.setdefault("max_steps", 6)
    cfg.setdefault("temperature", 0.0)
    cfg.setdefault("tool_call_primer", True)
    cfg.setdefault("prefer_atoms", False)  # heldout must score the fresh adapter, not a prior atom
    cfg.setdefault("actor", "model")
    require_ready(cfg)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required")

    # Prefer XML tool_call pairs (C4 format-mismatch fix). Fall back to raw traces.
    pairs = []
    pair_source = "raw_trace"
    try:
        from evo.office.use_log_xml import load_xml_pairs, write_xml_use_log

        write_xml_use_log(root, arm="dual", seed=0)
        pairs = load_xml_pairs(root, family, arm="dual", min_n=2)
        pair_source = "events_xml"
    except Exception as exc:
        rows = discover_rows(root, arm="dual")
        graded = grade_filter(rows, family=family, split="practice", ok_only=True)
        if len(graded) < 2:
            return {
                "ok": False,
                "why": f"need >=2 graded {family} pairs, got {len(graded)}; xml_err={exc}",
                "criterion": CRITERION,
            }
        pairs = pairs_from_rows(graded)
        pair_source = f"raw_trace (xml_err={exc})"

    # scaffold notes = first successful trace
    note_blob = "Previously verified workflow:\n" + pairs[0][1][:800] + "\n\nNow solve:\n"

    name = atom_name or f"office_{family}_uselog"
    atom_dir = _repo() / "runs" / "capabilities" / name
    report: dict = {
        "family": family,
        "n_train_pairs": len(pairs),
        "pair_source": pair_source,
        "heldout_n": heldout_n,
        "criterion": CRITERION,
        "gate2_claim": False,
    }

    evo = None
    try:
        evo = build_model(cfg)
        # Qwen2.5 has no DeltaNet day-slot sites that train; use night (delta+mlp) then full fallback.
        from evo.model import LORA_SITES
        from evo.outer_loop import sft_policy

        trained = commit_pairs(evo, pairs, cfg, "slot", phase="night", epochs=int(epochs))
        if not trained.get("wrote"):
            full_sites = list(LORA_SITES.get("attn") or []) + list(LORA_SITES.get("delta") or []) + list(LORA_SITES.get("mlp") or [])
            stats = sft_policy(
                evo,
                pairs,
                float(cfg.get("outer_lr", 5e-4)),
                int(epochs),
                int(cfg.get("max_seq_len", 768)),
                adapter="policy",
                sites=full_sites or None,
            )
            trained = {
                "wrote": int(stats.get("steps") or 0) > 0,
                "sites": list(stats.get("sites") or full_sites),
                "phase": "full_fallback",
                "adapter": "policy",
                "steps": int(stats.get("steps") or 0),
                "kept": False,
                "loss": stats.get("loss"),
            }
        report["train"] = trained
        if not trained.get("wrote"):
            report["ok"] = False
            report["why"] = "SFT wrote nothing (night+full fallback)"
            return report

        # snapshot policy adapter into atom dir
        atom_dir.mkdir(parents=True, exist_ok=True)
        policy_src = Path(getattr(evo, "adapter_dirs", {}).get("policy") or "")
        # peft adapters live on the model; save via evo helpers if present
        saved = False
        if hasattr(evo, "save_adapter"):
            evo.save_adapter("policy", atom_dir / "policy")
            saved = True
        else:
            from evo.model import adapter_state
            from safetensors.torch import save_file

            state = adapter_state(evo.model, "policy")
            pol = atom_dir / "policy"
            pol.mkdir(parents=True, exist_ok=True)
            # flatten tensors
            flat = {k: v.detach().cpu() for k, v in state.items()} if isinstance(state, dict) else {}
            if flat:
                save_file(flat, str(pol / "adapter_model.safetensors"))
                (pol / "adapter_config.json").write_text(
                    json.dumps({"adapter": "policy", "family": family}), encoding="utf-8"
                )
                saved = True
        report["adapter_saved"] = saved

        # Use office XML tool-call actor (same path as F3 stream), not raw generate().
        from evo.office.stream import _model_reply

        tasks = _heldout_tasks(family, heldout_n)
        bare_hits = []
        scaf_hits = []
        for task in tasks:
            with tempfile.TemporaryDirectory() as folder:
                ws = Path(folder)
                bare_task = dict(task)
                bare_reply = _model_reply(evo, cfg, bare_task)
                ok_bare = _run_episode_ok(bare_task, bare_reply, ws, cfg)
                bare_hits.append(ok_bare)
                print(f"[dissolve] bare family={family} id={task.get('id')} ok={ok_bare}", flush=True)

            with tempfile.TemporaryDirectory() as folder:
                ws = Path(folder)
                scaf_task = dict(task)
                scaf_task["prompt"] = note_blob + "\n\n" + task["prompt"]
                scaf_reply = _model_reply(evo, cfg, scaf_task)
                ok_scaf = _run_episode_ok(scaf_task, scaf_reply, ws, cfg)
                scaf_hits.append(ok_scaf)
                print(f"[dissolve] scaffold family={family} id={task.get('id')} ok={ok_scaf}", flush=True)

        bare_rate = sum(bare_hits) / len(bare_hits)
        scaf_rate = sum(scaf_hits) / len(scaf_hits)
        d = dissolution_score(scaf_rate, bare_rate)
        report.update(
            {
                "ok": True,
                "bare_rate": bare_rate,
                "scaffold_rate": scaf_rate,
                "dissolution": d,
                "bare_clears_gate": bare_rate >= CRITERION,
                "bare_hits": bare_hits,
                "scaffold_hits": scaf_hits,
                "internalized": bare_rate >= CRITERION and d <= 0.05,
            }
        )

        atom = crystallize_from_adapter(
            name,
            family,
            atom_dir if saved else atom_dir,
            bare_rate=bare_rate,
            sites=["office", family],
            evidence={"source": "dissolve_uselog", "n_train": len(pairs), "heldout": heldout_n, "dissolution": d, "scaffold_rate": scaf_rate},
            criterion=CRITERION,
        )
        atom.scaffold_rate = scaf_rate
        atom.dissolution = d
        atom.write(atom_dir)
        (atom_dir / "dissolution.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        report["atom"] = atom.name
        report["path"] = str(atom_dir)
    finally:
        if evo is not None:
            release(evo)
    out = root / f"dissolve_{family}_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(out)
    return report


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--use-log", default="runs/use_log/office_use_log_dual_f3i_s0")
    p.add_argument("--family", default="table")
    p.add_argument("--epochs", type=int, default=2)
    p.add_argument("--heldout-n", type=int, default=4)
    args = p.parse_args(argv)
    report = run_dissolve(args.use_log, args.family, epochs=args.epochs, heldout_n=args.heldout_n)
    print(json.dumps(report, indent=2, ensure_ascii=True)[:4000], flush=True)
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
