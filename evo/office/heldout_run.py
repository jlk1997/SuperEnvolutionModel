"""Open a sealed pack once, run it, and score transfer against a fresh pass."""

from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path

from evo.computer.episode import run_episode, scripted_reply
from evo.computer.license import License
from evo.office.families import FAMILIES, make_task
from evo.office.judge import judge_transfer, touches_to_rate, write_gate
from evo.office.seal import (
    load_heldout,
    load_next_heldout,
    load_gen3_heldout,
    load_gen4_heldout,
    load_gen5_heldout,
    load_gen6_heldout,
    load_gen7_heldout,
    load_gen8_heldout,
    load_gen9_heldout,
    load_gen10_heldout,
    load_gen11_heldout,
)
from evo.util import repo_path


def run_heldout(cfg: dict, evo=None) -> dict:
    generation = str(cfg.get("heldout_generation") or "first").lower()
    if generation in ("gen10", "10", "observatory"):
        default_seal = "runs/heldout_seal_gen10.json"
    elif generation in ("gen9", "9", "lighthouse"):
        default_seal = "runs/heldout_seal_gen9.json"
    elif generation in ("gen8", "8", "marina"):
        default_seal = "runs/heldout_seal_gen8.json"
    elif generation in ("gen7", "7", "atelier"):
        default_seal = "runs/heldout_seal_gen7.json"
    elif generation in ("gen6", "6", "harbor"):
        default_seal = "runs/heldout_seal_gen6.json"
    elif generation in ("gen5", "5", "cinema"):
        default_seal = "runs/heldout_seal_gen5.json"
    elif generation in ("gen4", "4", "museum"):
        default_seal = "runs/heldout_seal_gen4.json"
    elif generation in ("gen3", "3", "ferry"):
        default_seal = "runs/heldout_seal_gen3.json"
    elif generation in ("next", "2", "library"):
        default_seal = "runs/heldout_seal_next.json"
    else:
        default_seal = "runs/heldout_seal.json"
    record = repo_path(cfg.get("seal_path", default_seal))
    reason = str(cfg.get("reason") or "")
    open_flag = bool(cfg.get("open_heldout", True))
    if generation in ("gen11", "11", "archives"):
        packs = load_gen11_heldout(open_flag, reason, record)
    elif generation in ("gen10", "10", "observatory"):
        packs = load_gen10_heldout(open_flag, reason, record)
    elif generation in ("gen9", "9", "lighthouse"):
        packs = load_gen9_heldout(open_flag, reason, record)
    elif generation in ("gen8", "8", "marina"):
        packs = load_gen8_heldout(open_flag, reason, record)
    elif generation in ("gen7", "7", "atelier"):
        packs = load_gen7_heldout(open_flag, reason, record)
    elif generation in ("gen6", "6", "harbor"):
        packs = load_gen6_heldout(open_flag, reason, record)
    elif generation in ("gen5", "5", "cinema"):
        packs = load_gen5_heldout(open_flag, reason, record)
    elif generation in ("gen4", "4", "museum"):
        packs = load_gen4_heldout(open_flag, reason, record)
    elif generation in ("gen3", "3", "ferry"):
        packs = load_gen3_heldout(open_flag, reason, record)
    elif generation in ("next", "2", "library"):
        packs = load_next_heldout(open_flag, reason, record)
    else:
        packs = load_heldout(open_flag, reason, record)
    n = int(cfg.get("heldout_items", 4))
    difficulty = int(cfg.get("difficulty", 1))
    if evo is None or cfg.get("actor", "reference") != "model":
        flags = []
        for pack in packs:
            flags.extend(_reference_flags(pack, n, difficulty))
        judged = judge_transfer(flags, flags, touches_to_rate(flags), touches_to_rate(flags))
        judged["measured"] = False
        judged["branch"] = "Reference actor only. This opened the seal but it is not a transfer measurement."
        judged["pass"] = False
        judged["gate3_claim"] = False
        payload = {"packs": [pack["name"] for pack in packs], "judge": judged, "flags": flags}
    else:
        payload = _model_transfer(evo, packs, cfg)
        judged = payload["judge"]
    if cfg.get("write_gate"):
        write_gate(judged, [{"seed": cfg.get("seed", 0)}], marker="GATE3")
    evidence = repo_path(cfg.get("evidence_path") or "runs/office_gate3_judge.json")
    evidence.parent.mkdir(parents=True, exist_ok=True)
    payload["seal"] = str(record)
    payload["evidence"] = str(evidence)
    payload["heldout_generation"] = generation
    evidence.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return payload


