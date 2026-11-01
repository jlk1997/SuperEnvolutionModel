# -*- coding: utf-8 -*-
"""Aggregate office family dissolution.json into one dashboard JSON+md."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

FAMILIES = ("table", "report", "file", "shell")
CRITERION = 0.6


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_family(root: Path, family: str) -> dict:
    path = root / "runs" / "capabilities" / f"office_{family}_uselog" / "dissolution.json"
    if not path.is_file():
        return {
            "family": family,
            "found": False,
            "path": str(path),
            "bare_rate": None,
            "scaffold_rate": None,
            "dissolution": None,
            "bare_clears_gate": False,
            "internalized": False,
            "error": "missing_dissolution_json",
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "family": family,
        "found": True,
        "path": str(path),
        "bare_rate": data.get("bare_rate"),
        "scaffold_rate": data.get("scaffold_rate"),
        "dissolution": data.get("dissolution"),
        "bare_clears_gate": bool(data.get("bare_clears_gate")),
        "internalized": bool(data.get("internalized")),
        "n_train_pairs": data.get("n_train_pairs"),
        "heldout_n": data.get("heldout_n"),
        "pair_source": data.get("pair_source"),
        "criterion": data.get("criterion", CRITERION),
        "atom": f"office_{family}_uselog",
    }


def build(root: Path | None = None) -> dict:
    root = root or repo_root()
    rows = [load_family(root, f) for f in FAMILIES]
    all_found = all(r["found"] for r in rows)
    all_bare = all(r.get("bare_clears_gate") for r in rows)
    all_d0 = all(
        r.get("dissolution") is not None and float(r["dissolution"]) <= 0.05 for r in rows if r["found"]
    )
    evidence = {
        "kind": "dissolve_dashboard",
        "product": "蚁算模型",
        "engine": "Envolution",
        "gate": str(CRITERION),
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "families": rows,
        "summary": {
            "n_families": len(rows),
            "all_found": all_found,
            "all_bare_clears_gate": all_bare,
            "all_dissolution_le_005": all_d0,
            "pass": bool(all_found and all_bare and all_d0),
        },
        "gate2_claim_untouched": True,
        "vl": False,
        "notes": "Aggregated from existing runs/capabilities/office_*_uselog/dissolution.json; no retrain.",
    }
    return evidence


def to_markdown(ev: dict) -> str:
    lines = [
        "# Dissolve 仪表盘 · 蚁算四族",
        "",
        f"时间：{ev['timestamp']}（本机时区）",
        f"Gate **{ev['gate']}** · 产品 **{ev['product']}** · 引擎 {ev['engine']}",
        "",
        f"判定：**{'PASS' if ev['summary']['pass'] else 'FAIL'}**（仅聚合证据，不新训）",
        "",
        "| 族 | bare | scaffold | D | bare≥gate | internalized | atom |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for r in ev["families"]:
        if not r["found"]:
            lines.append(f"| {r['family']} | — | — | — | missing | — | — |")
            continue
        lines.append(
            f"| {r['family']} | {r['bare_rate']} | {r['scaffold_rate']} | {r['dissolution']} | "
            f"{'yes' if r['bare_clears_gate'] else 'no'} | {'yes' if r['internalized'] else 'no'} | {r['atom']} |"
        )
    lines += [
        "",
        "## 摘要",
        f"- all_found={ev['summary']['all_found']}",
        f"- all_bare_clears_gate={ev['summary']['all_bare_clears_gate']}",
        f"- all_dissolution_le_005={ev['summary']['all_dissolution_le_005']}",
        "- gate2_claim_untouched=true · vl=false",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    root = repo_root()
    ev = build(root)
    docs = root / "docs"
    stamp = datetime.now().strftime("%Y-%m-%d")
    jp = docs / f"DISSOLVE_DASHBOARD_{stamp}.json"
    mp = docs / f"DISSOLVE_DASHBOARD_{stamp}.md"
    jp.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(to_markdown(ev), encoding="utf-8")
    print(json.dumps({"pass": ev["summary"]["pass"], "json": str(jp), "md": str(mp)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
