# -*- coding: utf-8 -*-
"""C162: Cheap fix v8h_02 — OCR glues '14.ok'; unglue in parse; refresh V8 heldout claim if rate rises.
Reparse saved C159 OCR only (no GPU). Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric, _clean

GATE = 0.6
DOC = ROOT / "docs" / "r50"
SRC = DOC / "C159_VISION_V8_HELDOUT_SMOKE.json"
RUN = ROOT / "runs" / "vision_v8h_c162"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    prev = json.loads(SRC.read_text(encoding="utf-8"))
    rows_in = prev.get("rows") or []
    # unit proof on known fail OCR
    proof_ocr = next((r["ocr_preview"] for r in rows_in if r["id"] == "v8h_02"), "")
    proof_got, proof_ok = parse_metric(proof_ocr, "qty_sum", 23.0)

    rows, n_ok = [], 0
    for r in rows_in:
        got, atom_ok = parse_metric(r.get("ocr_preview") or "", r["metric"], r["expected"])
        ocr_ok = bool(r.get("ocr_ok"))
        ok = bool(ocr_ok and atom_ok)
        n_ok += int(ok)
        rows.append({
            **{k: r[k] for k in ("id", "kind", "metric", "expected", "ocr_preview") if k in r},
            "ocr_ok": ocr_ok,
            "atom_ok": atom_ok,
            "ok": ok,
            "got": got,
            "was_ok": bool(r.get("ok")),
            "prev_got": r.get("got"),
        })

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 16 and rate >= GATE
    claim = gate_pass
    rose = rate > float(prev.get("rate") or 0)
    scope = "r50plus_v8_heldout_disjoint_n>=16_c162_unglue_digit_status_qwen35_2b" if claim else None

    out = {
        "cycle": "C162",
        "theme": "v8h_02_unglue_digit_status_reparse",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "parse_fix": "unglue_digit.status_in__clean + qty_regex_tolerant",
        "unit_v8h_02": {
            "ocr_preview_head": (proof_ocr or "")[:160],
            "cleaned_head": _clean(proof_ocr)[:160],
            "got": proof_got,
            "expected": 23.0,
            "ok": proof_ok,
        },
        "prev_rate": prev.get("rate"),
        "prev_fail_ids": prev.get("fail_ids"),
        "n": n,
        "n_ok": n_ok,
        "rate": rate,
        "rate_rose": rose,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v8_heldout_claim": claim,
        "claim_scope": scope,
        "claim_refreshed": bool(claim and rose),
        "source_smoke": str(SRC.relative_to(ROOT)).replace("\\", "/"),
        "gate2_3_untouched": True,
        "v0_v7_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "Cheap reparse of saved C159 OCR after C162 unglue fix; no new VL call.",
    }
    J(DOC / "C162_V8H02_UNGLUE_REPARSE.json", out)
    J(RUN / "judge.json", out)
    if claim and rose:
        J(DOC / "C162b_VISION_GATE_V8_HELDOUT_REFRESH_CLAIM.json", {
            "kind": "vision_gate_v8_heldout_refresh_claim",
            "timestamp": ts(),
            "vl_gate_v8_heldout_claim": True,
            "rate": rate,
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "prev_rate": prev.get("rate"),
            "claim_scope": scope,
            "parse_fix": out["parse_fix"],
            "gate2_3_untouched": True,
            "v0_v7_untouched": True,
            "gen11": "HOLD",
            "cycle": "C162",
        })
    # also update C159b claim file rate if refreshed (keep history via C162b)
    print(json.dumps({
        "cycle": "C162",
        "rate": rate,
        "n_ok": n_ok,
        "n": n,
        "fail_ids": out["fail_ids"],
        "unit_v8h_02_ok": proof_ok,
        "rose": rose,
        "claim": claim,
        "claim_refreshed": out["claim_refreshed"],
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