def _reference_flags(pack: dict, n: int, difficulty: int) -> list[float]:
    flags = []
    license = License(grants={"python", "shell", "read", "write", "http"}, max_steps=8, timeout=8)
    for index in range(n):
        family = FAMILIES[index % len(FAMILIES)]
        variant = 0 if family in ("shell", "http", "mixed") else index % 2
        task = make_task(pack, family, 3000 + index, variant=variant, difficulty=difficulty)
        with tempfile.TemporaryDirectory(prefix="evo-held-") as folder:
            result = run_episode(task, scripted_reply(task["calls"]), Path(folder), license)
        flags.append(1.0 if result["ok"] else 0.0)
    return flags



def _model_transfer(evo, packs: list[dict], cfg: dict) -> dict:
    """Fresh (atoms) across seeds → one absorb SFT → trained (warm atoms) across seeds.

    Multiple seeds concatenate flags so transfer CI can exclude 0 when gain holds (~0.25).
    """
    from evo.office.packs import pack_by_name

    n = int(cfg.get("heldout_items", 4))
    seeds = list(cfg.get("seeds") or [int(cfg.get("seed", 0))])
    eval_cfg = dict(cfg)
    eval_cfg["prefer_atoms"] = True

    fresh_all: list[float] = []
    fresh_by_seed: list[dict] = []
    for seed in seeds:
        seed_cfg = dict(eval_cfg)
        seed_cfg["seed"] = int(seed)
        flags = _model_flags(evo, packs, n, seed_cfg, warm=None, seed_offset=int(seed) * 10007)
        fresh_all.extend(flags)
        fresh_by_seed.append({"seed": int(seed), "flags": flags, "rate": sum(flags) / len(flags) if flags else None})

    pairs = _dev_pairs_curriculum(cfg)
    if bool(cfg.get("schema_random_table_sft", True)):
        schema_pairs = _schema_random_table_pairs(cfg)
        tagged = list(cfg.get("_tagged_pairs") or [])
        tagged.extend(("table", pair) for pair in schema_pairs)
        cfg["_tagged_pairs"] = tagged
        pairs = pairs + schema_pairs

    warm = None
    atom_sft_stats = {}
    if bool(cfg.get("atom_adapter_sft", True)) and pairs:
        warm, atom_sft_stats = _sft_into_atom_adapters(evo, pairs, cfg)

    orders = pack_by_name("orders")
    # DEV exam once on warm atoms (speed reference)
    dev_exam = _model_flags(
        evo, [orders], max(2, int(cfg.get("dev_exam_items", 6))), eval_cfg, warm=warm, seed_offset=0
    )

    trained_all: list[float] = []
    trained_by_seed: list[dict] = []
    for seed in seeds:
        seed_cfg = dict(eval_cfg)
        seed_cfg["seed"] = int(seed)
        flags = _model_flags(evo, packs, n, seed_cfg, warm=warm, seed_offset=int(seed) * 10007)
        trained_all.extend(flags)
        trained_by_seed.append({"seed": int(seed), "flags": flags, "rate": sum(flags) / len(flags) if flags else None})

    families = list(cfg.get("families") or ["table", "report", "file"])
    n_per = n
    fam_diag = {}
    for label, flags in (("fresh", fresh_all), ("trained", trained_all)):
        by = {f: [] for f in families}
        for i, flag in enumerate(flags):
            by[families[(i % n_per) % len(families)]].append(float(flag))
        fam_diag[label] = {f: (sum(v) / len(v) if v else None) for f, v in by.items()}

    dev_touches = touches_to_rate([bool(f) for f in dev_exam], rate=0.8, window=1)
    held_touches = touches_to_rate([bool(f) for f in trained_all], rate=0.8, window=1)
    judged = judge_transfer(trained_all, fresh_all, dev_touches, held_touches)
    judged["measured"] = True
    judged["fresh_rate"] = sum(fresh_all) / len(fresh_all) if fresh_all else None
    judged["trained_rate"] = sum(trained_all) / len(trained_all) if trained_all else None
    judged["dev_touches"] = dev_touches
    judged["held_touches"] = held_touches
    judged["family_diag"] = fam_diag
    judged["seeds"] = seeds
    judged["learning_rule"] = {
        "prefer_atoms_both": True,
        "atom_adapter_sft": bool(cfg.get("atom_adapter_sft", True)),
        "schema_random_table_sft": bool(cfg.get("schema_random_table_sft", True)),
        "schema_random_n": int(cfg.get("schema_random_n", 16)),
        "multi_seed": seeds,
        "heldout_items": n,
        "n_flags": len(fresh_all),
        "table_overweight": True,
        "dev_difficulties": list(cfg.get("dev_difficulties") or [2, 3]),
        "dev_items": int(cfg.get("dev_items", 24)),
        "sft_rounds": int(cfg.get("sft_rounds", 4)),
        "sft_epochs": int(cfg.get("sft_epochs", 4)),
        "atom_sft_lr": float(cfg.get("atom_sft_lr") or cfg.get("outer_lr") or 5e-4),
        "eval_difficulty": int(cfg.get("difficulty", 2)),
        "atom_sft": atom_sft_stats,
        "warm_adapters": list((warm or {}).keys()),
        "column_names_d_le_3": True,
    }
    return {
        "packs": [pack["name"] for pack in packs],
        "fresh": fresh_all,
        "trained": trained_all,
        "fresh_by_seed": fresh_by_seed,
        "trained_by_seed": trained_by_seed,
        "dev_exam": dev_exam,
        "judge": judged,
        "dev_pairs": len(pairs),
        "family_diag": fam_diag,
        "seeds": seeds,
    }




