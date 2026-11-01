# -*- coding: utf-8 -*-
"""C163: Vision V9 real-VL smoke. Claim only if rate>=0.6 and n>=16.
Hardening: torn/barcode/FX/ghost/QR. Uses C162 parse (unglue digit.status).
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
FIX = ROOT / "evo/office/fixtures/vision_images_v9"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v9_c163"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.?\d*", " ".join(lines if isinstance(lines, list) else [str(lines)]))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def gpu_free_mib():
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        return float((r.stdout or "0").strip().split("\n")[0])
    except Exception:
        return 0.0


def main():
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    # normalize any legacy swapped fields
    for it in man["items"]:
        if isinstance(it.get("metric"), (int, float)) and isinstance(it.get("lines"), str):
            # swapped legacy — should not happen after C160 fix regen
            it["metric"], it["expected"], it["lines"] = it["lines"], it["metric"], it["expected"]
        if not isinstance(it.get("lines"), list):
            raise SystemExit(f"bad lines for {it.get('id')}: {it.get('lines')!r}")
        if not isinstance(it.get("metric"), str):
            raise SystemExit(f"bad metric for {it.get('id')}: {it.get('metric')!r}")

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C163", "theme": "vision_v9_smoke", "gate": GATE,
            "timestamp": ts(), "attempted": False,
            "reason": f"gpu_free={free} or no weights",
            "vl_gate_v9_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C163_VISION_V9_SMOKE.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image

    RUN.mkdir(parents=True, exist_ok=True)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows, n_ok = [], 0
    try:
        for it in man["items"]:
            png = ROOT / it["path"]
            ocr = ocr_image(png, prefer="vl", vl_backend=backend)
            text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            ocr_ok = soft_ocr_ok(text, it["lines"])
            got, atom_ok = parse_metric(text, it["metric"], it["expected"])
            ok = bool(ocr_ok and atom_ok)
            n_ok += int(ok)
            rows.append({
                "id": it["id"], "kind": it["kind"], "metric": it["metric"],
                "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                "got": got, "expected": it["expected"], "ocr_preview": text[:360],
            })
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

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = rate >= GATE and n >= 16
    claim = bool(gate_pass)
    scope = "r50plus_v9_torn_barcode_fx_ghost_qr_n>=16_c162_parse_qwen35_2b_c163" if claim else None
    out = {
        "cycle": "C163",
        "theme": "vision_v9_smoke",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "vl_gate_v9_claim": claim,
        "claim_scope": scope,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "harder_than": "v8",
        "parse_ref": "C162 unglue digit.status",
        "fixture_regen": "C160 arg-order fix",
        "gate2_3_untouched": True,
        "v0_v8_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "Real VL smoke on V9. Claim only if rate>=0.6. Gate2/3 untouched.",
    }
    J(DOC / "C163_VISION_V9_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C163b_VISION_GATE_V9_CLAIM.json", {
            "kind": "vision_gate_v9_claim",
            "timestamp": ts(),
            "vl_gate_v9_claim": True,
            "rate": rate,
            "n": n, "n_ok": n_ok,
            "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v8_untouched": True,
            "gen11": "HOLD",
            "cycle": "C163",
        })
    print(json.dumps({
        "cycle": "C163", "rate": rate, "n_ok": n_ok, "n": n,
        "fail": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
