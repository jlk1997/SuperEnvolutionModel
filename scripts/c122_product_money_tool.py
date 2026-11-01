# -*- coding: utf-8 -*-
"""C122: Product harden — tool-backed money math preferred over U2C LoRA absorb."""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_paid_from_text, sum_csv_text, prefer_tool_over_lora

DOC = ROOT / "docs" / "r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    tests = []
    # mirror C115 paid parse cases with tool
    cases = [
        ("item A paid 11.00 item C paid 19.00", 30.0),
        ("paid 1.5 paid 2.5 paid 3", 7.0),
        ("OPEN ONLY X 9.00 open Y 11.00 open", 0.0),
        ("amount,status\n12.5,paid\n8,open\n5.5,paid\n", 18.0),
    ]
    n_ok = 0
    for text, exp in cases:
        if "amount,status" in text:
            got = sum_csv_text(text)
        else:
            got = sum_paid_from_text(text)
        ok = abs(got - exp) < 0.08
        n_ok += int(ok)
        tests.append({"text": text[:60], "exp": exp, "got": got, "ok": ok})

    # wire note into capture lib preference file
    policy = prefer_tool_over_lora()
    pol_path = ROOT / "evo" / "office" / "product_money_policy.json"
    J(pol_path, {**policy, "timestamp": ts(), "gate": GATE})

    rate = n_ok / len(tests) if tests else 0.0
    out = {
        "cycle": "C122",
        "theme": "product_harden_tool_backed_money",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "module": "evo/office/money_tool.py",
        "policy_path": str(pol_path.relative_to(ROOT)).replace("\\", "/"),
        "tests": {"n": len(tests), "n_ok": n_ok, "rate": round(rate, 4), "rows": tests},
        "u2c_absorb_claim": False,
        "c120_ref": "docs/r50/C120_U2C_ABSORB_DIAGNOSIS.json",
        "pass": rate >= GATE,
        "claim": False,
        "note": "Cheap product harden: money sums via tool, not LoRA. No Gate2/3.",
    }
    J(DOC / "C122_PRODUCT_MONEY_TOOL.json", out)
    print(json.dumps({"cycle": "C122", "rate": round(rate, 4), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