_SCHEMA_WORDS = (
    "alpha", "bravo", "coral", "delta", "ember", "flint", "gamma", "helix",
    "ivory", "jade", "kilo", "lunar", "mica", "nova", "onyx", "prism",
    "quartz", "ridge", "satin", "timber", "umbra", "vapor", "willow", "xenon",
    "yarrow", "zephyr", "cedar", "drift", "fjord", "glade", "haven", "inlet",
)


def _schema_random_table_pairs(cfg: dict) -> list[tuple[str, str]]:
    """DEV-only probe-style column rebind: random synthetic packs → table (prompt, code).

    Never imports sealed packs. Teaches column-agnostic DictReader ops for Branch lift.
    """
    from evo.computer.actions import format_call
    from evo.office.packs import _pack

    n = int(cfg.get("schema_random_n", 16))
    difficulties = [int(x) for x in (cfg.get("schema_random_difficulties") or cfg.get("dev_difficulties") or [1, 2, 3])]
    seed0 = int(cfg.get("seed", 0)) + 77000
    rng = random.Random(seed0)
    pairs: list[tuple[str, str]] = []
    for index in range(n):
        # Unique field tokens within one pack
        fields = rng.sample(_SCHEMA_WORDS, 6)
        pack = _pack(
            f"synth_{index}",
            fields[0],  # record
            fields[1],  # amount
            fields[2],  # status
            fields[3],  # ok
            fields[4],  # date
            fields[5] + "_id",  # id_field
        )
        difficulty = difficulties[index % len(difficulties)]
        variant = index % 3
        task = make_task(pack, "table", seed0 + index, variant=variant, difficulty=difficulty)
        text = "\n".join(format_call(call.name, call.arguments) for call in task["calls"])
        pairs.append((task["prompt"], text))
    print(f"[heldout] schema_random_table_pairs n={len(pairs)} difficulties={difficulties}", flush=True)
    return pairs


