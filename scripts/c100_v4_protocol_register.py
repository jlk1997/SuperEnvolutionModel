# -*- coding: utf-8 -*-
"""C100: Register Vision V4 multi-hop protocol (docs already staged). Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
PROTO = ROOT / "docs" / "蚁算视_VL_GATE_V4_PROTOCOL.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def main():
    DOC.mkdir(parents=True, exist_ok=True)
    out = {
        "cycle": "C100",
        "theme": "vision_v4_protocol_register",
        "gate": 0.6,
        "protocol_path": "docs/蚁算视_VL_GATE_V4_PROTOCOL.md",
        "protocol_exists": PROTO.is_file(),
        "rules": {"n_min": 8, "rate_min": 0.6, "require_ocr_and_atom": True, "open_domain": False},
        "claim": False,
        "pass": PROTO.is_file(),
        "timestamp": ts(),
        "note": "Protocol only; claim deferred to C101 run.",
    }
    p = DOC / "C100_V4_PROTOCOL.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("cycle", "pass", "protocol_exists")}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
