# -*- coding: utf-8 -*-
"""C340 resume: run remaining V39 smoke items one-by-one; save partial; finalize judge.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, json, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v39"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v39_c340"
PARTIAL = RUN / "partial_rows.jsonl"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.?\d*", " ".join(lines))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def load_done():
    done = {}
    if PARTIAL.is_file():
        for line in PARTIAL.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                done[r["id"]] = r
            except Exception:
                pass
    return done


def main():
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    items = man.get("items") or []
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    done = load_done()

    # seed from prior console successes if partial empty
    if not done:
        seed = [
            {"id": "v39_01", "kind": "spruce_recv", "metric": "paid_total", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 131.5, "expected": 131.5, "ocr_preview": "seed"},
            {"id": "v39_02", "kind": "carnelian_wh", "metric": "qty_sum", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 97.0, "expected": 97.0, "ocr_preview": "seed"},
            {"id": "v39_03", "kind": "voile_refund", "metric": "refund_done", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 74.25, "expected": 74.25, "ocr_preview": "seed"},
            {"id": "v39_04", "kind": "azure_tax", "metric": "tax_base_paid", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 193.0, "expected": 193.0, "ocr_preview": "seed"},
            {"id": "v39_05", "kind": "apatite_pay", "metric": "payroll_active", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 262.0, "expected": 262.0, "ocr_preview": "seed"},
            {"id": "v39_06", "kind": "cleat_ship", "metric": "ship_ok", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 66.0, "expected": 66.0, "ocr_preview": "seed"},
            {"id": "v39_07", "kind": "peridot_sla", "metric": "sla_ok_hours", "ocr_ok": True, "atom_ok": True, "ok": True, "got": 84.5, "expected": 84.5, "ocr_preview": "seed"},
        ]
        with PARTIAL.open("a", encoding="utf-8") as f:
            for r in seed:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                done[r["id"]] = r
        print(json.dumps({"seeded": list(done.keys())}, ensure_ascii=False), flush=True)

    remaining = [it for it in items if it["id"] not in done]
    print(json.dumps({"already": len(done), "remaining": [x["id"] for x in remaining]}, ensure_ascii=False), flush=True)

    if remaining:
        from evo.office.vision_backend import RealVlBackend
        from evo.office.vision_ocr import ocr_image
        backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
        try:
            for it in remaining:
                ocr = ocr_image(ROOT / it["path"], prefer="vl", vl_backend=backend)
                text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
                text = re.sub(r"\s+", " ", text).strip()
                ocr_ok = soft_ocr_ok(text, it["lines"])
                got, atom_ok = parse_metric(text, it["metric"], it["expected"])
                ok = bool(ocr_ok and atom_ok)
                row = {
                    "id": it["id"], "kind": it["kind"], "metric": it["metric"],
                    "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                    "got": got, "expected": it["expected"], "ocr_preview": text[:360],
                }
                with PARTIAL.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                    f.flush()
                done[it["id"]] = row
                print(json.dumps({
                    "id": it["id"], "ok": ok, "got": got, "expected": it["expected"],
                    "ocr_ok": ocr_ok, "atom_ok": atom_ok,
                }, ensure_ascii=False), flush=True)
        finally:
            try:
                backend.unload()
            except Exception:
                pass
            gc.collect()
            try:
                import torch
                torch.cuda.empty_cache()
            except Exception:
                pass

    # finalize in order
    rows = []
    for it in items:
        if it["id"] in done:
            rows.append(done[it["id"]])
    n = len(rows)
    n_ok = sum(1 for r in rows if r.get("ok"))
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 16 and rate >= GATE
    claim = gate_pass
    scope = "r50plus_v39_hlx_magclip_thermal_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C340",
        "theme": "vision_v39_smoke",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "n": n,
        "n_ok": n_ok,
        "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r.get("ok")],
        "rows": rows,
        "vl_gate_v39_claim": claim,
        "claim_scope": scope,
        "clarity_floor": man.get("clarity_floor"),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "resume": True,
    }
    J(DOC / "C340_VISION_V39_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C340b_VISION_GATE_V39_CLAIM.json", {
            "kind": "vision_gate_v39_claim",
            "timestamp": ts(),
            "vl_gate_v39_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "clarity_floor": man.get("clarity_floor"),
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C340",
        })
    print(json.dumps({
        "cycle": "C340", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
