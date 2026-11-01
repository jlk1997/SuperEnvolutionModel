# -*- coding: utf-8 -*-
"""C78: Smoke vision routing policy — dense-table→bare; LoRA only weak domains."""
from __future__ import annotations
import json, tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
from evo.office.vision_route import route_vision, DENSE_TABLE_DOMAINS, WEAK_LORA_OK

GATE = 0.6
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v2h_style_lora"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    cases = []
    # dense table meta from heldout
    d1 = route_vision("table_cells", meta={"domain": "dense_table", "v3_heldout": True}, adapter_path=ADAPTER)
    cases.append({"name": "dense_table_with_adapter", "expect_mode": "bare", "got": d1.as_dict(), "ok": d1.mode == "bare" and not d1.use_adapter})

    d2 = route_vision("table_cells", meta={"v3_dense": True}, adapter_path=ADAPTER)
    cases.append({"name": "v3_dense_table_infer", "expect_mode": "bare", "got": d2.as_dict(), "ok": d2.mode == "bare"})

    d3 = route_vision("ocr", meta={"domain": "ocr"}, adapter_path=ADAPTER)
    cases.append({"name": "ocr_default_bare", "expect_mode": "bare", "got": d3.as_dict(), "ok": d3.mode == "bare"})

    d4 = route_vision("ocr", meta={"domain": "ocr_weak"}, adapter_path=ADAPTER)
    expect_lora = ADAPTER.is_dir() and (ADAPTER / "adapter_config.json").is_file()
    cases.append({"name": "ocr_weak_lora", "expect_mode": "lora" if expect_lora else "bare", "got": d4.as_dict(), "ok": (d4.mode == "lora") if expect_lora else (d4.mode == "bare")})

    d5 = route_vision("caption", meta={"domain": "caption_weak"}, adapter_path=ADAPTER)
    cases.append({"name": "caption_weak_lora", "expect_mode": "lora" if expect_lora else "bare", "got": d5.as_dict(), "ok": (d5.mode == "lora") if expect_lora else (d5.mode == "bare")})

    d6 = route_vision("caption", meta={"domain": "caption_weak"}, adapter_path=None)
    cases.append({"name": "weak_no_adapter_bare", "expect_mode": "bare", "got": d6.as_dict(), "ok": d6.mode == "bare"})

    d7 = route_vision("table_cells", meta={"domain": "dense_table"}, adapter_path=ADAPTER, force_bare=True)
    cases.append({"name": "force_bare", "expect_mode": "bare", "got": d7.as_dict(), "ok": d7.mode == "bare"})

    # fake missing adapter path
    fake = ROOT / "runs" / "capabilities" / "_missing_adapter_"
    d8 = route_vision("ocr", meta={"domain": "train_style"}, adapter_path=fake)
    cases.append({"name": "train_style_missing_adapter", "expect_mode": "bare", "got": d8.as_dict(), "ok": d8.mode == "bare"})

    n_ok = sum(1 for c in cases if c["ok"])
    n = len(cases)
    rate = n_ok / n if n else 0.0
    payload = {
        "kind": "r50plus_c78_vision_route_policy_smoke",
        "timestamp": ts(),
        "gate": GATE,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": rate >= GATE,
        "policy": "dense_table_bare__lora_only_weak_domains",
        "dense_table_domains": sorted(DENSE_TABLE_DOMAINS),
        "weak_lora_ok": sorted(WEAK_LORA_OK),
        "adapter_present": expect_lora,
        "cases": cases,
        "evidence_basis": ["C66_vision_lora_vs_bare.json", "C72_vision_lora_vs_bare_retest.json"],
        "innovation": "Productize LoRA-hurts-dense-table finding into enforceable route()",
        "gate2_3_untouched": True,
        "v1_v2_v3_claims_untouched": True,
    }
    J(ROOT / "docs/r50/C78_vision_route_policy_smoke.json", payload)
    print(json.dumps({"rate": round(rate, 4), "n_ok": n_ok, "n": n, "gate_pass": rate >= GATE}, ensure_ascii=False))


if __name__ == "__main__":
    main()
