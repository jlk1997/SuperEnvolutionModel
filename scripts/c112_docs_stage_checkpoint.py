# -*- coding: utf-8 -*-
"""C112: Update STAGE/CHECKPOINT/loop for C107-C111."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs"
R50 = DOC / "r50"

def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def load(name):
    p = R50 / name
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None

def main():
    c107 = load("C107_VISION_V4_HELDOUT.json") or {}
    c108 = load("C108_U2C_ABSORB_LORA.json") or {}
    c109 = load("C109_ANT_CAPTURE_OFFICE_CLI.json") or {}
    c110 = load("C110_REPLACE_HARDER_COST.json") or {}
    c111 = load("C111_GEN11_HOLD.json") or {}
    c101 = load("C101_VISION_V4_MULTIHOP.json") or {}
    now = ts()
    absorb = c108.get("absorb") or {}
    bare = c108.get("bare") or {}
    trained = c108.get("trained") or {}
    dense = c108.get("dense_route") or {}
    stage = "# STAGE_ANT_R50PLUS\n\nUpdated: %s (Asia/Shanghai)\n\n**R50PLUS_CONTINUATION=YES** (C107-C112)\n\n" % now
    stage += "- **C107** V4 heldout n=%s rate=%s claim=%s pass=%s\n" % (c107.get("n"), c107.get("rate"), c107.get("vl_gate_v4_heldout_claim"), c107.get("pass"))
    stage += "- **C108** U2C absorb ok=%s bare=%s trained=%s delta=%s dense_bare=%s pass=%s\n" % (absorb.get("ok"), bare.get("rate"), trained.get("rate"), c108.get("delta_trained_minus_bare"), dense.get("dense_prefers_bare"), c108.get("pass"))
    stage += "- **C109** CLI ok=%s paid=%s entry=%s pass=%s\n" % (c109.get("ok"), c109.get("paid_got"), c109.get("cli_entry"), c109.get("pass"))
    stage += "- **C110** replace bare=%s replace=%s ratio=%s pass=%s\n" % (c110.get("bare_rate"), c110.get("replace_rate"), c110.get("step_ratio_agent_over_bare"), c110.get("pass"))
    stage += "- **C111** gen11 %s seal=%s\n- **C112** docs\n\n" % (c111.get("decision"), c111.get("seal_opened"))
    stage += "## Prior\n- C101 V4 claim=%s rate=%s\n\n" % (c101.get("vl_gate_v4_claim"), c101.get("rate"))
    stage += "## Iron\nGate **0.6**. Gate2/3 untouched. gen11 HOLD unless fresh>=0.99. Dense vision default **bare**. No fake VL.\n\n"
    stage += "## Evidence\n`docs/r50/C107_*.json` ... `C111_*.json` · `scripts/ant_capture_office.py`\n"
    (DOC / "STAGE_ANT_R50PLUS.md").write_text(stage, encoding="utf-8")
    ck = "# CHECKPOINT_NOW · %s · 蚁算模型\n\n**R50PLUS=YES**\n\nGate **0.6**. Gate2/3 untouched.\n" % now
    ck += "**C107 V4 heldout**: n=%s rate=%s claim=%s\n" % (c107.get("n"), c107.get("rate"), c107.get("vl_gate_v4_heldout_claim"))
    ck += "**C108 U2C**: bare=%s trained=%s delta=%s\n" % (bare.get("rate"), trained.get("rate"), c108.get("delta_trained_minus_bare"))
    ck += "**C109 CLI**: %s ok=%s paid=%s\n" % (c109.get("cli_entry"), c109.get("ok"), c109.get("paid_got"))
    ck += "**C110**: bare=%s replace=%s ratio=%s\n" % (c110.get("bare_rate"), c110.get("replace_rate"), c110.get("step_ratio_agent_over_bare"))
    ck += "gen11 seal=%s decision=%s\nProduct vision default: **bare**.\n" % (c111.get("seal_opened"), c111.get("decision"))
    (DOC / "CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")
    loop_path = DOC / "蚁算_R50PLUS_LOOP.md"
    prev = loop_path.read_text(encoding="utf-8") if loop_path.is_file() else "# 蚁算 R50PLUS LOOP\n\n"
    add = "\n## C107-C112 @ %s\n- C107 rate=%s claim=%s\n- C108 bare=%s trained=%s delta=%s\n- C109 pass=%s paid=%s\n- C110 bare=%s ratio=%s\n- C111 %s seal=%s\n" % (now, c107.get("rate"), c107.get("vl_gate_v4_heldout_claim"), bare.get("rate"), trained.get("rate"), c108.get("delta_trained_minus_bare"), c109.get("pass"), c109.get("paid_got"), c110.get("bare_rate"), c110.get("step_ratio_agent_over_bare"), c111.get("decision"), c111.get("seal_opened"))
    loop_path.write_text(prev.rstrip() + "\n" + add, encoding="utf-8")
    proto = DOC / "蚁算视_VL_GATE_V4_PROTOCOL.md"
    if proto.is_file():
        txt = proto.read_text(encoding="utf-8")
        if "V4 Heldout" not in txt:
            txt = txt.rstrip() + "\n\n## V4 Heldout (C107+)\n- Fixtures: evo/office/fixtures/vision_images_v4_heldout\n- Disjoint from C101 train\n- Claim: vl_gate_v4_heldout_claim=true only if n>=8 rate>=0.6\n- Updated: %s\n" % now
            proto.write_text(txt, encoding="utf-8")
    R50.mkdir(parents=True, exist_ok=True)
    dissolve = {"cycle": "C112", "theme": "docs_stage_checkpoint", "gate": 0.6, "pointers": ["C107","C108","C109","C110","C111"], "v4_heldout_claim": c107.get("vl_gate_v4_heldout_claim"), "v4_claim_prior": c101.get("vl_gate_v4_claim"), "timestamp": now, "pass": True}
    (R50 / "C112_DOCS.json").write_text(json.dumps(dissolve, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOC / "STAGE_ANT_C112.md").write_text("# STAGE_ANT_C112\n\nSee STAGE_ANT_R50PLUS.md\n\nUpdated: %s\n" % now, encoding="utf-8")
    print(json.dumps({"cycle": "C112", "pass": True, "v4_heldout_claim": c107.get("vl_gate_v4_heldout_claim"), "c108_pass": c108.get("pass"), "c110_pass": c110.get("pass")}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
