# -*- coding: utf-8 -*-
"""C119: Stage docs for C113-C118."""
from __future__ import annotations
import json, subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(name):
    p = DOC / f"{name}.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c113, c114, c115, c116, c117, c118 = (
        load("C113_U2C_GROW_PAIRS"),
        load("C114_U2C_ABSORB_PUSH"),
        load("C115_HARDEN_ANT_CAPTURE"),
        load("C116_V5_DESIGN_BATCH"),
        load("C117_DISSOLVE_COST_REFRESH"),
        load("C118_GEN11_HOLD"),
    )
    trained = (c114.get("trained") or {}).get("rate")
    lines = [
        "# STAGE_ANT_R50PLUS",
        "",
        f"Updated: {ts()} (Asia/Shanghai)",
        "",
        "**R50PLUS_CONTINUATION=YES** (C113-C119)",
        "",
        f"- **C113** U2C grow pairs n={c113.get('n_pairs_total')} heldout={c113.get('heldout_n')} pass={c113.get('pass')}",
        f"- **C114** U2C absorb push trained={trained} rate_gate_pass={c114.get('rate_gate_pass')} claim={c114.get('claim')} ceiling={bool(c114.get('ceiling'))}",
        f"- **C115** harden capture test_rate={(c115.get('tests') or {}).get('rate')} pass={c115.get('pass')}",
        f"- **C116** V5 design n={c116.get('n_fixtures')} smoke_rate={(c116.get('smoke') or {}).get('rate')} v5_claim={c116.get('vl_gate_v5_claim')}",
        f"- **C117** dissolve/cost refresh pass={c117.get('pass')}",
        f"- **C118** gen11 {c118.get('decision')} seal={c118.get('seal')}",
        f"- **C119** docs",
        "",
        "## Iron",
        "Gate **0.6**. Gate2/3 untouched. gen11 HOLD unless fresh>=0.99. Dense vision default **bare**. No fake VL.",
        "",
        "## Evidence",
        "`docs/r50/C113_*.json` ... `C118_*.json` + `scripts/ant_capture_office_lib.py` + `docs/蚁算视_VL_GATE_V5_PROTOCOL.md`",
        "",
    ]
    (ROOT / "docs" / "STAGE_ANT_R50PLUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    stage = {
        "cycle": "C119",
        "theme": "docs_stage_c113_c118",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "summary": {
            "c114_trained_rate": trained,
            "c114_rate_gate_pass": c114.get("rate_gate_pass"),
            "c114_claim": c114.get("claim"),
            "c115_test_rate": (c115.get("tests") or {}).get("rate"),
            "c116_v5_claim": c116.get("vl_gate_v5_claim"),
            "gen11": c118.get("decision"),
        },
        "pass": True,
        "claim": False,
    }
    J(DOC / "C119_DOCS.json", stage)
    (ROOT / "docs" / "STAGE_ANT_C119.md").write_text(
        f"# STAGE_ANT_C119\n\nSee STAGE_ANT_R50PLUS.md\n\nUpdated: {ts()}\n",
        encoding="utf-8",
    )
    # append loop ledger briefly
    loop = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    block = (
        f"\n## C113-C119 ({ts()})\n"
        f"- C113 grow pairs → C114 absorb push (trained={trained}, gate_pass={c114.get('rate_gate_pass')}, claim={c114.get('claim')})\n"
        f"- C115 capture harden tests={(c115.get('tests') or {}).get('rate')}\n"
        f"- C116 V5 design/smoke claim={c116.get('vl_gate_v5_claim')}\n"
        f"- C117 dashboards · C118 gen11 HOLD · C119 docs\n"
        f"- Iron: Gate 0.6, Gate2/3 untouched\n"
    )
    if loop.is_file():
        loop.write_text(loop.read_text(encoding="utf-8") + block, encoding="utf-8")
    else:
        loop.write_text("# 蚁算 R50PLUS LOOP\n" + block, encoding="utf-8")
    print(json.dumps({"cycle": "C119", "pass": True, "summary": stage["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