def _sft_into_atom_adapters(evo, pairs: list[tuple[str, str]], cfg: dict) -> tuple[dict, dict]:
    """Load office atoms into named adapters, SFT abbreviated/schema pairs in-place, keep warm."""
    from evo.crystal.router import route
    from evo.outer_loop import sft_policy
    from evo.model import add_named_adapter
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file

    skills = list(cfg.get("dev_families") or cfg.get("families") or ["table", "report", "file"])
    warm: dict[str, str] = {}
    stats: dict[str, dict] = {}
    rounds = max(1, int(cfg.get("sft_rounds", 4)))
    epochs = max(1, int(cfg.get("sft_epochs", 4)))
    lr = float(cfg.get("atom_sft_lr") or cfg.get("outer_lr") or 5e-4)
    max_len = int(cfg.get("max_seq_len", 512))

    tagged = list(cfg.get("_tagged_pairs") or [])
    if not tagged:
        families = list(cfg.get("dev_families") or ["table", "report", "file"])
        tagged = [(families[i % len(families)], pair) for i, pair in enumerate(pairs)]

    for skill in skills:
        decision = route(skill, notes=None, prefer_atom=True)
        if decision.get("mode") != "atom":
            continue
        atom_dir = Path(str(decision.get("adapter_dir") or ""))
        weight = atom_dir / "policy" / "adapter_model.safetensors"
        src_name = "policy"
        if not weight.is_file():
            weight = atom_dir / "skill2" / "adapter_model.safetensors"
            src_name = "skill2"
        if not weight.is_file():
            continue
        adapter = f"atom_{skill}"
        try:
            add_named_adapter(evo, adapter)
        except Exception:
            pass
        raw = load_file(str(weight))
        loaded = {k.replace(f".{src_name}.", f".{adapter}."): v for k, v in raw.items()}
        set_peft_model_state_dict(evo.model, loaded, adapter_name=adapter)
        skill_pairs = [pair for fam, pair in tagged if fam == skill]
        if not skill_pairs:
            continue
        last = {"steps": 0, "loss": None}
        for _ in range(rounds):
            last = sft_policy(evo, skill_pairs, lr, epochs, max_len, adapter=adapter)
        warm[skill] = adapter
        stats[skill] = {
            "atom": decision.get("atom"),
            "pairs": len(skill_pairs),
            "loss": last.get("loss"),
            "steps": last.get("steps"),
            "rounds": rounds,
            "epochs": epochs,
            "lr": lr,
        }
        print(
            f"[heldout] atom_sft skill={skill} adapter={adapter} pairs={len(skill_pairs)} "
            f"rounds={rounds} epochs={epochs} lr={lr} loss={last.get('loss')}",
            flush=True,
        )
    return warm, stats


def _model_flags(evo, packs, n: int, cfg: dict, warm: dict | None = None, seed_offset: int = 0) -> list[float]:
    from evo.office.stream import _license, _model_reply
    from evo.generate import generate_messages

    flags = []
    license = _license(cfg)
    families = list(cfg.get("families") or FAMILIES)
    if not families:
        families = list(FAMILIES)
    for pack in packs:
        for index in range(n):
            family = families[index % len(families)]
            variant = index % 3 if family == "table" else index % 2
            task = make_task(
                pack, family, 4000 + seed_offset + index, variant=variant, difficulty=int(cfg.get("difficulty", 1))
            )
            if warm and family in warm:
                adapter = warm[family]
                max_new = int(cfg.get("max_new_code") or cfg.get("max_new_tokens") or 220)

                def reply(messages, _adapter=adapter, _max_new=max_new):
                    return generate_messages(
                        evo,
                        messages,
                        _max_new,
                        float(cfg.get("temperature") or 0.0),
                        _adapter,
                    )

                print(f"[heldout] warm_atom family={family} adapter={adapter}", flush=True)
            else:
                reply = _model_reply(evo, cfg, task)
            with tempfile.TemporaryDirectory(prefix="evo-held-m-") as folder:
                result = run_episode(task, reply, Path(folder), license)
            flags.append(1.0 if result["ok"] else 0.0)
    return flags


def _dev_pairs_curriculum(cfg: dict) -> list[tuple[str, str]]:
    """Abbreviated-prompt SFT on real DEV packs; overweight table."""
    from evo.computer.actions import format_call
    from evo.office.packs import DEV_PACKS, pack_by_name

    schedule = list(cfg.get("dev_family_schedule") or ["table", "table", "table", "report", "file"])
    difficulties = [int(x) for x in (cfg.get("dev_difficulties") or [2, 3])]
    n = int(cfg.get("dev_items", 24))
    pack_names = list(cfg.get("dev_packs") or ["orders", "expenses"])
    packs = []
    for name in pack_names:
        try:
            packs.append(pack_by_name(name))
        except Exception:
            continue
    if not packs:
        packs = [DEV_PACKS[0]]
    pairs = []
    tagged = []
    for index in range(n):
        pack = packs[index % len(packs)]
        family = schedule[index % len(schedule)]
        difficulty = difficulties[index % len(difficulties)]
        variant = index % 3 if family == "table" else index % 2
        task = make_task(pack, family, 5000 + index, variant=variant, difficulty=difficulty)
        text = "\n".join(format_call(call.name, call.arguments) for call in task["calls"])
        pair = (task["prompt"], text)
        pairs.append(pair)
        tagged.append((family, pair))
    cfg["_tagged_pairs"] = tagged
    return pairs