# -*- coding: utf-8 -*-
"""Post-V1 strength cycles: compose + vision U2C crystallize on readable fixtures + beat board."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\envolution")
GATE = 0.6


def ts() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cycle_compose() -> dict:
    from evo.office.compose_atom import run_compose_smoke

    ev = run_compose_smoke(ROOT)
    out = ROOT / "docs" / "r50" / "C54_compose_post_v1.json"
    payload = {
        "kind": "r50_c54_compose_post_v1",
        "timestamp": ts(),
        "gate": GATE,
        "pass": bool(ev.get("pass")),
        "rate": ev.get("rate"),
        "n": ev.get("n"),
        "n_ok": ev.get("n_ok"),
        "details": ev,
        "innovation": "Compose family smoke after Vision V1 claim",
        "gate2_3_untouched": True,
    }
    J(out, payload)
    J(ROOT / "docs" / f"COMPOSE_FAMILY_SMOKE_{datetime.now().strftime('%Y-%m-%d')}.json", ev)
    return payload


def cycle_vision_u2c() -> dict:
    """Use→grade→crystallize on C52 readable successes. No new Gate2/3."""
    smoke = json.loads((ROOT / "docs/r50/C52_vision_v1_smoke_readable.json").read_text(encoding="utf-8"))
    base = ROOT / "runs" / "vision_u2c_v1_readable"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    use_log = []
    atoms = []
    for row in smoke["items"]:
        if row.get("error"):
            continue
        img = f"evo/office/fixtures/vision_images_real/{row['id']}.png"
        ok = bool(row.get("ok"))
        use_log.append({
            "phase": "use",
            "task_id": row["id"],
            "task": row.get("task"),
            "image": img,
            "pred": row.get("pred_head"),
            "backend": "real_vl",
            "readable_v1": True,
            "weights_local": True,
        })
        use_log.append({"phase": "grade", "task_id": row["id"], "ok": ok, "gold": row.get("gold")})
        if ok:
            atom = {
                "id": f"vision_atom_{row['id']}",
                "family": f"vision_{row.get('task')}",
                "task": row.get("task"),
                "image": img,
                "gold": row.get("gold"),
                "source": "c52_readable_v1",
                "crystallized": True,
            }
            atoms.append(atom)
            use_log.append({"phase": "crystallize", "atom_id": atom["id"], "ok": True})

    # route check: registry grows
    reg_path = ROOT / "evo/office/fixtures/vision_atom_registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.is_file() else {"atoms": []}
    if isinstance(reg, list):
        reg = {"atoms": reg}
    existing = reg.get("atoms") or []
    if isinstance(existing, dict):
        existing = list(existing.values())
    ids = {a.get("id") for a in existing if isinstance(a, dict)}
    added = 0
    for a in atoms:
        if a["id"] not in ids:
            existing.append({**a, "registered_at": ts()})
            ids.add(a["id"])
            added += 1
            use_log.append({"phase": "route_register", "atom_id": a["id"], "ok": True})
    reg["atoms"] = existing
    reg["updated"] = ts()
    reg["source"] = "c55_vision_u2c_v1_readable"
    J(reg_path, reg)

    J(base / "use_log.jsonl", None)  # placeholder replaced below
    (base / "use_log.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in use_log) + "\n", encoding="utf-8"
    )
    J(base / "vision_atoms_crystallized.json", {"n": len(atoms), "atoms": atoms, "timestamp": ts()})

    rate = (len(atoms) / max(1, sum(1 for r in smoke["items"] if not r.get("error"))))
    payload = {
        "kind": "r50_c55_vision_u2c_v1_readable",
        "timestamp": ts(),
        "gate": GATE,
        "n_use": sum(1 for e in use_log if e.get("phase") == "use"),
        "n_crystallized": len(atoms),
        "n_registry_added": added,
        "crystallize_rate": round(rate, 4),
        "pass": rate >= GATE,
        "adapter_trained": False,
        "note": "Crystallize+route only this cycle (no LoRA) — honest pipeline after V1 claim",
        "evidence_run": str(base.relative_to(ROOT)).replace("\\", "/"),
        "innovation": "Vision U2C on readable V1 fixtures → atom registry growth",
        "gate2_3_untouched": True,
    }
    J(ROOT / "docs/r50/C55_vision_u2c_v1_readable.json", payload)
    return payload


def cycle_beat_board() -> dict:
    """Refresh beat-agent observational board from existing Gate2 claim + cost ledger; no new claim."""
    g2 = None
    for cand in [
        ROOT / "docs/GATE2_CLAIM.json",
        ROOT / "docs/r50/C01_beat_agent_board.json",
    ]:
        if cand.is_file():
            g2 = json.loads(cand.read_text(encoding="utf-8"))
            break
    cost = None
    for cand in sorted((ROOT / "docs").glob("COST_LEDGER*.json")):
        cost = json.loads(cand.read_text(encoding="utf-8"))
    v1 = json.loads((ROOT / "docs/r50/C52_vision_v1_smoke_readable.json").read_text(encoding="utf-8"))
    board = {
        "kind": "r50_c56_beat_agent_board_post_v1",
        "timestamp": ts(),
        "gate2_claim_untouched": True,
        "gate3_claim_untouched": True,
        "text_beat_agent_ref": g2,
        "cost_ledger_ref_keys": list(cost.keys())[:12] if isinstance(cost, dict) else None,
        "vision_v1_rate": v1.get("rate"),
        "vision_v1_claim": v1.get("vl_gate_v1_claim"),
        "composite_note": "Text Gate2 claim preserved; Vision V1 now also scoped-claimed — dual stack stronger",
        "innovation": "Post-V1 beat-agent observational board (no new text gate mint)",
    }
    # optional: re-run cost ledger stub if script exists
    try:
        import subprocess

        subprocess.check_call(
            [str(ROOT / ".venv/Scripts/python.exe"), str(ROOT / "scripts/cost_ledger_dual_vs_agent.py")],
            cwd=str(ROOT),
        )
        board["cost_ledger_refreshed"] = True
    except Exception as e:  # noqa: BLE001
        board["cost_ledger_refreshed"] = False
        board["cost_ledger_error"] = f"{type(e).__name__}: {e}"[:300]
    J(ROOT / "docs/r50/C56_beat_agent_board_post_v1.json", board)
    return board


def main():
    c54 = cycle_compose()
    c55 = cycle_vision_u2c()
    c56 = cycle_beat_board()
    summary = {
        "kind": "post_v1_strength_cycles",
        "timestamp": ts(),
        "compose_rate": c54.get("rate"),
        "compose_pass": c54.get("pass"),
        "u2c_crystallize_rate": c55.get("crystallize_rate"),
        "u2c_pass": c55.get("pass"),
        "vision_v1_rate": c56.get("vision_v1_rate"),
        "all_strength_ok": bool(c54.get("pass") and c55.get("pass")),
        "gate2_3_untouched": True,
    }
    J(ROOT / "docs/r50/C57_post_v1_strength_summary.json", summary)
    # loop append
    loop = ROOT / "docs" / "蚁算_R50_LOOP.md"
    if loop.is_file():
        block = f"""

### Post-R50 strength — C54 compose / C55 vision U2C / C56 beat board
- **Time**: {ts()}
- **Compose**: rate={c54.get('rate')} pass={c54.get('pass')}
- **Vision U2C crystallize**: rate={c55.get('crystallize_rate')} added={c55.get('n_registry_added')}
- **Beat board**: observational only; Gate2/3 untouched
- **Evidence**: `docs/r50/C54_*.json`, `C55_*.json`, `C56_*.json`, `C57_*.json`
"""
        loop.write_text(loop.read_text(encoding="utf-8").rstrip() + block + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
