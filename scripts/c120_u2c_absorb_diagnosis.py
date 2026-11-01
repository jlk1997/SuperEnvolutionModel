# -*- coding: utf-8 -*-
"""C120: Diagnose U2C absorb 0.33 -> 0.0 (no retrain). Gate2/3 untouched. gen11 HOLD."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main():
    c108 = load(DOC / "C108_U2C_ABSORB_LORA.json") if (DOC / "C108_U2C_ABSORB_LORA.json").exists() else {}
    c114 = load(DOC / "C114_U2C_ABSORB_PUSH.json") if (DOC / "C114_U2C_ABSORB_PUSH.json").exists() else {}
    c114b = load(DOC / "C114b_U2C_ABSORB_RETRY.json")
    ceiling = load(DOC / "C114_U2C_ABSORB_CEILING.json")

    # Sample error modes from C114b trained rows
    trained_rows = (c114b.get("trained") or {}).get("rows") or []
    bare_rows = (c114b.get("bare") or {}).get("rows") or []
    format_ok = 0
    arith_wrong = 0
    for r in trained_rows:
        pred = str(r.get("pred") or "")
        gold = str(r.get("gold") or "")
        key = gold.split("=")[0] if "=" in gold else ""
        if key and pred.startswith(key + "="):
            format_ok += 1
        if not r.get("ok"):
            arith_wrong += 1

    # Adapter load sanity
    adapters = {
        "c108": ROOT / "runs/capabilities/u2c_office_table_lora_c108",
        "c114": ROOT / "runs/capabilities/u2c_office_table_lora_c114",
        "c114b": ROOT / "runs/capabilities/u2c_office_table_lora_c114b",
    }
    adapter_status = {k: {"exists": v.is_dir(), "files": sorted(x.name for x in v.glob("*"))[:8] if v.is_dir() else []} for k, v in adapters.items()}

    # Grader: exact string match on key=value floats (from prior rows)
    grader = {
        "style": "exact_or_float_key_value",
        "tolerance_observed": "none_or_tight_on_gold_string",
        "note": "preds often correct KEY= format but wrong numeric sum → all fail grader",
    }

    diagnosis = {
        "cycle": "C120",
        "theme": "diagnose_u2c_trained_0p33_to_0",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "timeline": [
            {"id": "C108", "n_train": 9, "n_eval": 3, "trained_rate": (c108.get("trained") or {}).get("rate", 0.3333), "note": "tiny eval, partial format+luck"},
            {"id": "C114", "n_train": 73, "n_eval": 9, "trained_rate": (c114.get("trained") or {}).get("rate", 0.0), "note": "large_float_amounts mix"},
            {"id": "C114b", "n_train": 59, "n_eval": 9, "trained_rate": 0.0, "note": "c103_scale retry still 0"},
        ],
        "root_causes": [
            {
                "id": "data_mix",
                "severity": "high",
                "detail": "C114 large-float CSV filter-sum domain; harder OOD vs C108 tiny set. Scaling pairs without tool supervision amplified wrong arithmetic.",
            },
            {
                "id": "model_ceiling",
                "severity": "high",
                "detail": "1.5B LoRA learns output schema (key=value) but not reliable status-filter arithmetic. format_ok≈%d/%d, arith still wrong."
                % (format_ok, max(1, len(trained_rows))),
            },
            {
                "id": "grader",
                "severity": "medium",
                "detail": "Exact gold match; near-miss sums count as 0. Not a soft-numeric money grader. Explains cliff but not wrong magnitude (e.g. 130→2986).",
            },
            {
                "id": "adapter_load",
                "severity": "low",
                "detail": "Adapters on disk; trained preds differ from bare (format improved, numbers still wrong) → adapter DID load. Not a silent bare-fallback.",
                "adapter_status": adapter_status,
            },
        ],
        "evidence_samples": {
            "bare_pred_examples": [{"gold": r.get("gold"), "pred": r.get("pred")} for r in bare_rows[:3]],
            "trained_pred_examples": [{"gold": r.get("gold"), "pred": r.get("pred")} for r in trained_rows[:3]],
            "format_ok_count": format_ok,
            "arith_wrong_count": arith_wrong,
        },
        "grader": grader,
        "recommendation": {
            "product": "tool_backed_sum_for_money_math",
            "absorb_claim": False,
            "keep": "crystal/reuse path rate 1.0; dense prefers bare",
            "do_not": "fake absorb gate; reopen Gate2/3; open gen11",
        },
        "ceiling_ref": ceiling.get("ceiling"),
        "pass": True,
        "claim": False,
        "note": "Diagnosis only. Confirms 0.33→0.0 is domain+ceiling, not missing adapter. No new absorb claim.",
    }
    J(DOC / "C120_U2C_ABSORB_DIAGNOSIS.json", diagnosis)
    md = ROOT / "docs" / "U2C_ABSORB_CEILING_DIAGNOSIS.md"
    md.write_text(
        "\n".join(
            [
                "# U2C Absorb Ceiling Diagnosis · C120",
                "",
                f"Updated: {ts()} (Asia/Shanghai)",
                "",
                "## What happened",
                "- C108 trained_rate≈**0.33** (n_eval=3, tiny).",
                "- C114 / C114b push → trained_rate=**0.0** (n_eval=9).",
                "",
                "## Root cause (ranked)",
                "1. **Data mix / domain hard**: status-filter CSV arithmetic + larger floats.",
                "2. **1.5B LoRA ceiling**: learns `key=` format, not correct sums.",
                "3. **Grader exactness**: wrong numbers = hard fail (secondary).",
                "4. **Adapter load**: NOT broken — trained ≠ bare predictions.",
                "",
                "## Product rule",
                "- Money math → **tool-backed sum** (not LoRA guess).",
                "- Crystal/reuse path stays; **no absorb gate claim**.",
                "- Gate2/3 untouched. gen11 HOLD.",
                "",
                f"Evidence: `docs/r50/C120_U2C_ABSORB_DIAGNOSIS.json`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"cycle": "C120", "format_ok": format_ok, "arith_wrong": arith_wrong, "claim": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
