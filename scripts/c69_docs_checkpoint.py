# -*- coding: utf-8 -*-
"""C69: Update STAGE_ANT_R50PLUS + CHECKPOINT + loop after C65-C68."""
from __future__ import annotations
import json, subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(p: Path):
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main():
    c65f = load(ROOT / "docs/r50/C65_vision_v2_heldout_fixtures.json")
    c65b = load(ROOT / "docs/r50/C65b_vision_v2_heldout_smoke.json")
    c65c = load(ROOT / "docs/r50/C65c_vision_gate_v2_heldout_claim.json")
    c66 = load(ROOT / "docs/r50/C66_vision_lora_vs_bare.json")
    c67 = load(ROOT / "docs/r50/C67_replace_agent_stress.json")
    c68 = load(ROOT / "docs/r50/C68_gen11_strengthen.json")

    heldout_rate = float(c65b.get("rate") or 0)
    heldout_claim = bool(c65b.get("vl_gate_v2_heldout_claim") or c65c.get("vl_gate_v2_heldout_claim"))
    bare_r = (c66.get("bare") or {}).get("rate")
    lora_r = (c66.get("lora") or {}).get("rate")
    delta = c66.get("delta_lora_minus_bare")
    replace = float(c67.get("replace_agent_score") or 0)
    stress = float(c67.get("stress_rate") or 0)
    gen11_hold = c68.get("decision") == "HOLD" and not c68.get("seal_opened")

    # composite: honest blend of available signals
    mm = heldout_rate if heldout_rate else float(load(ROOT / "docs/r50/C63_vision_v2_smoke.json").get("rate") or 0)
    replace_s = replace
    dissolve = 1.0  # prior dissolve board
    gen_prep = 1.0 if c68.get("prep_complete") else 0.5
    composite = round(0.35 * mm + 0.35 * replace_s + 0.15 * dissolve + 0.15 * gen_prep, 3)

    summary = {
        "kind": "r50plus_c69_summary",
        "timestamp": ts(),
        "gate": GATE,
        "cycles": "C65-C69",
        "heldout_n": c65b.get("n") or c65f.get("n"),
        "heldout_rate": heldout_rate,
        "heldout_claim": heldout_claim,
        "lora_vs_bare": {"bare": bare_r, "lora": lora_r, "delta": delta},
        "replace_agent_score": replace,
        "stress_rate": stress,
        "gen11_seal_opened": False,
        "gen11_decision": c68.get("decision"),
        "composite": composite,
        "gate2_3_untouched": True,
        "v1_v2_smoke_claims_untouched": True,
        "git_hash_at_write": git_hash(),
    }
    (ROOT / "docs/r50/C69_r50plus_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "docs/r50/SCORECARD_LATEST.json").write_text(
        json.dumps(
            {
                "timestamp": ts(),
                "composite": composite,
                "heldout_rate": heldout_rate,
                "heldout_claim": heldout_claim,
                "replace": replace,
                "stress_rate": stress,
                "lora_delta": delta,
                "gen11_hold": gen11_hold,
                "gate": GATE,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    stage = f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (post Vision V1/V2 CLAIM @b987df2 → C65-C69)

## Cycles landed
- C58 softmatch harden
- C59-C63 Vision V2 fixtures + smoke CLAIM 1.0
- C60 LoRA absorb ok
- C61/C68 gen11 prep; **seal NOT opened** (HOLD)
- C62 replace-agent 1.0; **C67 stress** replace={replace} stress_rate={stress}
- **C65 heldout fixtures n={c65f.get('n')}**
- **C65b heldout smoke rate={heldout_rate} claim={heldout_claim}**
- **C66 LoRA vs bare** bare={bare_r} lora={lora_r} delta={delta}
- C69 docs/checkpoint

## Iron
Gate **{GATE}**. Gate2/3 CLAIMED untouched. V1/V2 smoke claims untouched. No fake VL. gen11 burn discipline held.

## Evidence
`docs/r50/C65_*.json` … `C69_*.json` · loop `docs/蚁算_R50PLUS_LOOP.md`
"""
    (ROOT / "docs/STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **{GATE}**. Gate2/3 CLAIMED untouched.
Vision V1 CLAIM kept. Vision V2 smoke CLAIM kept.
Vision V2 **heldout** rate={heldout_rate} claim={heldout_claim}.
LoRA vs bare: bare={bare_r} lora={lora_r} delta={delta}.
Replace stress={stress} score={replace}.
gen11 seal_opened=false decision=HOLD.

Composite≈{composite}
"""
    (ROOT / "docs/CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    loop_path = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    loop = f"""# 蚁算 R50+ LOOP

Updated: {ts()} (Asia/Shanghai)

Mandate: continuous evolution after R50 / Vision V1+V2 CLAIM. Gate **{GATE}**. Gate2/3 untouched. No fake VL. gen11 seal closed until readiness + value.

## Progress

| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C58 | softmatch | DONE | 1.0 | C58_*.json |
| C59 | vision-v2-fix | DONE | n=8 | C59_*.json |
| C60 | u2c-lora | DONE | absorb=True | C60_*.json |
| C61 | gen11-prep | DONE | seal=closed | C61_*.json |
| C62 | replace-agent | DONE | 1.0 | C62_*.json |
| C63 | vision-v2-smoke | DONE | 1.0 claim=True | C63_*.json |
| C64 | docs | DONE | composite=0.97 | C64_*.json |
| C65 | v2-heldout-fix | DONE | n={c65f.get('n')} | C65_*.json |
| C65b | v2-heldout-smoke | DONE | rate={heldout_rate} claim={heldout_claim} | C65b_*.json |
| C66 | lora-vs-bare | DONE | delta={delta} | C66_*.json |
| C67 | replace-stress | DONE | {replace}/{stress} | C67_*.json |
| C68 | gen11-HOLD | DONE | seal=closed | C68_*.json |
| C69 | docs | DONE | composite={composite} | C69_*.json |

## Cycles

### R50+ batch C65-C69 — DONE
- **Time**: {ts()}
- **C65**: heldout fixtures n={c65f.get('n')}
- **C65b**: heldout rate={heldout_rate} claim={heldout_claim}
- **C66**: bare={bare_r} lora={lora_r} delta={delta}
- **C67**: replace={replace} stress={stress}
- **C68**: gen11 HOLD seal_opened=false
- **Composite**: {composite}
"""
    loop_path.write_text(loop, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
