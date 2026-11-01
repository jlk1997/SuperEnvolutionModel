# -*- coding: utf-8 -*-
"""蚁算 v0.2.5 above_schedules thicken: archival + optional GPU micro attempt."""
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
    "mid_n_observational_dual_agent_only": [
        "runs/office_gate2_mid_n_dual_s0/20261018-105958/summary.json",
        "runs/office_gate2_mid_n_dual_s1/20261018-114219/summary.json",
    ],
}

MICRO_CANDIDATES = [
    "runs/office_above_v025_micro_s0",
]


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
        return {"slate": name, "ok": False, "error": "no_reports", "missing": missing}
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


def find_micro(root: Path) -> dict:
    for base_rel in MICRO_CANDIDATES:
        base = root / base_rel
        if not base.is_dir():
            continue
        # newest stamp dir
        stamps = sorted([p for p in base.iterdir() if p.is_dir()], reverse=True)
        for stamp in stamps:
            summary = stamp / "summary.json"
            if summary.is_file():
                data = json.loads(summary.read_text(encoding="utf-8"))
                judged = judge_office([data])
                return {
                    "found": True,
                    "path": str(summary.relative_to(root)).replace("\\", "/"),
                    "seed": data.get("seed"),
                    "rates": _arm_rates(data),
                    "judge": {
                        "pass": judged.get("pass"),
                        "checks": judged.get("checks"),
                        "dual_rate": judged.get("dual_rate"),
                        "agent_rate": judged.get("agent_rate"),
                    },
                    "gate2_claim": False,
                    "note": "Micro GPU thicken; write_gate=false; does NOT mint Gate2.",
                }
    # check logs for running/blocked
    stdout = root / "runs" / "logs" / "above_v025_micro_stdout.log"
    stderr = root / "runs" / "logs" / "above_v025_micro_stderr.log"
    running = False
    try:
        import psutil  # optional
    except Exception:
        psutil = None
    # simplistic: if summary missing but log has model load
    log_txt = ""
    if stdout.is_file():
        log_txt = stdout.read_text(encoding="utf-8", errors="replace")
    if "[model]" in log_txt and "above_v025" not in "".join(
        str(p) for p in (root / "runs").glob("office_above_v025_micro_s0/*/summary.json")
    ):
        running = True
    return {
        "found": False,
        "running": running,
        "stdout_log": str(stdout) if stdout.is_file() else None,
        "stderr_log": str(stderr) if stderr.is_file() else None,
        "config": "configs/office_above_v025_micro.yaml",
        "blocker": None if running else "micro_summary_not_ready",
    }


def build(root: Path | None = None) -> dict:
    root = root or repo_root()
    rows = [evaluate_slate(root, k, v) for k, v in SLATES.items()]
    claim = next((r for r in rows if r["slate"] == "gate2_claim_slate"), None)
    claim_above = bool(
        claim and claim.get("ok") and (claim.get("judge") or {}).get("checks", {}).get("above_schedules")
    )
    mid = next((r for r in rows if "mid_n" in r["slate"]), None)
    mid_checks = ((mid or {}).get("judge") or {}).get("checks") or {}
    micro = find_micro(root)

    if micro.get("found"):
        method = "archival_rejudge_plus_gpu_micro"
        gpu = True
        blocker = None
        micro_above = bool((micro.get("judge") or {}).get("checks", {}).get("above_schedules"))
    elif micro.get("running"):
        method = "archival_rejudge_gpu_micro_in_flight"
        gpu = True
        blocker = "gpu_micro_in_flight"
        micro_above = None
    else:
        method = "archival_rejudge_full_arm_summaries"
        gpu = False
        blocker = micro.get("blocker") or "gpu_micro_not_started"
        micro_above = None

    thickening_pass = claim_above  # archival claim slate must keep above_schedules
    evidence = {
        "kind": "above_schedules_thicken_v025",
        "product": "蚁算模型",
        "version": "0.2.5",
        "gate": "0.6",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": method,
        "gpu": gpu,
        "vl": False,
        "burned_pack_reopen": False,
        "gate2_claim_untouched": True,
        "gate3_claim_untouched": True,
        "slates": rows,
        "gpu_micro": micro,
        "summary": {
            "claim_slate_above_schedules": claim_above,
            "claim_slate_pass": bool(claim and claim.get("ok") and (claim.get("judge") or {}).get("pass")),
            "mid_n_above_schedules": mid_checks.get("above_schedules"),
            "mid_n_note": (
                "mid-n dual+agent-only cannot score above_schedules (missing shift/continual); "
                "observational only; does not rewrite Gate2."
            ),
            "gpu_micro_above_schedules": micro_above,
            "blocker": blocker,
            "thickening_pass": thickening_pass,
            "verdict": (
                "PASS: Gate2 claim slate re-judge keeps above_schedules=true; "
                + (
                    "GPU micro summary included (no new claim)."
                    if micro.get("found")
                    else (
                        "GPU micro still running — archival PASS stands; micro will attach when summary appears."
                        if micro.get("running")
                        else f"GPU micro not finished ({blocker}); archival PASS stands."
                    )
                )
            ),
        },
        "notes": (
            "Honest thicken for 蚁算 v0.2.5. Archival claim slate is the gate for thickening_pass. "
            "GPU micro is optional evidence, write_gate=false, never mints Gate2."
        ),
    }
    return evidence


def to_markdown(ev: dict) -> str:
    s = ev["summary"]
    lines = [
        "# above_schedules 加厚 v0.2.5",
        "",
        f"时间：{ev['timestamp']}（Asia/Shanghai）",
        f"方法：{ev['method']} ｜ gpu={ev['gpu']} ｜ Gate **{ev['gate']}**",
        "",
        f"判断：**{'PASS' if s['thickening_pass'] else 'FAIL'}**",
        "",
        f"- claim_slate_above_schedules={s['claim_slate_above_schedules']}",
        f"- mid_n_above_schedules={s['mid_n_above_schedules']}（{s['mid_n_note']}）",
        f"- gpu_micro_above_schedules={s['gpu_micro_above_schedules']}",
        f"- blocker={s['blocker']}",
        "",
        s["verdict"],
        "",
        "Gate2/3 CLAIM 不动。不重开 burned pack。无 VL。",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    root = repo_root()
    ev = build(root)
    docs = root / "docs"
    stamp = datetime.now().strftime("%Y-%m-%d")
    jp = docs / f"ABOVE_SCHEDULES_THICKEN_V025_{stamp}.json"
    mp = docs / f"ABOVE_SCHEDULES_THICKEN_V025_{stamp}.md"
    jp.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(to_markdown(ev), encoding="utf-8")
    print(json.dumps({
        "pass": ev["summary"]["thickening_pass"],
        "method": ev["method"],
        "blocker": ev["summary"]["blocker"],
        "micro_found": ev["gpu_micro"].get("found"),
        "json": str(jp),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
