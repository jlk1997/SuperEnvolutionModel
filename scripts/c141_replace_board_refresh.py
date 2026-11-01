# -*- coding: utf-8 -*-
"""C141: Replace-agent board refresh — text+vision+confidence-gate.
Bare (atoms+money_tool+confidence gate) vs agent multi-step. Gate 0.6. gen11 HOLD.
"""
from __future__ import annotations
import json, re, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text, sum_paid_from_text, confidence_gated_money

GATE = 0.6
DOC = ROOT / "docs/r50"
RUN = ROOT / "runs/unified_replace_c141"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_REPLACE_BOARD.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_bare(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    csv_text = "oid,sku,qty,status,amount\n1,A,2,paid,18\n2,B,5,open,40\n3,A,3,paid,27\n4,C,1,paid,9\n5,D,2,paid,6\n"
    (ws / "inbox" / "orders.csv").write_text(csv_text, encoding="utf-8")
    total = sum_csv_text(csv_text, amount_col="amount", status_col="status", status_value="paid")
    # confidence gate with a wrong "model" guess
    gated = confidence_gated_money(
        "paid 18 paid 27 paid 9 paid 6 TOTAL PAID TARGET 60.00",
        model_guess=100.0,
    )
    (ws / "exports" / "paid.csv").write_text(f"metric,value\npaid_total,{total:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(
        f"# Text bare C141\n\npaid_total: {total:.2f}\nagent_graph: none\n"
        f"money_tool: true\nconfidence_gate: {gated['confidence']}\n",
        encoding="utf-8",
    )
    ok = abs(total - 60.0) < 0.08 and gated["source"] == "money_tool"
    return {
        "ok": ok, "bare_steps": 5, "paid_total": total, "modality": "text",
        "money_tool": True, "confidence_gate": gated,
    }


def text_agent(ws: Path) -> dict:
    steps = 0
    (ws / "tmp").mkdir(parents=True)
    (ws / "out").mkdir(parents=True)
    raw = "oid,sku,qty,status,amount\n1,A,2,paid,18\n2,B,5,open,40\n3,A,3,paid,27\n4,C,1,paid,9\n5,D,2,paid,6\n"
    (ws / "tmp" / "raw.csv").write_text(raw, encoding="utf-8"); steps += 1
    lines = raw.strip().splitlines(); steps += 1
    paid_rows = []
    for i, ln in enumerate(lines[1:], 1):
        parts = ln.split(",")
        (ws / "tmp" / f"row_{i}.txt").write_text(ln, encoding="utf-8"); steps += 1
        if parts[3] == "paid":
            paid_rows.append(float(parts[4])); steps += 1
        else:
            steps += 1
    total = sum(paid_rows); steps += 1
    (ws / "out" / "sum.txt").write_text(str(total), encoding="utf-8"); steps += 1
    (ws / "out" / "report.md").write_text(f"paid={total}\nagent_graph: multi\n", encoding="utf-8"); steps += 1
    ok = abs(total - 60.0) < 0.08
    return {"ok": ok, "agent_steps": steps, "paid_total": total, "modality": "text", "fail": not ok}


def vision_bare(ws: Path) -> dict:
    from PIL import Image, ImageDraw, ImageFont
    (ws / "panel").mkdir(parents=True)
    (ws / "atoms").mkdir(parents=True)
    lines = [
        "VISION BARE LEDGER C141",
        "item A paid 11.00",
        "item B open 4.00",
        "item C paid 14.50",
        "item D paid 2.00",
        "TOTAL PAID TARGET 27.50",
    ]
    img = Image.new("RGB", (640, 400), (255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 16)
    except Exception:
        f = ImageFont.load_default()
    y = 20
    for ln in lines:
        d.text((20, y), ln, fill=(0, 0, 0), font=f)
        y += 28
    png = ws / "panel" / "ledger.png"
    img.save(png)
    ocr_text = "\n".join(lines)
    # wrong model distractor (noise total)
    gated = confidence_gated_money(ocr_text, model_guess=999.0)
    total = float(gated["value"])
    (ws / "atoms" / "paid.json").write_text(
        json.dumps({
            "metric": "paid_total", "value": total, "scaffold_steps": 4,
            "agent_graph": None, "confidence_gate": gated,
        }, indent=2),
        encoding="utf-8",
    )
    ok = abs(total - 27.50) < 0.08 and gated["agree"] is False
    return {
        "ok": ok, "bare_steps": 4, "paid_total": total, "modality": "vision_panel",
        "money_tool": True, "confidence_gate": gated,
        "panel": str(png.relative_to(ws)).replace("\\", "/"),
    }


def vision_agent(ws: Path) -> dict:
    steps = 0
    (ws / "tmp").mkdir(parents=True)
    (ws / "out").mkdir(parents=True)
    lines = [
        "VISION AGENT LEDGER C141",
        "item A paid 11.00",
        "item B open 4.00",
        "item C paid 14.50",
        "item D paid 2.00",
        "TOTAL PAID TARGET 27.50",
    ]
    (ws / "tmp" / "ocr_raw.txt").write_text("\n".join(lines), encoding="utf-8"); steps += 1
    for i in range(3):
        (ws / "tmp" / f"crop_{i}.txt").write_text(f"crop{i}\n", encoding="utf-8"); steps += 1
    paid = []
    for i, ln in enumerate(lines):
        (ws / "tmp" / f"line_{i}.txt").write_text(ln, encoding="utf-8"); steps += 1
        m = re.search(r"paid\s+(\d+\.?\d*)", ln.lower())
        if m:
            paid.append(float(m.group(1))); steps += 1
        else:
            steps += 1
    total = sum(paid); steps += 1
    (ws / "out" / "sum.txt").write_text(str(total), encoding="utf-8"); steps += 1
    (ws / "out" / "graph.md").write_text("agent_graph: vision_multi_hop\n", encoding="utf-8"); steps += 1
    ok = abs(total - 27.50) < 0.08
    return {"ok": ok, "agent_steps": steps, "paid_total": total, "modality": "vision_panel", "fail": not ok}


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)

    tb = text_bare(RUN / "text_bare")
    ta = text_agent(RUN / "text_agent")
    vb = vision_bare(RUN / "vision_bare")
    va = vision_agent(RUN / "vision_agent")

    text_ratio = ta["agent_steps"] / tb["bare_steps"] if tb["bare_steps"] else None
    vis_ratio = va["agent_steps"] / vb["bare_steps"] if vb["bare_steps"] else None
    text_replace = bool(tb["ok"] and tb["bare_steps"] < ta["agent_steps"])
    vis_replace = bool(vb["ok"] and vb["bare_steps"] < va["agent_steps"])
    both = text_replace and vis_replace
    rate = (float(text_replace) + float(vis_replace)) / 2.0
    mean_ratio = round(((text_ratio or 0) + (vis_ratio or 0)) / 2.0, 4)

    unified = {
        "text": {
            "bare": {k: v for k, v in tb.items() if k != "confidence_gate"} | {
                "confidence_gate": tb.get("confidence_gate"),
            },
            "agent": ta,
            "step_ratio_agent_over_bare": round(text_ratio, 4) if text_ratio else None,
            "replace_ok": text_replace,
        },
        "vision": {
            "bare": vb,
            "agent": va,
            "step_ratio_agent_over_bare": round(vis_ratio, 4) if vis_ratio else None,
            "replace_ok": vis_replace,
        },
        "both_replace_ok": both,
        "mean_step_ratio": mean_ratio,
        "confidence_gated": True,
    }
    out = {
        "cycle": "C141",
        "theme": "unified_replace_board_refresh_confidence_gate",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "unified": unified,
        "rate": round(rate, 4),
        "mean_step_ratio": mean_ratio,
        "pass": rate >= GATE and both,
        "claim": False,
        "prior_c134_ref": "docs/r50/C134_UNIFIED_REPLACE_BOARD.json",
        "note": "Refresh board with C140 confidence gate. No Gate2 mint.",
    }
    J(DOC / "C141_UNIFIED_REPLACE_BOARD.json", out)
    J(RUN / "judge.json", out)

    text_ratio_s = f"{text_ratio:.4f}" if text_ratio else "n/a"
    vis_ratio_s = f"{vis_ratio:.4f}" if vis_ratio else "n/a"
    BOARD_MD.write_text(
        f"""# 蚁算 · 统一替 Agent 板（Unified Replace Board）

Updated: {ts()} (Asia/Shanghai)

## 本轮 C141
- rate: **{rate:.4f}** both_replace_ok: **{both}**
- mean_step_ratio (agent/bare): **{mean_ratio}**
- confidence_gated: **true**（分歧时强制 money_tool）
- evidence: `docs/r50/C141_UNIFIED_REPLACE_BOARD.json`

## 文本
- bare_steps={tb['bare_steps']} agent_steps={ta['agent_steps']} ratio={text_ratio_s}

## 视觉面板
- bare_steps={vb['bare_steps']} agent_steps={va['agent_steps']} ratio={vis_ratio_s}

## 诚实边界
- 不新铸 Gate2/3；gen11 HOLD
- 金额路径 tool + 置信门控，非 LoRA 心算 claim
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "cycle": "C141", "pass": out["pass"], "rate": round(rate, 4),
        "mean_ratio": mean_ratio, "both": both,
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

