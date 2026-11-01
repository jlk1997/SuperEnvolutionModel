# -*- coding: utf-8 -*-
"""Rewrite CHECKPOINT_NOW + STAGE_ANT_V01 with 蚁算 naming and STAGE_READY."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    # load evidence flags
    def load(name: str):
        p = docs / name
        if not p.is_file():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    stamp = datetime.now().strftime("%Y-%m-%d")
    dash = load(f"DISSOLVE_DASHBOARD_{stamp}.json")
    shadow = load(f"SHADOW_READONLY_PILOT_{stamp}.json")
    above = load(f"ABOVE_SCHEDULES_THICKEN_{stamp}.json")

    blocks = {
        "dissolve": bool(dash and dash.get("summary", {}).get("pass")),
        "shadow_ro": bool(shadow and shadow.get("pass")),
        "above": bool(above and above.get("summary", {}).get("thickening_pass")),
        "naming_docs": (docs / "蚁算_NAMING.md").is_file()
        and (docs / "蚁算模型_主结构与升级地图_2026-10-18.md").is_file(),
        "vision_protocol": (docs / "蚁算视_VL_GATE_PROTOCOL.md").is_file(),
        "vision_schema": (docs / "schemas" / "vision_use_log_event.json").is_file(),
        "vision_fixture": (root / "evo" / "office" / "fixtures" / "vision_use_log_fixture.jsonl").is_file(),
        "vision_atom_stub": (root / "runs" / "capabilities" / "vision_table_uselog" / "atom_stub.json").is_file(),
    }
    ready = all(blocks.values())
    status = "STAGE_READY" if ready else "STAGE_BLOCKED"
    missing = [k for k, v in blocks.items() if not v]

    stage = f"""# 蚁算 v0.1 STAGE

更新：{now}（Asia/Shanghai）

状态：**{status}**

| 交付项 | 结果 |
| --- | --- |
| 蚁算主结构+升级地图+NAMING | {'PASS' if blocks['naming_docs'] else 'FAIL'} |
| Dissolve 四族仪表盘 | {'PASS' if blocks['dissolve'] else 'FAIL'} |
| Shadow 只读 pilot（超 smoke） | {'PASS' if blocks['shadow_ro'] else 'FAIL'} |
| above_schedules 诚实加厚 | {'PASS' if blocks['above'] else 'FAIL'} |
| 蚁算-视 protocol+schema+fixture+atom stub | {'PASS' if all(blocks[k] for k in ['vision_protocol','vision_schema','vision_fixture','vision_atom_stub']) else 'FAIL'} |

Gate **0.6** · Gate2/3 CLAIM 未卸 · 无假 VL 训分 · 不重开 burned pack

唯一阻塞：{('无 — STAGE_READY' if ready else ', '.join(missing))}

多模态轨：协议与 stubs 已就绪；**OPEN_ONLY_VL** 训练刀仍等本地 VL 权重（V0）。
"""
    (docs / "STAGE_ANT_V01.md").write_text(stage, encoding="utf-8")

    cp = f"""# CHECKPOINT_NOW · 2026-10-18 · 蚁算模型

时间：{now}（Asia/Shanghai）

产品名：**蚁算模型**（上海蚁算 / Ant Compute） · 引擎代号 Envolution  
命名：`docs/蚁算_NAMING.md` · 主结构与升级地图：`docs/蚁算模型_主结构与升级地图_2026-10-18.md`  
阶段单：`docs/STAGE_ANT_V01.md` → **{status}**

Gate **0.6**. **Gate2 CLAIMED**. **Gate3 CLAIMED** (Branch A transfer). 1.5B. No fake VL scores.

## Scores (unchanged claims)
- Gate2 CLAIMED — `docs/GATE2_OFFICE_JUDGE_2026-10-17.json`
- Gate3 CLAIMED gen10 — `docs/GATE3_GEN10_JUDGE_2026-10-18.json`
- Epoch C product path COMPLETE（四族 bare=1.0 · D=0）
- mid-n observational only — does not rewrite Gate2
- external local honest SFT — upstream_claim=false

## 蚁算 v0.1 本轮交付
- Dissolve 仪表盘：`docs/DISSOLVE_DASHBOARD_{stamp}.json` · pass={blocks['dissolve']}
- Shadow 只读 pilot：`docs/SHADOW_READONLY_PILOT_{stamp}.json` · pass={blocks['shadow_ro']}
- above_schedules 加厚：`docs/ABOVE_SCHEDULES_THICKEN_{stamp}.json` · pass={blocks['above']}

## 多模态轨 · 蚁算-视（protocol+stubs，非 CLAIM）
- 协议：`docs/蚁算视_VL_GATE_PROTOCOL.md`
- schema：`docs/schemas/vision_use_log_event.json`
- fixture：`evo/office/fixtures/vision_use_log_fixture.jsonl`
- atom stub：`runs/capabilities/vision_table_uselog/atom_stub.json`（status=stub_pending_weights）
- `vl_gate_claim=false` · `weights_local=false` · **禁止假训**

### OPEN_ONLY_VL
Epoch D / V0+ GPU 训练刀 HARD defer until local VL/vision weights under models/.  
Inventory already FAIL (Qwen2.5/3.5 text only). Protocol+stubs may advance without weights.

## Next knife
- 文本轨产品化：一键复现四族 + dissolve-first 演示
- 视轨：权重就位后开 V0 smoke（见 VL Gate 协议）
- Fleet / n≈800 仍冻结

Gate 0.6 · 不卸 CLAIM · 不重开 burned · 不假 VL。
"""
    (docs / "CHECKPOINT_NOW.md").write_text(cp, encoding="utf-8")

    # multimodal track pointer short file
    mm = f"""# MULTIMODAL_TRACK · 蚁算-视

更新：{now}

状态：PROTOCOL_AND_STUBS_READY · TRAINING_DEFER_NO_WEIGHTS

指针：
- `docs/蚁算视_VL_GATE_PROTOCOL.md`
- `docs/schemas/vision_use_log_event.json`
- `evo/office/fixtures/vision_use_log_fixture.jsonl`
- `runs/capabilities/vision_table_uselog/atom_stub.json`

CLAIM：无。OPEN_ONLY_VL 仍有效。
"""
    (docs / "MULTIMODAL_TRACK.md").write_text(mm, encoding="utf-8")
    print(json.dumps({"status": status, "blocks": blocks, "missing": missing}, ensure_ascii=False))


if __name__ == "__main__":
    main()
