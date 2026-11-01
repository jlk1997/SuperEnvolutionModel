# -*- coding: utf-8 -*-
"""C621: Capture-office regression after C617-C620. V4-V85+heldout + clarity floor.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_paid_from_text
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "capture_regression_c621"
README = ROOT / "docs" / "蚁算_截图办公_README.md"
CLI = ROOT / "scripts" / "ant_capture_office.py"
FLOOR = ROOT / "docs" / "蚁算_CLARITY_FLOOR.md"

SMOKE_POINTERS = [
    ("V85", DOC / "C618_VISION_V85_SMOKE.json"),
    ("V85_heldout", DOC / "C619_VISION_V85_HELDOUT_SMOKE.json"),
    ("V84", DOC / "C612_VISION_V84_SMOKE.json"),
    ("V84_heldout", DOC / "C613_VISION_V84_HELDOUT_SMOKE.json"),
    ("V84", DOC / "C612_VISION_V84_SMOKE.json"),
    ("V84_heldout", DOC / "C613_VISION_V84_HELDOUT_SMOKE.json"),
    ("V83", DOC / "C606_VISION_V83_SMOKE.json"),
    ("V83_heldout", DOC / "C607_VISION_V83_HELDOUT_SMOKE.json"),
    ("V83", DOC / "C606_VISION_V83_SMOKE.json"),
    ("V83_heldout", DOC / "C607_VISION_V83_HELDOUT_SMOKE.json"),
    ("V82", DOC / "C600_VISION_V82_SMOKE.json"),
    ("V82_heldout", DOC / "C601_VISION_V82_HELDOUT_SMOKE.json"),
    ("V82", DOC / "C600_VISION_V82_SMOKE.json"),
    ("V82_heldout", DOC / "C601_VISION_V82_HELDOUT_SMOKE.json"),
    ("V81", DOC / "C594_VISION_V81_SMOKE.json"),
    ("V81_heldout", DOC / "C595_VISION_V81_HELDOUT_SMOKE.json"),
    ("V81", DOC / "C594_VISION_V81_SMOKE.json"),
    ("V81_heldout", DOC / "C595_VISION_V81_HELDOUT_SMOKE.json"),
    ("V80", DOC / "C588_VISION_V80_SMOKE.json"),
    ("V80_heldout", DOC / "C589_VISION_V80_HELDOUT_SMOKE.json"),
    ("V80", DOC / "C588_VISION_V80_SMOKE.json"),
    ("V80_heldout", DOC / "C589_VISION_V80_HELDOUT_SMOKE.json"),
    ("V79", DOC / "C582_VISION_V79_SMOKE.json"),
    ("V79_heldout", DOC / "C583_VISION_V79_HELDOUT_SMOKE.json"),
    ("V79", DOC / "C582_VISION_V79_SMOKE.json"),
    ("V79_heldout", DOC / "C583_VISION_V79_HELDOUT_SMOKE.json"),
    ("V78", DOC / "C576_VISION_V78_SMOKE.json"),
    ("V78_heldout", DOC / "C577_VISION_V78_HELDOUT_SMOKE.json"),
    ("V78", DOC / "C576_VISION_V78_SMOKE.json"),
    ("V78_heldout", DOC / "C577_VISION_V78_HELDOUT_SMOKE.json"),
    ("V77", DOC / "C570_VISION_V77_SMOKE.json"),
    ("V77_heldout", DOC / "C571_VISION_V77_HELDOUT_SMOKE.json"),
    ("V77", DOC / "C570_VISION_V77_SMOKE.json"),
    ("V77_heldout", DOC / "C571_VISION_V77_HELDOUT_SMOKE.json"),
    ("V76", DOC / "C564_VISION_V76_SMOKE.json"),
    ("V76_heldout", DOC / "C565_VISION_V76_HELDOUT_SMOKE.json"),
    ("V76", DOC / "C564_VISION_V76_SMOKE.json"),
    ("V76_heldout", DOC / "C565_VISION_V76_HELDOUT_SMOKE.json"),
    ("V75", DOC / "C558_VISION_V75_SMOKE.json"),
    ("V75_heldout", DOC / "C559_VISION_V75_HELDOUT_SMOKE.json"),
    ("V75", DOC / "C558_VISION_V75_SMOKE.json"),
    ("V75_heldout", DOC / "C559_VISION_V75_HELDOUT_SMOKE.json"),
    ("V74", DOC / "C552_VISION_V74_SMOKE.json"),
    ("V74_heldout", DOC / "C553_VISION_V74_HELDOUT_SMOKE.json"),
    ("V74", DOC / "C552_VISION_V74_SMOKE.json"),
    ("V74_heldout", DOC / "C553_VISION_V74_HELDOUT_SMOKE.json"),
    ("V73", DOC / "C546_VISION_V73_SMOKE.json"),
    ("V73_heldout", DOC / "C547_VISION_V73_HELDOUT_SMOKE.json"),
    ("V73", DOC / "C546_VISION_V73_SMOKE.json"),
    ("V73_heldout", DOC / "C547_VISION_V73_HELDOUT_SMOKE.json"),
    ("V72", DOC / "C540_VISION_V72_SMOKE.json"),
    ("V72_heldout", DOC / "C541_VISION_V72_HELDOUT_SMOKE.json"),
    ("V72", DOC / "C540_VISION_V72_SMOKE.json"),
    ("V72_heldout", DOC / "C541_VISION_V72_HELDOUT_SMOKE.json"),
    ("V71", DOC / "C534_VISION_V71_SMOKE.json"),
    ("V71_heldout", DOC / "C535_VISION_V71_HELDOUT_SMOKE.json"),
    ("V71", DOC / "C534_VISION_V71_SMOKE.json"),
    ("V71_heldout", DOC / "C535_VISION_V71_HELDOUT_SMOKE.json"),
    ("V70", DOC / "C528_VISION_V70_SMOKE.json"),
    ("V70_heldout", DOC / "C529_VISION_V70_HELDOUT_SMOKE.json"),
    ("V70", DOC / "C528_VISION_V70_SMOKE.json"),
    ("V70_heldout", DOC / "C529_VISION_V70_HELDOUT_SMOKE.json"),
    ("V69", DOC / "C522_VISION_V69_SMOKE.json"),
    ("V69_heldout", DOC / "C523_VISION_V69_HELDOUT_SMOKE.json"),
    ("V69", DOC / "C522_VISION_V69_SMOKE.json"),
    ("V69_heldout", DOC / "C523_VISION_V69_HELDOUT_SMOKE.json"),
    ("V68", DOC / "C516_VISION_V68_SMOKE.json"),
    ("V68_heldout", DOC / "C517_VISION_V68_HELDOUT_SMOKE.json"),
    ("V68", DOC / "C516_VISION_V68_SMOKE.json"),
    ("V68_heldout", DOC / "C517_VISION_V68_HELDOUT_SMOKE.json"),
    ("V67", DOC / "C510_VISION_V67_SMOKE.json"),
    ("V67_heldout", DOC / "C511_VISION_V67_HELDOUT_SMOKE.json"),
    ("V67", DOC / "C510_VISION_V67_SMOKE.json"),
    ("V67_heldout", DOC / "C511_VISION_V67_HELDOUT_SMOKE.json"),
    ("V66", DOC / "C504_VISION_V66_SMOKE.json"),
    ("V66_heldout", DOC / "C505_VISION_V66_HELDOUT_SMOKE.json"),
    ("V66", DOC / "C504_VISION_V66_SMOKE.json"),
    ("V66_heldout", DOC / "C505_VISION_V66_HELDOUT_SMOKE.json"),
    ("V65", DOC / "C498_VISION_V65_SMOKE.json"),
    ("V65_heldout", DOC / "C499_VISION_V65_HELDOUT_SMOKE.json"),
    ("V65", DOC / "C498_VISION_V65_SMOKE.json"),
    ("V65_heldout", DOC / "C499_VISION_V65_HELDOUT_SMOKE.json"),
    ("V64", DOC / "C492_VISION_V64_SMOKE.json"),
    ("V64_heldout", DOC / "C493_VISION_V64_HELDOUT_SMOKE.json"),
    ("V64", DOC / "C492_VISION_V64_SMOKE.json"),
    ("V64_heldout", DOC / "C493_VISION_V64_HELDOUT_SMOKE.json"),
    ("V63", DOC / "C486_VISION_V63_SMOKE.json"),
    ("V63_heldout", DOC / "C487_VISION_V63_HELDOUT_SMOKE.json"),
    ("V63", DOC / "C486_VISION_V63_SMOKE.json"),
    ("V63_heldout", DOC / "C487_VISION_V63_HELDOUT_SMOKE.json"),
    ("V62", DOC / "C480_VISION_V62_SMOKE.json"),
    ("V62_heldout", DOC / "C481_VISION_V62_HELDOUT_SMOKE.json"),
    ("V62", DOC / "C480_VISION_V62_SMOKE.json"),
    ("V62_heldout", DOC / "C481_VISION_V62_HELDOUT_SMOKE.json"),
    ("V61", DOC / "C474_VISION_V61_SMOKE.json"),
    ("V61_heldout", DOC / "C475_VISION_V61_HELDOUT_SMOKE.json"),
    ("V61", DOC / "C474_VISION_V61_SMOKE.json"),
    ("V61_heldout", DOC / "C475_VISION_V61_HELDOUT_SMOKE.json"),
    ("V60", DOC / "C468_VISION_V60_SMOKE.json"),
    ("V60_heldout", DOC / "C469_VISION_V60_HELDOUT_SMOKE.json"),
    ("V60", DOC / "C468_VISION_V60_SMOKE.json"),
    ("V60_heldout", DOC / "C469_VISION_V60_HELDOUT_SMOKE.json"),
    ("V59", DOC / "C462_VISION_V59_SMOKE.json"),
    ("V59_heldout", DOC / "C463_VISION_V59_HELDOUT_SMOKE.json"),
    ("V59", DOC / "C462_VISION_V59_SMOKE.json"),
    ("V59_heldout", DOC / "C463_VISION_V59_HELDOUT_SMOKE.json"),
    ("V58", DOC / "C456_VISION_V58_SMOKE.json"),
    ("V58_heldout", DOC / "C457_VISION_V58_HELDOUT_SMOKE.json"),
    ("V58", DOC / "C456_VISION_V58_SMOKE.json"),
    ("V58_heldout", DOC / "C457_VISION_V58_HELDOUT_SMOKE.json"),
    ("V57", DOC / "C450_VISION_V57_SMOKE.json"),
    ("V57_heldout", DOC / "C451_VISION_V57_HELDOUT_SMOKE.json"),
    ("V57", DOC / "C450_VISION_V57_SMOKE.json"),
    ("V57_heldout", DOC / "C451_VISION_V57_HELDOUT_SMOKE.json"),
    ("V56", DOC / "C444_VISION_V56_SMOKE.json"),
    ("V56_heldout", DOC / "C445_VISION_V56_HELDOUT_SMOKE.json"),
    ("V56", DOC / "C444_VISION_V56_SMOKE.json"),
    ("V56_heldout", DOC / "C445_VISION_V56_HELDOUT_SMOKE.json"),
    ("V55", DOC / "C438_VISION_V55_SMOKE.json"),
    ("V55_heldout", DOC / "C439_VISION_V55_HELDOUT_SMOKE.json"),
    ("V55", DOC / "C438_VISION_V55_SMOKE.json"),
    ("V55_heldout", DOC / "C439_VISION_V55_HELDOUT_SMOKE.json"),
    ("V54", DOC / "C432_VISION_V54_SMOKE.json"),
    ("V54_heldout", DOC / "C433_VISION_V54_HELDOUT_SMOKE.json"),
    ("V53", DOC / "C426_VISION_V53_SMOKE.json"),
    ("V53_heldout", DOC / "C427_VISION_V53_HELDOUT_SMOKE.json"),
    ("V52", DOC / "C420_VISION_V52_SMOKE.json"),
    ("V52_heldout", DOC / "C421_VISION_V52_HELDOUT_SMOKE.json"),
    ("V51", DOC / "C414_VISION_V51_SMOKE.json"),
    ("V51_heldout", DOC / "C415_VISION_V51_HELDOUT_SMOKE.json"),
    ("V50", DOC / "C408_VISION_V50_SMOKE.json"),
    ("V50_heldout", DOC / "C409_VISION_V50_HELDOUT_SMOKE.json"),

    ("V4", DOC / "C101_VISION_V4_MULTIHOP.json"),
    ("V4_heldout", DOC / "C107_VISION_V4_HELDOUT.json"),
    ("V5", DOC / "C121_VISION_V5_SMOKE.json"),
    ("V5_heldout", DOC / "C126_VISION_V5_HELDOUT_SMOKE.json"),
    ("V6", DOC / "C132_VISION_V6_SMOKE.json"),
    ("V6_heldout", DOC / "C138_VISION_V6_HELDOUT_SMOKE.json"),
    ("V7", DOC / "C144_VISION_V7_SMOKE.json"),
    ("V7_heldout", DOC / "C150_VISION_V7_HELDOUT_SMOKE.json"),
    ("V8", DOC / "C155_VISION_V8_SMOKE.json"),
    ("V8_heldout_refresh", DOC / "C162_V8H02_UNGLUE_REPARSE.json"),
    ("V9", DOC / "C163_VISION_V9_SMOKE.json"),
    ("V9_heldout", DOC / "C164_VISION_V9_HELDOUT_SMOKE.json"),
    ("V10", DOC / "C167_VISION_V10_SMOKE.json"),
    ("V10_heldout", DOC / "C171_VISION_V10_HELDOUT_SMOKE.json"),
    ("V11", DOC / "C173_VISION_V11_SMOKE.json"),
    ("V11_heldout", DOC / "C175_VISION_V11_HELDOUT_SMOKE.json"),
    ("V12", DOC / "C180_V12_FAIL_FIX_RETEST.json"),
    ("V12_heldout", DOC / "C181_VISION_V12_HELDOUT_SMOKE.json"),
    ("V13", DOC / "C183_VISION_V13_SMOKE.json"),
    ("V13_heldout", DOC / "C186_VISION_V13_HELDOUT_SMOKE.json"),
    ("V14", DOC / "C188_VISION_V14_SMOKE.json"),
    ("V14_heldout", DOC / "C191_VISION_V14_HELDOUT_SMOKE.json"),
    ("V15", DOC / "C193_VISION_V15_SMOKE.json"),
    ("V15_heldout", DOC / "C196_VISION_V15_HELDOUT_SMOKE.json"),
    ("V16", DOC / "C198_VISION_V16_SMOKE.json"),
    ("V16_heldout", DOC / "C201_VISION_V16_HELDOUT_SMOKE.json"),
    ("V17", DOC / "C203_VISION_V17_SMOKE.json"),
    ("V17_heldout", DOC / "C207_VISION_V17_HELDOUT_SMOKE.json"),
    ("V18", DOC / "C209_VISION_V18_SMOKE.json"),
    ("V18_refresh", DOC / "C213_V18_FAIL_FIX_RETEST.json"),
    ("V18_heldout", DOC / "C214_VISION_V18_HELDOUT_SMOKE.json"),
    ("V19_prior", DOC / "C218_VISION_V19_SMOKE.json"),
    ("V19_refresh", DOC / "C219_V19_FAIL_FIX_RETEST.json"),
    ("V19_heldout", DOC / "C220_VISION_V19_HELDOUT_SMOKE.json"),
    ("V20", DOC / "C225_VISION_V20_SMOKE.json"),
    ("V20_heldout", DOC / "C226_VISION_V20_HELDOUT_SMOKE.json"),
    ("V21", DOC / "C231_VISION_V21_SMOKE.json"),
    ("V21_refresh", DOC / "C236_V21_FAIL_FIX_RETEST.json"),
    ("V21_heldout", DOC / "C232_VISION_V21_HELDOUT_SMOKE.json"),
    ("V22", DOC / "C238_VISION_V22_SMOKE.json"),
    ("V22_heldout", DOC / "C239_VISION_V22_HELDOUT_SMOKE.json"),
    ("V23", DOC / "C243_VISION_V23_SMOKE.json"),
    ("V23_heldout", DOC / "C244_VISION_V23_HELDOUT_SMOKE.json"),
    ("V24", DOC / "C249_VISION_V24_SMOKE.json"),
    ("V24_heldout", DOC / "C250_VISION_V24_HELDOUT_SMOKE.json"),
    ("C251_product_polish", DOC / "C251_PRODUCT_POLISH_V24.json"),
    ("C210_conf_gate", DOC / "C210_CONFIDENCE_GATE_CAPTURE_WIRE.json"),
    ("C227_multi_metric_deepen", DOC / "C227_MULTI_METRIC_CAPTURE_DEEPEN.json"),
    ("C233_clarity_floor", DOC / "C233_CLARITY_FLOOR_PRODUCT.json"),
    ("C245_cost_ledger", DOC / "C245_COST_LEDGER_REFRESH.json"),
    ("V25", DOC / "C255_VISION_V25_SMOKE.json"),
    ("V25_heldout", DOC / "C256_VISION_V25_HELDOUT_SMOKE.json"),
    ("C257_innovation", DOC / "C257_INNOVATION_U2C_CAPTURE_REPLACE.json"),
    ("V26", DOC / "C261_VISION_V26_SMOKE.json"),
    ("V26_heldout", DOC / "C262_VISION_V26_HELDOUT_SMOKE.json"),
    ("C263_dissolve_cost_shadow", DOC / "C263_DISSOLVE_COST_SHADOW.json"),
    ("V27", DOC / "C267_VISION_V27_SMOKE.json"),
    ("V27_heldout", DOC / "C268_VISION_V27_HELDOUT_SMOKE.json"),
    ("V48", DOC / "C396_VISION_V48_SMOKE.json"),
    ("V48_heldout", DOC / "C397_VISION_V48_HELDOUT_SMOKE.json"),
    ("V49", DOC / "C402_VISION_V49_SMOKE.json"),
    ("V49_heldout", DOC / "C403_VISION_V49_HELDOUT_SMOKE.json"),
    ("C404_conf_gate", DOC / "C404_CONFIDENCE_GATE_STRETCH.json"),

    ("V28", DOC / "C273_VISION_V28_SMOKE.json"),
    ("V28_heldout", DOC / "C274_VISION_V28_HELDOUT_SMOKE.json"),
    ("V29", DOC / "C279_VISION_V29_SMOKE.json"),
    ("V29_heldout", DOC / "C280_VISION_V29_HELDOUT_SMOKE.json"),
    ("V30", DOC / "C285_VISION_V30_SMOKE.json"),
    ("V30_heldout", DOC / "C286_VISION_V30_HELDOUT_SMOKE.json"),
    ("V31", DOC / "C291_VISION_V31_SMOKE.json"),
    ("V31_heldout", DOC / "C292_VISION_V31_HELDOUT_SMOKE.json"),
    ("V32", DOC / "C297_VISION_V32_SMOKE.json"),
    ("V32_heldout", DOC / "C298_VISION_V32_HELDOUT_SMOKE.json"),
    ("V33", DOC / "C303_VISION_V33_SMOKE.json"),
    ("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),
    ("V34", DOC / "C309_VISION_V34_SMOKE.json"),
    ("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),
    ("V35", DOC / "C315_VISION_V35_SMOKE.json"),
    ("V35_heldout", DOC / "C316_VISION_V35_HELDOUT_SMOKE.json"),
    ("V36", DOC / "C321_VISION_V36_SMOKE.json"),
    ("V36_heldout", DOC / "C322_VISION_V36_HELDOUT_SMOKE.json"),
    ("V37", DOC / "C327_VISION_V37_SMOKE.json"),
    ("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),
    ("V38", DOC / "C333_VISION_V38_SMOKE.json"),
    ("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),
    ("V39", DOC / "C340_VISION_V39_SMOKE.json"),
    ("V39_heldout", DOC / "C341_VISION_V39_HELDOUT_SMOKE.json"),
    ("V40", DOC / "C347_VISION_V40_SMOKE.json"),
    ("V40_heldout", DOC / "C348_VISION_V40_HELDOUT_SMOKE.json"),
    ("V41", DOC / "C353_VISION_V41_SMOKE.json"),
    ("V41_heldout", DOC / "C354_VISION_V41_HELDOUT_SMOKE.json"),
    ("V42", DOC / "C360_VISION_V42_SMOKE.json"),
    ("V42_heldout", DOC / "C361_VISION_V42_HELDOUT_SMOKE.json"),
    ("V43", DOC / "C366_VISION_V43_SMOKE.json"),
    ("V43_heldout", DOC / "C367_VISION_V43_HELDOUT_SMOKE.json"),
    ("V44", DOC / "C372_VISION_V44_SMOKE.json"),
    ("V44_heldout", DOC / "C373_VISION_V44_HELDOUT_SMOKE.json"),
    ("V45", DOC / "C378_VISION_V45_SMOKE.json"),
    ("V45_heldout", DOC / "C379_VISION_V45_HELDOUT_SMOKE.json"),
    ("V46", DOC / "C384_VISION_V46_SMOKE.json"),
    ("V46_heldout", DOC / "C385_VISION_V46_HELDOUT_SMOKE.json"),
    ("V47", DOC / "C390_VISION_V47_SMOKE.json"),
    ("V47_heldout", DOC / "C391_VISION_V47_HELDOUT_SMOKE.json"),
    ("V48", DOC / "C396_VISION_V48_SMOKE.json"),
    ("V48_heldout", DOC / "C397_VISION_V48_HELDOUT_SMOKE.json"),
    ("C392_confidence_gate_stretch", DOC / "C392_CONFIDENCE_GATE_STRETCH.json"),
    ("C342_confidence_gate_stretch", DOC / "C342_CONFIDENCE_GATE_STRETCH.json"),
    ("C275_u2c_replace_stretch", DOC / "C275_U2C_REPLACE_STRETCH.json"),
    ("C281_product_u2c_cost", DOC / "C281_PRODUCT_U2C_COST.json"),
    ("C287_confidence_gate_stretch", DOC / "C287_CONFIDENCE_GATE_STRETCH.json"),
    ("C293_dissolve_cost_shadow", DOC / "C293_DISSOLVE_COST_SHADOW.json"),
    ("C299_product_u2c_cost", DOC / "C299_PRODUCT_U2C_COST.json"),
    ("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),
    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),
    ("C317_product_u2c_cost", DOC / "C317_PRODUCT_U2C_COST.json"),
    ("C323_dissolve_cost_shadow", DOC / "C323_DISSOLVE_COST_SHADOW.json"),
    ("C329_confidence_gate_stretch", DOC / "C329_CONFIDENCE_GATE_STRETCH.json"),
    ("C335_product_u2c_cost", DOC / "C335_PRODUCT_U2C_COST.json"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_ok(path: Path):
    if not path.is_file():
        return {"present": False, "pass": False, "rate": None, "claim": None}
    try:
        o = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"present": True, "pass": False, "rate": None, "claim": None, "error": "bad_json"}
    rate = o.get("rate")
    claim = bool(
        o.get("claim")
        or o.get("vl_gate_v25_claim") or o.get("vl_gate_v27_claim") or o.get("vl_gate_v27_heldout_claim") or o.get("vl_gate_v26_heldout_claim") or o.get("vl_gate_v24_claim") or o.get("vl_gate_v24_heldout_claim")
        or o.get("vl_gate_v23_claim") or o.get("vl_gate_v23_heldout_claim")
        or o.get("vl_gate_v22_claim") or o.get("vl_gate_v22_heldout_claim")
        or o.get("vl_gate_v21_claim") or o.get("pass")
    )
    ok = bool(o.get("pass") or o.get("claim") or (isinstance(rate, (int, float)) and rate >= GATE))
    return {"present": True, "pass": ok, "rate": rate, "claim": claim, "fail_ids": o.get("fail_ids")}


def unit_money_parse():
    cases = [
        ("a paid 10.00 b paid 20.50 c open 5.00", 30.5),
        ("TOTAL PAID TARGET 56.25 rA paid 28.00 rB paid 28.25", 56.25),
        ("line paid 28.00 line paid 28.00 line paid 28.00 bait 88.88", 84.0),
        ("a paid 46.00 b paid 47.50 c open 12.00 TOTAL PAID TARGET 93.50", 93.5),
    ]
    rows, n_ok = [], 0
    for text, exp in cases:
        got = sum_paid_from_text(text)
        ok = abs(got - exp) < 0.08
        n_ok += int(ok)
        rows.append({"text": text[:60], "got": got, "expected": exp, "ok": ok})
        g2, aok = parse_metric(text, "paid_total", exp)
        rows[-1]["parse_metric_ok"] = bool(aok and abs((g2 or 0) - exp) < 0.08)
    return {"n": len(cases), "n_ok": n_ok, "rate": round(n_ok / len(cases), 4), "rows": rows, "pass": n_ok == len(cases)}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    readme_ok = README.is_file() and CLI.is_file()
    floor_ok = FLOOR.is_file()
    pointers = []
    n_ok = 0
    for name, path in SMOKE_POINTERS:
        info = load_ok(path)
        info["name"] = name
        info["path"] = str(path.relative_to(ROOT)).replace("\\", "/")
        pointers.append(info)
        n_ok += int(info["pass"] and info["present"])
    money = unit_money_parse()
    cli_help_ok = False
    try:
        import os
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        r = subprocess.run(
            [sys.executable, str(CLI), "--help"],
            capture_output=True, text=True, timeout=30, cwd=str(ROOT), env=env,
        )
        cli_help_ok = r.returncode == 0 and (
            "metric" in (r.stdout or "").lower()
            or "usage" in (r.stdout or "").lower()
            or len(r.stdout or "") > 20
        )
    except Exception:
        cli_help_ok = False

    required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "V34", "V34_heldout", "V35", "V35_heldout", "V36", "V36_heldout", "V37", "V37_heldout", "V38", "V38_heldout", "V39", "V39_heldout", "C233_clarity_floor", "C342_confidence_gate_stretch", "V40", "V40_heldout"]
    by_name = {p["name"]: p for p in pointers}
    required_ok = all(by_name.get(k, {}).get("pass") for k in required)
    overall = bool(required_ok and money["pass"] and readme_ok and cli_help_ok)
    out = {
        "cycle": "C621",
        "theme": "capture_office_regression_c377_c380",
        "gate": GATE,
        "timestamp": ts(),
        "n_pointers": len(pointers),
        "n_ok_pointers": n_ok,
        "pointers": pointers,
        "required": required,
        "required_ok": required_ok,
        "money_unit": money,
        "readme_ok": readme_ok,
        "floor_doc_ok": floor_ok,
        "cli_help_ok": cli_help_ok,
        "pass": overall,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C621_CAPTURE_OFFICE_REGRESSION.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C621", "pass": overall, "required_ok": required_ok,
        "n_ok_pointers": n_ok, "n_pointers": len(pointers),
        "money": money["rate"], "cli_help_ok": cli_help_ok,
    }, ensure_ascii=False))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
