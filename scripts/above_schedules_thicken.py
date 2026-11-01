# -*- coding: utf-8 -*-
"""Honest above_schedules thickening from archival full-arm office reports.

Does NOT reopen burned packs, does NOT unset Gate2/3 claims, does NOT train.
Re-judges existing summaries and records pass/fail honestly.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from evo.office.judge import judge_office


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


SLATES = {
    "gate2_claim_slate": [
        "runs/office_gate2_full_slate_s0/20261017-201213/summary.json",
        "runs/office_gate2_full_slate_s1/20261017-210105/summary.json",
    ],
    "mid_n_80_ceiling": [
        "runs/office_mid_n_80_s0/20261017-011948/summary.json",
    ],
    "mid_n_160_ceiling": [
        "runs/office_mid_n_160_s0/20261017-013705/summary.json",
    ],
    "census_archival": [
        "runs/office_census_s0/20261009-011405/summary.json",
        "runs/office_census_s1/20261009-012404/summary.json",
        "runs/office_census_s2/20261009-013748/summary.json",
    ],
}


def _arm_rates(summary: dict) -> dict:
    arms = {a["arm"]: a for a in summary.get("arms") or []}
    out = {}
    for name, arm in arms.items():
        items = arm.get("exam_items") or []
        rate = (sum(1 for i in items if i.get("ok")) / len(items)) if items else None
        out[name] = {"rate": rate, "n": len(items)}
    return out


def evaluate_slate(root: Path, name: str, rels: list[str]) -> dict:
    reports = []
    missing = []
    per_file = []
    for rel in rels:
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        reports.append(data)
        per_file.append({"path": rel, "seed": data.get("seed"), "rates": _arm_rates(data)})
    if not reports:
        return {
            "slate": name,
            "ok": False,
            "error": "no_reports",
            "missing": missing,
        }
    judged = judge_office(reports)
    return {
        "slate": name,
        "ok": True,
        "missing": missing,
        "n_reports": len(reports),
        "paths": rels,
        "per_file": per_file,
        "judge": {
            "pass": judged.get("pass"),
            "checks": judged.get("checks"),
            "dual_rate": judged.get("dual_rate"),
            "agent_rate": judged.get("agent_rate"),
            "ceiling_tie": judged.get("ceiling_tie"),
            "informative": judged.get("informative"),
            "ci": judged.get("ci"),
            "seeds": judged.get("seeds"),
        },
    }


def build(root: Path | None = None) -> dict:
    root = root or repo_root()
    rows = [evaluate_slate(root, k, v) for k, v in SLATES.items()]
    claim = next((r for r in rows if r["slate"] == "gate2_claim_slate"), None)
    claim_above = bool(
        claim
        and claim.get("ok")
        and (claim.get("judge") or {}).get("checks", {}).get("above_schedules")
    )
    # Thickening verdict: archival re-judge of claim slate must keep above_schedules.
    # Ceiling packs may show above_schedules=true but are uninformative for beat_agent.
    ceiling_notes = []
    for r in rows:
        j = r.get("judge") or {}
        if j.get("ceiling_tie"):
            ceiling_notes.append(r["slate"])
    evidence = {
        "kind": "above_schedules_thicken",
        "product": "蚁算模型",
        "gate": "0.6",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": "archival_rejudge_full_arm_summaries",
        "gpu": False,
        "vl": False,
        "burned_pack_reopen": False,
        "gate2_claim_untouched": True,
        "gate3_claim_untouched": True,
        "slates": rows,
        "summary": {
            "claim_slate_above_schedules": claim_above,
            "claim_slate_pass": bool(claim and claim.get("ok") and (claim.get("judge") or {}).get("pass")),
            "ceiling_slates_uninformative_for_beat_agent": ceiling_notes,
            "thickening_pass": claim_above,
            "verdict": (
                "PASS: Gate2 claim slate re-judge keeps above_schedules=true; "
                "ceiling mid-n packs are vacuous for beat_agent (dual=agent=1.0); "
                "census archival underpowered / not claim-grade. No new Gate2 claim."
                if claim_above
                else "FAIL: claim slate lost above_schedules on re-judge — investigate before any new claim."
            ),
        },
        "notes": (
            "Honest thicken = re-aggregate existing seven-arm reports. "
            "mid-n dual+agent-only observational cannot score above_schedules (missing shift/continual). "
            "No GPU retrain in this knife."
        ),
    }
    return evidence


def to_markdown(ev: dict) -> str:
    lines = [
        "# above_schedules 加厚（档案重判）",
        "",
        f"时间：{ev['timestamp']}",
        f"方法：{ev['method']} · GPU={ev['gpu']} · VL={ev['vl']}",
        "",
        f"**thickening_pass={ev['summary']['thickening_pass']}**",
        "",
        ev["summary"]["verdict"],
        "",
        "| slate | above_schedules | beat_agent | pass | dual | agent | ceiling |",
        "| --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for r in ev["slates"]:
        if not r.get("ok"):
            lines.append(f"| {r['slate']} | — | — | error | — | — | — |")
            continue
        c = (r["judge"].get("checks") or {})
        lines.append(
            f"| {r['slate']} | {c.get('above_schedules')} | {c.get('beat_agent')} | "
            f"{r['judge'].get('pass')} | {r['judge'].get('dual_rate')} | {r['judge'].get('agent_rate')} | "
            f"{r['judge'].get('ceiling_tie')} |"
        )
    lines += [
        "",
        "- gate2_claim_untouched=true",
        "- burned_pack_reopen=false",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    root = repo_root()
    ev = build(root)
    docs = root / "docs"
    stamp = datetime.now().strftime("%Y-%m-%d")
    jp = docs / f"ABOVE_SCHEDULES_THICKEN_{stamp}.json"
    mp = docs / f"ABOVE_SCHEDULES_THICKEN_{stamp}.md"
    jp.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(to_markdown(ev), encoding="utf-8")
    print(json.dumps({"pass": ev["summary"]["thickening_pass"], "json": str(jp)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
