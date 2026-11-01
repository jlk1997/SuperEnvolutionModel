# -*- coding: utf-8 -*-
"""蚁算-视 fixture eval harness — schema/validate only, NO weights, NO fake scores."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def validate_event(ev: dict, schema: dict) -> list[str]:
    errs = []
    for key in schema.get("required") or []:
        if key not in ev:
            errs.append(f"missing:{key}")
    modality = ev.get("modality")
    if modality is not None and modality not in ("text", "image", "image+text"):
        errs.append("bad_modality")
    if modality in ("image", "image+text"):
        iref = ev.get("image_ref")
        if not isinstance(iref, dict):
            errs.append("missing:image_ref")
        else:
            for k in ("uri", "sha256", "mime"):
                if k not in iref:
                    errs.append(f"missing:image_ref.{k}")
            sha = iref.get("sha256")
            if sha is not None and not SHA256_RE.match(str(sha)):
                errs.append("bad:image_ref.sha256")
    if ev.get("vl_gate_claim") is True:
        errs.append("forbidden:vl_gate_claim_true_without_weights")
    if ev.get("weights_local") is True:
        # harness does not verify weights; flag as warning-level for honesty
        errs.append("unexpected:weights_local_true_in_fixture")
    return errs


def build_registry(root: Path) -> dict:
    return {
        "kind": "vision_atom_registry",
        "product": "蚁算-视",
        "version": "0.2.5",
        "gate": "0.6",
        "weights_local": False,
        "vl_gate_claim": False,
        "atoms": [
            {
                "atom": "vision_table_uselog",
                "family": "vision_table",
                "status": "stub_pending_weights",
                "stub_path": "evo/office/fixtures/vision_table_atom_stub.json",
                "dissolve_path": [
                    "use_log(image_ref) -> grade -> pairs",
                    "crystallize -> CapabilityAtom vision_table_uselog",
                    "dissolve bare vs scaffold when VL weights ready",
                    "route prefer_atoms",
                ],
            },
            {
                "atom": "vision_ui_uselog",
                "family": "vision_ui",
                "status": "stub_pending_weights",
                "stub_path": "evo/office/fixtures/vision_ui_atom_stub.json",
                "dissolve_path": [
                    "screenshot use_log -> grade",
                    "crystallize vision_ui_uselog",
                    "dissolve when VL ready",
                    "route prefer_atoms",
                ],
            },
            {
                "atom": "vision_doc_uselog",
                "family": "vision_doc",
                "status": "stub_pending_weights",
                "stub_path": "evo/office/fixtures/vision_doc_atom_stub.json",
                "dissolve_path": [
                    "PDF/page image use_log -> grade",
                    "crystallize vision_doc_uselog",
                    "dissolve when VL ready",
                    "route prefer_atoms",
                ],
            },
        ],
        "notes": "Registry only. No bare/D. No train. Opens after local VL weights pass V0.",
    }


def run_harness(root: Path | None = None) -> dict:
    root = root or repo_root()
    schema_path = root / "docs" / "schemas" / "vision_use_log_event.json"
    fixture_path = root / "evo" / "office" / "fixtures" / "vision_use_log_fixture.jsonl"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    lines = [ln for ln in fixture_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    events = [json.loads(ln) for ln in lines]
    per = []
    all_ok = True
    for i, ev in enumerate(events):
        errs = validate_event(ev, schema)
        ok = not errs
        all_ok = all_ok and ok
        per.append({"index": i, "task_id": ev.get("task_id"), "modality": ev.get("modality"), "ok": ok, "errors": errs})

    registry = build_registry(root)
    # write atom stubs under fixtures (tracked)
    fixtures = root / "evo" / "office" / "fixtures"
    for atom in registry["atoms"]:
        stub = {
            "kind": "vision_atom_stub",
            "product": "蚁算-视",
            "atom": atom["atom"],
            "family": atom["family"],
            "status": atom["status"],
            "gate": "0.6",
            "weights_local": False,
            "vl_gate_claim": False,
            "bare_rate": None,
            "scaffold_rate": None,
            "dissolution": None,
            "dissolve_path": atom["dissolve_path"],
            "fixture_use_log": "evo/office/fixtures/vision_use_log_fixture.jsonl",
            "schema": "docs/schemas/vision_use_log_event.json",
            "version": "0.2.5",
            "notes": "No training. No fake bare/D.",
        }
        (fixtures / Path(atom["stub_path"]).name).write_text(
            json.dumps(stub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    reg_path = fixtures / "vision_atom_registry.json"
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # expand fixture with one more vision_doc line if missing
    families = {e.get("family") for e in events}
    if "vision_doc" not in families:
        extra = {
            "event": "observation",
            "modality": "image",
            "task_id": "viz-doc-001",
            "family": "vision_doc",
            "split": "practice",
            "image_ref": {
                "uri": "runs/use_log/images/fixture_viz_doc_001.png",
                "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "width": 128,
                "height": 128,
                "mime": "image/png",
            },
            "text_caption": None,
            "caption_source": "none",
            "tool_call": None,
            "weights_local": False,
            "vl_gate_claim": False,
        }
        with fixture_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(extra, ensure_ascii=False) + "\n")
        events.append(extra)
        errs = validate_event(extra, schema)
        per.append({"index": len(per), "task_id": extra["task_id"], "modality": "image", "ok": not errs, "errors": errs})
        all_ok = all_ok and not errs

    evidence = {
        "kind": "vision_fixture_harness",
        "product": "蚁算-视",
        "version": "0.2.5",
        "gate": "0.6",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "weights_local": False,
        "vl_gate_claim": False,
        "method": "schema_validate_only",
        "schema": str(schema_path.relative_to(root)).replace("\\", "/"),
        "fixture": str(fixture_path.relative_to(root)).replace("\\", "/"),
        "registry": str(reg_path.relative_to(root)).replace("\\", "/"),
        "n_events": len(events),
        "per_event": per,
        "all_events_valid": all_ok,
        "fake_scores": False,
        "pass": all_ok and reg_path.is_file(),
        "notes": "Harness runs without VL weights. Validates schema + registry stubs only.",
    }
    stamp = datetime.now().strftime("%Y-%m-%d")
    out = root / "docs" / f"VISION_FIXTURE_HARNESS_{stamp}.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence["evidence_path"] = str(out)
    return evidence


def main() -> None:
    ev = run_harness()
    print(json.dumps({"pass": ev["pass"], "n": ev["n_events"], "path": ev["evidence_path"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
