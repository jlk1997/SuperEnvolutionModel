# -*- coding: utf-8 -*-
"""C144: Vision V7 smoke on C143 fixtures. Claim only if rate>=0.6.
Gate2/3 untouched. gen11 HOLD. No fake VL.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v7"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v7_c144"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.\d+|\d+", " ".join(lines))
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
    man_path = FIX / "manifest.json"
    if not man_path.is_file():
        print(json.dumps({"error": "missing_manifest", "hint": "run C143 first"}))
        return 1
    if not WEIGHTS.is_dir():
        print(json.dumps({"error": "no_vl_weights"}))
        return 1
    free = gpu_free_mib()
    if free < 2000:
        out = {
            "cycle": "C144",
            "theme": "vision_v7_smoke",
            "gate": GATE,
            "timestamp": ts(),
            "attempted": False,
            "reason": f"gpu_free_mib={free}",
            "pass": False,
            "claim": False,
            "vl_gate_v7_claim": False,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
        }
        J(DOC / "C144_VISION_V7_SMOKE.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    man = json.loads(man_path.read_text(encoding="utf-8"))
    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image

    RUN.mkdir(parents=True, exist_ok=True)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows = []
    n_ok = 0
    items = man["items"]
    try:
        for it in items:
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
                "got": got, "expected": it["expected"], "ocr_preview": text[:280],
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
    rate = n_ok / n if n else 0.0
    gate_pass = rate >= GATE and n >= 14
    claim = bool(gate_pass)
    scope = "r50plus_v7_occlusion_tiny_stamped_n>=14_softocr_atom_qwen35_2b" if claim else None
    out = {
        "cycle": "C144",
        "theme": "vision_v7_smoke_occlusion_tiny_stamped",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "weights": "models/Qwen3.5-2B",
        "fixtures": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "gpu_free_mib_start": free,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": gate_pass,
        "vl_gate_v7_claim": claim,
        "claim_scope": scope,
        "rows": rows,
        "prior_v0_v6_untouched": True,
        "open_domain_benchmark": False,
        "pass": True,
        "claim": claim,
        "note": "Honest V7 smoke. Claim only if rate>=0.6. Failures kept in rows.",
    }
    J(DOC / "C144_VISION_V7_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C144b_VISION_GATE_V7_CLAIM.json", {
            "kind": "vision_gate_v7_claim",
            "timestamp": ts(),
            "vl_gate_v7_claim": True,
            "rate": round(rate, 4),
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v6_untouched": True,
            "gen11": "HOLD",
        })
    print(json.dumps({
        "cycle": "C144", "rate": round(rate, 4), "n": n, "n_ok": n_ok, "claim": claim,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

