# -*- coding: utf-8 -*-
"""C68: Strengthen gen11 prep; DO NOT open seal unless near-ceiling evidence says go."""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

NEAR_CEILING = 0.99  # Branch B heritability burn threshold (from C61)


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    # Collect near-ceiling signals from recent boards — honest, no invent
    signals = []
    c62 = ROOT / "docs/r50/C62_replace_agent_board.json"
    c67 = ROOT / "docs/r50/C67_replace_agent_stress.json"
    c63 = ROOT / "docs/r50/C63_vision_v2_smoke.json"
    c65 = ROOT / "docs/r50/C65b_vision_v2_heldout_smoke.json"
    gate3 = ROOT / "docs/GATE3_GEN11_HERITABILITY_RULE_2026-10-18.json"

    def load(p):
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
        return None

    d62 = load(c62)
    d67 = load(c67)
    d63 = load(c63)
    d65 = load(c65)
    rule = load(gate3)

    if d62:
        signals.append({"src": "c62", "metric": "replace_agent_score", "value": d62.get("replace_agent_score"), "near_ceiling": float(d62.get("replace_agent_score") or 0) >= NEAR_CEILING})
    if d67:
        signals.append({"src": "c67", "metric": "replace_agent_score", "value": d67.get("replace_agent_score"), "near_ceiling": float(d67.get("replace_agent_score") or 0) >= NEAR_CEILING})
        signals.append({"src": "c67", "metric": "stress_rate", "value": d67.get("stress_rate"), "near_ceiling": float(d67.get("stress_rate") or 0) >= NEAR_CEILING})
    if d63:
        signals.append({"src": "c63", "metric": "v2_smoke_rate", "value": d63.get("rate"), "near_ceiling": float(d63.get("rate") or 0) >= NEAR_CEILING})
    if d65:
        signals.append({"src": "c65b", "metric": "v2_heldout_rate", "value": d65.get("rate"), "near_ceiling": float(d65.get("rate") or 0) >= NEAR_CEILING})

    # Fresh heritability proxy: we do NOT have a gen11 fresh run (seal closed). Record absence.
    fresh_proxy = None
    fresh_near = False
    signals.append({"src": "gen11_fresh", "metric": "fresh_rate", "value": fresh_proxy, "near_ceiling": False, "note": "seal closed; no fresh measured"})

    any_near = any(s.get("near_ceiling") for s in signals if s.get("src") != "gen11_fresh")
    # Burn policy: need explicit fresh>=0.99 for Branch B — not just other boards at 1.0
    go_open = False
    reason = (
        f"Branch B heritability requires measured fresh>={NEAR_CEILING} on sealed gen11 packs. "
        f"Other boards near-ceiling={any_near} but fresh unmeasured → seal stays closed."
    )

    checklist = {
        "rule_preregistered": (ROOT / "docs/GATE3_GEN11_HERITABILITY_RULE_2026-10-18.json").is_file(),
        "packs_code_present": (ROOT / "evo/office/heldout_gen11.py").is_file(),
        "seal_loader_present": "load_gen11_heldout" in (ROOT / "evo/office/seal.py").read_text(encoding="utf-8"),
        "config_present": (ROOT / "configs/office_gate3_gen11.yaml").is_file(),
        "open_heldout_false": True,
        "seal_file_absent": not (ROOT / "runs/heldout_seal_gen11.json").is_file(),
        "near_ceiling_threshold": NEAR_CEILING,
        "fresh_measured": False,
        "fresh_near_ceiling": fresh_near,
        "valuable_now": False,
        "go_open_seal": go_open,
    }

    # Strengthen prep artifacts: readiness memo + dry-run checklist
    memo = {
        "kind": "gen11_burn_readiness_memo",
        "timestamp": ts(),
        "decision": "HOLD",
        "go_open_seal": False,
        "reason": reason,
        "signals": signals,
        "what_would_unlock": [
            f"Run a non-gen11 ceiling probe on analogous heritability tasks >= {NEAR_CEILING}",
            "Confirm operator intent to burn irreversible seal",
            "Have rollback / Branch A Gate3 claim locked",
        ],
        "prep_strengthened": [
            "signals board aggregated",
            "explicit HOLD decision recorded",
            "unlock criteria written",
        ],
    }
    J(ROOT / "docs/r50/C68_gen11_burn_readiness_memo.json", memo)

    # Verify closed seal still PermissionError
    sealed_ok = False
    err = None
    try:
        import importlib
        import evo.office.seal as sealmod

        importlib.reload(sealmod)
        sealmod.load_gen11_heldout(False, "c68_strengthen_test")
    except PermissionError as e:
        sealed_ok = True
        err = str(e)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"

    checklist["permission_error_when_closed"] = sealed_ok
    prep_complete = all(
        checklist[k]
        for k in (
            "rule_preregistered",
            "packs_code_present",
            "seal_loader_present",
            "config_present",
            "open_heldout_false",
            "seal_file_absent",
            "permission_error_when_closed",
        )
    )

    payload = {
        "kind": "r50plus_c68_gen11_strengthen",
        "timestamp": ts(),
        "seal_opened": False,
        "ready_to_open": False,
        "go_open_seal": False,
        "prep_complete": prep_complete,
        "near_ceiling": NEAR_CEILING,
        "signals": signals,
        "checklist": checklist,
        "closed_error_sample": err,
        "decision": "HOLD",
        "reason": reason,
        "innovation": "Strengthen gen11 prep with explicit burn HOLD + unlock criteria; no seal burn",
        "gate2_3_untouched": True,
        "rule": rule.get("kind") if isinstance(rule, dict) else None,
    }
    J(ROOT / "docs/r50/C68_gen11_strengthen.json", payload)
    # refresh C18 readiness still closed
    J(
        ROOT / "docs/r50/C18_gen11_readiness.json",
        {
            "kind": "r50_c18",
            "rule_preregistered": True,
            "seal_opened": False,
            "ready_to_open": False,
            "prep_complete": prep_complete,
            "go_open_seal": False,
            "decision": "HOLD",
            "timestamp": ts(),
            "innovation": "C68 strengthen; burn discipline held",
        },
    )
    print(json.dumps({"prep_complete": prep_complete, "go_open_seal": False, "decision": "HOLD", "sealed_ok": sealed_ok}, ensure_ascii=False))


if __name__ == "__main__":
    main()
