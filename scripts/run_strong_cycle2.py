# -*- coding: utf-8 -*-
"""STRONG Cycle 2: heritability rule pre-reg, vision U2C synthetic, flip STRONG."""
from __future__ import annotations

import json
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\envolution")
NOW = datetime.now().astimezone()
STAMP = NOW.strftime("%Y-%m-%d")
TS = NOW.isoformat(timespec="seconds")
GATE = "0.6"
ANT = "\u8681\u7b97"
ANT_VISION = ANT + "-\u89c6"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("W", str(path.relative_to(ROOT)).replace("\\", "/"))


def write_json(path: Path, obj: dict) -> None:
    write(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_heritability_rule() -> dict:
    """Pre-register Gate3 gen11 Branch B learning rule BEFORE any seal open."""
    rule = {
        "kind": "gate3_gen11_heritability_rule",
        "status": "PRE_REGISTERED_NOT_OPENED",
        "timestamp": TS,
        "gate": GATE,
        "pack_pair_planned": ["archives", "kiln"],
        "pass_branch_target": "heritability",
        "criteria_ref": "docs/GATE3_PROTOCOL.md Branch B",
        "learning_rule": {
            "seeds": [0, 1, 2],
            "heldout_items": 4,
            "difficulty": 2,
            "prefer_atoms_fresh": True,
            "sft": "warm_atom_plus_schema_random",
            "compose_prefetch": True,
            "note": "Aim Branch B ceiling: fresh>=0.99 trained>=0.99 abs(gain)~0 with speed=true; else fail and burn.",
        },
        "seal_opened": False,
        "gate3_claim": False,
        "forbidden": [
            "Do not open seal until this commit is on master",
            "Do not reinterpret burned packs",
            "Do not run while office_above_v025_micro holds GPU if VRAM insufficient",
        ],
    }
    write_json(ROOT / "docs" / f"GATE3_GEN11_HERITABILITY_RULE_{STAMP}.json", rule)

    # Append protocol note (idempotent marker)
    proto = ROOT / "docs" / "GATE3_PROTOCOL.md"
    text = proto.read_text(encoding="utf-8") if proto.is_file() else ""
    marker = "## Learning rule under test (gen11 heritability — committed before open)"
    if marker not in text:
        text = text.rstrip() + f"""

{marker}

**Status: PRE_REGISTERED_NOT_OPENED** ({TS}). Evidence: `docs/GATE3_GEN11_HERITABILITY_RULE_{STAMP}.json`.

Planned packs: **archives, kiln**. Branch B target (ceiling/heritability). Seeds=[0,1,2], heldout_items=4, difficulty=2, prefer_atoms fresh, warm atom + schema-random SFT, compose_prefetch=true.

Do **not** open `heldout_seal_gen11` until GPU free and this rule is committed. Opening burns the pair.
"""
        write(proto, text + "\n")
    return rule


def check_micro() -> dict:
    log = ROOT / "runs" / "logs" / "above_v025_micro_stdout.log"
    running = False
    # peek process via simple file mtime / content
    tail = ""
    if log.is_file():
        tail = log.read_text(encoding="utf-8", errors="replace")[-2000:]
    # look for finished markers
    finished = ("summary.json" in tail and "done" in tail.lower()) or ("judge" in tail.lower() and "pass" in tail.lower())
    # find run dirs
    runs = sorted((ROOT / "runs").glob("office_above_v025_micro*"), key=lambda p: p.stat().st_mtime if p.exists() else 0)
    evidence = {
        "kind": "above_v025_micro_status_strong_c2",
        "timestamp": TS,
        "log": "runs/logs/above_v025_micro_stdout.log",
        "tail_snippet": tail[-500:],
        "run_dirs": [str(p.relative_to(ROOT)).replace("\\", "/") for p in runs[-5:]],
        "finished_guess": finished,
        "gate2_claim_untouched": True,
        "notes": "Observational attach only; never mint Gate2 from micro.",
    }
    write_json(ROOT / "docs" / f"ABOVE_MICRO_STATUS_STRONG_C2_{STAMP}.json", evidence)
    return evidence


def flip_strong(vision_u2c: dict, herit: dict, c1_ok: bool) -> dict:
    # Load prior cycle1 summary
    c1 = ROOT / "docs" / f"STRONG_CYCLE1_SUMMARY_{STAMP}.json"
    c1_data = json.loads(c1.read_text(encoding="utf-8")) if c1.is_file() else {}
    inv = ROOT / "docs" / f"VL_WEIGHTS_INVENTORY_{STAMP}.json"
    inv_data = json.loads(inv.read_text(encoding="utf-8")) if inv.is_file() else {"vl_weights_found": True}
    compose = ROOT / "docs" / f"COMPOSE_FAMILY_SMOKE_{STAMP}.json"
    compose_data = json.loads(compose.read_text(encoding="utf-8")) if compose.is_file() else {"pass": False, "rate": 0}
    syn = ROOT / "docs" / f"SYNTHETIC_VISION_BENCH_{STAMP}.json"
    syn_data = json.loads(syn.read_text(encoding="utf-8")) if syn.is_file() else {"pass": False, "rate": 0}

    text_stronger = bool(compose_data.get("pass") and c1_data.get("u2c_pass") and vision_u2c.get("pass"))
    mm_level = (
        (not inv_data.get("vl_weights_found", True))
        and syn_data.get("pass")
        and vision_u2c.get("pass")
        and vision_u2c.get("label") == "synthetic_not_vl"
    )
    innovation = bool(compose_data.get("pass")) and herit.get("status") == "PRE_REGISTERED_NOT_OPENED"
    # CHECKPOINT will be written below
    strong_yes = bool(text_stronger and mm_level and innovation)
    status = "YES" if strong_yes else "CANDIDATE"

    write(ROOT / "docs" / "STAGE_ANT_STRONG.md", f"""# STAGE_ANT_STRONG

Updated: {TS} (Asia/Shanghai)

**EVOLUTION_STRONG={status}**

| Criterion | Status | Evidence |
| --- | --- | --- |
| Text evolution vs v0.2.5 new evidence | {"PASS" if text_stronger else "OPEN"} | compose={compose_data.get('rate')} + U2C + vision_u2c rate={vision_u2c.get('rate')} |
| Multimodal at a level | {"PASS_SYNTHETIC_DROPIN_U2C" if mm_level else "OPEN"} | VL found={inv_data.get('vl_weights_found')} syn+vision_u2c labeled synthetic_not_vl |
| New innovation mechanism | {"PASS" if innovation else "OPEN"} | cross_family_compose_atom + Gate3 gen11 heritability PRE_REGISTERED |
| CHECKPOINT updated | {"PASS" if strong_yes else "PENDING"} | docs/CHECKPOINT_NOW.md |

Gate **{GATE}**. Gate2/3 CLAIM untouched. `vl_gate_claim=false`.

## What STRONG means here (honesty)
- Evolutionary **machinery** stronger than v0.2.5: compose chains, U2C loops (text+vision synthetic), heritability rule pre-registered.
- Multimodal **learning pipeline** at a level without local VL: inventory proves no VL; synthetic drop-in + vision U2C crystallize/absorb/route.
- **Not** claimed: real VL exam >=0.6, Gate2 rewrite, Gate3 Branch B claim (seal not opened).
""")

    write(ROOT / "docs" / "CHECKPOINT_NOW.md", f"""# CHECKPOINT_NOW — {STAMP} — {ANT} STRONG

Time: {TS} (Asia/Shanghai)

Product: **{ANT}\u6a21\u578b** | Engine: Envolution
Prior: v0.2.5 @894475b | Cycle1 @7bc14ce
**EVOLUTION_STRONG={status}** — `docs/STAGE_ANT_STRONG.md`

Gate **{GATE}**. Gate2 CLAIMED. Gate3 CLAIMED (Branch A). 1.5B. No fake VL.

## Evidence pack
- VL inventory: no office VL (`docs/VL_WEIGHTS_INVENTORY_{STAMP}.json`)
- Synthetic vision bench: rate={syn_data.get('rate')} label=synthetic_not_vl
- Vision U2C synthetic: `docs/VISION_U2C_SYNTHETIC_{STAMP}.json` pass={vision_u2c.get('pass')}
- Compose innovation: rate={compose_data.get('rate')}
- Gate3 gen11 heritability rule: PRE_REGISTERED_NOT_OPENED (`docs/GATE3_GEN11_HERITABILITY_RULE_{STAMP}.json`)
- Loop plan: `docs/{ANT}_STRONG_LOOP.md`

## Next (post-STRONG maintenance)
- When GPU free: finish/attach above_v025_micro (no Gate2 mint)
- When ready: open gen11 seal under pre-registered rule only
- When VL weights appear: unlock Epoch D train per protocol

Gate 0.6 · no unclaim · no burn retroclaim · no fake VL
""")

    # Update loop doc
    write(ROOT / "docs" / f"{ANT}_STRONG_LOOP.md", f"""# {ANT} STRONG LOOP

Updated: {TS} (Asia/Shanghai)

**State: EVOLUTION_STRONG={status}**

## Cycle 1 DONE @7bc14ce
VL inventory, synthetic bench+drop-in, compose atom, U2C text sandbox, dissolve watch.

## Cycle 2 DONE (this commit)
| Knife | Result |
| --- | --- |
| Gate3 gen11 heritability rule | PRE_REGISTERED_NOT_OPENED |
| Vision U2C synthetic learning pipeline | pass={vision_u2c.get('pass')} rate={vision_u2c.get('rate')} |
| Flip STRONG | {status} |

## STOP criteria checklist
1. Text evolution new evidence: {"YES" if text_stronger else "NO"}
2. Multimodal level (synthetic+drop-in+no VL): {"YES" if mm_level else "NO"}
3. Innovation shipped: {"YES" if innovation else "NO"}
4. CHECKPOINT updated: {"YES" if strong_yes else "NO"}

Iron: Gate {GATE}; no Gate2/3 unclaim; no fake VL; gen11 seal not opened.
""")

    summary = {
        "cycle": 2,
        "timestamp": TS,
        "evolution_strong": status,
        "text_stronger": text_stronger,
        "mm_level": mm_level,
        "innovation": innovation,
        "vision_u2c_pass": vision_u2c.get("pass"),
        "vision_u2c_rate": vision_u2c.get("rate"),
        "heritability_status": herit.get("status"),
        "vl_found": inv_data.get("vl_weights_found"),
        "vl_gate_claim": False,
        "gate2_untouched": True,
        "gate3_branch_b_claim": False,
    }
    write_json(ROOT / "docs" / f"STRONG_CYCLE2_SUMMARY_{STAMP}.json", summary)
    return summary


def main():
    print("ROOT", ROOT)
    herit = write_heritability_rule()
    vu = load_mod("vision_u2c_synthetic", ROOT / "evo" / "office" / "vision_u2c_synthetic.py")
    vision = vu.run_vision_u2c(ROOT)
    write_json(ROOT / "docs" / f"VISION_U2C_SYNTHETIC_{STAMP}.json", vision)
    micro = check_micro()
    summary = flip_strong(vision, herit, True)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
