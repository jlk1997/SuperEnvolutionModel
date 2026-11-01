# -*- coding: utf-8 -*-
"""C77: Smoke V3 heldout harder set with bare Qwen3.5-2B. Claim only if rate>=0.6 and n>=8."""
from __future__ import annotations
import gc, json, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from evo.office.vision_route import route_vision
from scripts.vision_softmatch import softmatch

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
IMG = ROOT / "evo/office/fixtures/vision_images_v3_heldout"
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v2h_style_lora"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def main():
    if not IMG.is_dir():
        raise SystemExit("run c76 fixtures first")
    ids = sorted(p.stem for p in IMG.glob("*.png"))
    # Always evaluate with bare for claim; also record route decisions
    bare = RealVlBackend(WEIGHTS, max_new_tokens=180)
    items = []
    n_ok = 0
    routes = []
    for fid in ids:
        meta = json.loads((IMG / f"{fid}.json").read_text(encoding="utf-8"))
        task = meta.get("task") or "caption"
        gold = str(meta.get("gold") or "")
        decision = route_vision(task, meta=meta, adapter_path=ADAPTER)
        routes.append({"id": fid, **decision.as_dict()})
        # claim path: always bare (policy also says bare for dense tables; heldout claim is bare)
        try:
            pred = bare.predict(VisionObs(image_path=IMG / f"{fid}.png", task=task, gold=gold))
            text = clean(pred.text or "")
            ok = softmatch(text, gold, task)
            err = None
        except Exception as e:
            text, ok, err = "", False, f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        items.append({"id": fid, "task": task, "domain": decision.domain, "route": decision.mode, "gold": gold, "pred_head": text[:280], "ok": ok, "error": err})
    bare.unload()
    gc.collect()

    n = len(items)
    rate = n_ok / n if n else 0.0
    claim = bool(rate >= GATE and n >= 8)
    claim_path = ROOT / "docs/r50/C77c_vision_gate_v3_heldout_claim.json"
    if claim:
        J(claim_path, {
            "kind": "vision_gate_v3_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v3_heldout_claim": True,
            "rate": round(rate, 4),
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "claim_scope": "r50plus_v3_heldout_harder_drawn_n>=8_softmatch_qwen35_2b_bare",
            "backend": "bare",
            "gate2_3_untouched": True,
            "v1_v2_v3_dense_untouched": True,
        })
    else:
        J(claim_path, {
            "kind": "vision_gate_v3_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v3_heldout_claim": False,
            "rate": round(rate, 4),
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "reason": "below_gate_or_n",
            "gate2_3_untouched": True,
            "v1_v2_v3_dense_untouched": True,
        })

    # route consistency: all table_cells should be bare
    route_ok = all(r["mode"] == "bare" for r in routes if r["task"] in ("table_cells", "table") or r["domain"] == "dense_table")

    payload = {
        "kind": "r50plus_c77_vision_v3_heldout_smoke",
        "timestamp": ts(),
        "gate": GATE,
        "dir": "evo/office/fixtures/vision_images_v3_heldout",
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": claim,
        "vl_gate_v3_heldout_claim": claim,
        "items": items,
        "routes": routes,
        "route_tables_all_bare": route_ok,
        "innovation": "Harder V3 heldout claim; routing recorded; claim bare-only",
        "gate2_3_untouched": True,
        "v1_v2_v3_dense_untouched": True,
    }
    J(ROOT / "docs/r50/C77_vision_v3_heldout_smoke.json", payload)
    print(json.dumps({
        "rate": round(rate, 4),
        "n_ok": n_ok,
        "n": n,
        "claim": claim,
        "route_tables_all_bare": route_ok,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
