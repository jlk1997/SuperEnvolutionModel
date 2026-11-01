# -*- coding: utf-8 -*-
"""Write STAGE_ANT_V025 + CHECKPOINT_NOW for 蚁算 v0.2.5."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def load(docs: Path, name: str):
    p = docs / name
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    stamp = datetime.now().strftime("%Y-%m-%d")

    plan = (docs / f"蚁算_v025_升级计划_{stamp}.md").is_file()
    shadow = load(docs, f"SHADOW_WRITE_GUARDED_PILOT_{stamp}.json")
    dissolve = load(docs, f"DISSOLVE_DASHBOARD_{stamp}.json")
    delta = load(docs, f"DISSOLVE_DELTA_V025_{stamp}.json")
    above = load(docs, f"ABOVE_SCHEDULES_THICKEN_V025_{stamp}.json")
    vision = load(docs, f"VISION_FIXTURE_HARNESS_{stamp}.json")
    cost = load(docs, f"COST_LEDGER_DUAL_VS_AGENT_{stamp}.json")
    registry = (root / "evo" / "office" / "fixtures" / "vision_atom_registry.json").is_file()
    mm = (docs / "MULTIMODAL_TRACK.md").is_file()

    blocks = {
        "plan_doc": plan,
        "shadow_write_guarded": bool(shadow and shadow.get("pass")),
        "dissolve_refresh": bool(dissolve and dissolve.get("summary", {}).get("pass")),
        "dissolve_delta": bool(delta and delta.get("pass")),
        "above_schedules_v025": bool(above and above.get("summary", {}).get("thickening_pass")),
        "vision_harness": bool(vision and vision.get("pass")),
        "vision_registry": registry,
        "multimodal_track": mm,
        "cost_ledger": bool(cost and cost.get("pass")),
    }
    ready = all(blocks.values())
    missing = [k for k, v in blocks.items() if not v]
    status = "STAGE_READY" if ready else "STAGE_BLOCKED"

    micro = (above or {}).get("gpu_micro") or {}
    micro_note = (
        f"GPU micro found={micro.get('found')} running={micro.get('running')} "
        f"blocker={((above or {}).get('summary') or {}).get('blocker')}"
    )

    stage = f"""# 蚁算 v0.2.5 STAGE

更新：{now}（Asia/Shanghai）

状态：**{status}**（STAGE_READY_V025={'YES' if ready else 'NO'}）

| 验收项 | 结果 |
| --- | --- |
| 升级计划 docs/蚁算_v025_升级计划_{stamp}.md | {'PASS' if blocks['plan_doc'] else 'FAIL'} |
| Shadow 写护栏 pilot（超只读） | {'PASS' if blocks['shadow_write_guarded'] else 'FAIL'} |
| Dissolve 看板刷新 | {'PASS' if blocks['dissolve_refresh'] else 'FAIL'} |
| Dissolve delta v0.2.5 | {'PASS' if blocks['dissolve_delta'] else 'FAIL'} |
| above_schedules 加厚 v0.2.5 | {'PASS' if blocks['above_schedules_v025'] else 'FAIL'} |
| 蚁算-视 registry+harness | {'PASS' if blocks['vision_harness'] and blocks['vision_registry'] else 'FAIL'} |
| MULTIMODAL_TRACK 更新 | {'PASS' if blocks['multimodal_track'] else 'FAIL'} |
| Dual vs Agent 成本账本 stub | {'PASS' if blocks['cost_ledger'] else 'FAIL'} |

Gate **0.6** ｜ Gate2/3 CLAIM 未卸 ｜ 无假 VL 训分 ｜ 不重开 burned pack

唯一缺口：{('无 → STAGE_READY_V025' if ready else ', '.join(missing))}

GPU 微跑备注：{micro_note}

视轨：PROTOCOL+REGISTRY+HARNESS；**OPEN_ONLY_VL** 训练仍等本地 VL 权重。
"""
    (docs / "STAGE_ANT_V025.md").write_text(stage, encoding="utf-8")

    cost_agg = (cost or {}).get("aggregate") or {}
    cp = f"""# CHECKPOINT_NOW — 2026-10-18 — 蚁算模型

时间：{now}（Asia/Shanghai）

产品名：**蚁算模型**（上海话 / Ant Compute）｜ 引擎代号 Envolution  
阶段交付：`docs/STAGE_ANT_V025.md` → **{status}**（v0.2.5）  
计划：`docs/蚁算_v025_升级计划_{stamp}.md`  
上一版：v0.1 STAGE_READY @90f7536

Gate **0.6**. **Gate2 CLAIMED**. **Gate3 CLAIMED** (Branch A transfer). 1.5B. No fake VL scores.

## Scores (unchanged claims)
- Gate2 CLAIMED → `docs/GATE2_OFFICE_JUDGE_2026-10-17.json`
- Gate3 CLAIMED gen10 → `docs/GATE3_GEN10_JUDGE_2026-10-18.json`
- Epoch C product path COMPLETE（四族 bare=1.0 · D=0）
- mid-n observational only → does not rewrite Gate2
- external local honest SFT → upstream_claim=false

## 蚁算 v0.2.5 本轮交付
- Write-guarded shadow：`docs/SHADOW_WRITE_GUARDED_PILOT_{stamp}.json` → pass={bool(shadow and shadow.get('pass'))}
- Dissolve 刷新 + delta：`docs/DISSOLVE_DASHBOARD_{stamp}.json` / `docs/DISSOLVE_DELTA_V025_{stamp}.json`
- above_schedules v025：`docs/ABOVE_SCHEDULES_THICKEN_V025_{stamp}.json` → thickening_pass={bool(above and (above.get('summary') or {}).get('thickening_pass'))}；{micro_note}
- 成本账本：`docs/COST_LEDGER_DUAL_VS_AGENT_{stamp}.json` → dual_steps_mean={cost_agg.get('dual_steps_mean')} agent_steps_mean={cost_agg.get('agent_steps_mean')} dual_fail={cost_agg.get('dual_fail_rate_mean')} agent_fail={cost_agg.get('agent_fail_rate_mean')}
- 蚁算-视 v0.2.5：registry + harness `docs/VISION_FIXTURE_HARNESS_{stamp}.json`；`vl_gate_claim=false`

## 多模态轨（蚁算-视）
- 协议+schema+fixture+registry+harness 齐；**禁止假训**
- OPEN_ONLY_VL：等 `models/` VL 权重

## Next knife (v0.3)
- 写护栏 → 真实用户目录 + 二次确认
- 成本账本接 model_turn_log 补 tokens
- GPU micro 收束后刷新 ABOVE_SCHEDULES_THICKEN_V025（不 mint Gate2）
- VL 权重到位 → V0 smoke

Gate 0.6 · 不卸 CLAIM · 不重开 burned · 不做假 VL。
"""
    (docs / "CHECKPOINT_NOW.md").write_text(cp, encoding="utf-8")
    print(json.dumps({"status": status, "ready": ready, "missing": missing, "blocks": blocks}, ensure_ascii=False))


if __name__ == "__main__":
    main()
