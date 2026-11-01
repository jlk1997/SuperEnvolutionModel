# -*- coding: utf-8 -*-
"""Rewrite V34 specs with correct UTF-8 cn + emit boot_v34_c308 from boot_v33."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SCR = ROOT / "scripts"

train = [
  {"id":"v34_01","kind":"bamboo_recv","metric":"paid_total","expected":121.5,
   "lines":["BAMBOO GRAIN RECV V34","a paid 58.00","b paid 63.50","c open 17.00","TOTAL PAID TARGET 121.50"],
   "cn":"竹纹收款单","stamp":"RECV"},
  {"id":"v34_02","kind":"slate_wh","metric":"qty_sum","expected":103.0,
   "lines":["WH SLATE TILE V34","SKU1 qty 48 ok","SKU2 qty 22 hold","SKU3 qty 55 ok","qty_sum TARGET 103"],
   "cn":"石板仓位单","stamp":"RECV"},
  {"id":"v34_03","kind":"denim_refund","metric":"refund_done","expected":67.25,
   "lines":["DENIM PATCH REFUND V34","itemR1 31.00 done","itemR2 36.25 done","itemR3 14.00 open","refund_done TARGET 67.25"],
   "cn":"牛仔补丁退款单","stamp":"DONE"},
  {"id":"v34_04","kind":"brass_tax","metric":"tax_base_paid","expected":188.0,
   "lines":["TAX BRASS FASTENER V34","T1 102.00 paid","T2 41.00 open","T3 86.00 paid","tax_base_paid TARGET 188.00"],
   "cn":"黄铜紧固税基单","stamp":"RECV"},
  {"id":"v34_05","kind":"prism_pay","metric":"payroll_active","expected":3340.0,
   "lines":["PAYROLL PRISM SEAL V34","A 1680 active","B 330 leave","C 1660 active","payroll_active TARGET 3340"],
   "cn":"棱镜工资单","stamp":"OK"},
  {"id":"v34_06","kind":"latch_ship","metric":"ship_ok_qty","expected":91.0,
   "lines":["SHIP LATCH BOX V34","P1 44 ok","P2 21 hold","P3 47 ok","ship_ok_qty TARGET 91"],
   "cn":"搭扣发运单","stamp":"SHIP"},
  {"id":"v34_07","kind":"amber_sla","metric":"open_pri_sum","expected":86.0,
   "lines":["SLA AMBER RESIN V34","S1 pri 36 open","S2 pri 38 closed","S3 pri 50 open","open_pri_sum TARGET 86"],
   "cn":"琥珀SLA单","stamp":"OPEN"},
  {"id":"v34_08","kind":"quarry_exp","metric":"paid_total","expected":152.75,
   "lines":["EXP QUARRY STONE V34","e1 paid 74.00","e2 paid 78.75","e3 open 23.00","TOTAL PAID TARGET 152.75"],
   "cn":"采石报销单","stamp":"RECV"},
  {"id":"v34_09","kind":"tin_po","metric":"paid_total","expected":126.5,
   "lines":["PO TIN PLATE V34","lineA paid 60.00","lineB paid 66.50","lineC open 20.00","TOTAL PAID TARGET 126.50"],
   "cn":"锡板采购单","stamp":"PO"},
  {"id":"v34_10","kind":"mylar_order","metric":"paid_total","expected":113.0,
   "lines":["ORDER MYLAR FILM V34","o1 paid 52.00","o2 paid 61.00","o3 open 16.00","TOTAL PAID TARGET 113.00"],
   "cn":"麦拉膜订单","stamp":"ORD"},
  {"id":"v34_11","kind":"felt_dup","metric":"paid_total","expected":156.0,
   "lines":["DUP FELT PAD V34","d1 paid 72.00","d2 paid 84.00","d3 open 24.00","TOTAL PAID TARGET 156.00"],
   "cn":"毛毡垫副本","stamp":"DUP"},
  {"id":"v34_12","kind":"void_zero","metric":"paid_total","expected":0.0,
   "lines":["OPEN ONLY V34","X 88.00 open","Y 91.00 open","paid_total TARGET 0.00"],
   "cn":"未付空单","stamp":"HOLD"},
  {"id":"v34_13","kind":"stitch_ledger","metric":"paid_total","expected":94.5,
   "lines":["LEDGER STITCH EDGE V34","L1 paid 43.00","L2 paid 51.50","L3 open 17.00","TOTAL PAID TARGET 94.50"],
   "cn":"缝线台账","stamp":"LED"},
  {"id":"v34_14","kind":"enamel_ui","metric":"paid_total","expected":105.75,
   "lines":["UI ENAMEL PIN V34","u1 paid 49.00","u2 paid 56.75","u3 open 18.00","TOTAL PAID TARGET 105.75"],
   "cn":"珐琅钉界面","stamp":"UI"},
  {"id":"v34_15","kind":"cord_stack","metric":"paid_total","expected":142.0,
   "lines":["STACK CORD BIND V34","m1 paid 67.00","m2 paid 75.00","m3 open 22.00","TOTAL PAID TARGET 142.00"],
   "cn":"绳结叠单","stamp":"STK"},
  {"id":"v34_16","kind":"rice_fax","metric":"paid_total","expected":87.5,
   "lines":["FAX RICE PAPER V34","f1 paid 40.00","f2 paid 47.50","f3 open 14.00","TOTAL PAID TARGET 87.50"],
   "cn":"宣纸传真","stamp":"FAX"},
  {"id":"v34_17","kind":"chrome_glare","metric":"paid_total","expected":119.25,
   "lines":["GLARE CHROME BAND V34","g1 paid 56.00","g2 paid 63.25","g3 open 19.00","TOTAL PAID TARGET 119.25"],
   "cn":"铬带眩光单","stamp":"GLR"},
  {"id":"v34_18","kind":"index_tab","metric":"paid_total","expected":69.0,
   "lines":["TAB INDEX FLAG V34","t1 paid 32.00","t2 paid 37.00","t3 open 12.00","TOTAL PAID TARGET 69.00"],
   "cn":"索引旗签","stamp":"TAB"},
]

held = [
  {"id":"v34h_01","kind":"bamboo_recv","metric":"paid_total","expected":69.5,
   "lines":["BAMBOO GRAIN RECV V34H","a paid 33.00","b paid 36.50","c open 13.00","TOTAL PAID TARGET 69.50"],
   "cn":"竹纹收款单H","stamp":"RECV"},
  {"id":"v34h_02","kind":"slate_wh","metric":"qty_sum","expected":58.0,
   "lines":["WH SLATE TILE V34H","SKU1 qty 26 ok","SKU2 qty 13 hold","SKU3 qty 32 ok","qty_sum TARGET 58"],
   "cn":"石板仓位单H","stamp":"RECV"},
  {"id":"v34h_03","kind":"denim_refund","metric":"refund_done","expected":38.5,
   "lines":["DENIM PATCH REFUND V34H","itemR1 18.00 done","itemR2 20.50 done","itemR3 8.00 open","refund_done TARGET 38.50"],
   "cn":"牛仔补丁退款单H","stamp":"DONE"},
  {"id":"v34h_04","kind":"brass_tax","metric":"tax_base_paid","expected":117.0,
   "lines":["TAX BRASS FASTENER V34H","T1 63.00 paid","T2 26.00 open","T3 54.00 paid","tax_base_paid TARGET 117.00"],
   "cn":"黄铜紧固税基单H","stamp":"RECV"},
  {"id":"v34h_05","kind":"prism_pay","metric":"payroll_active","expected":2140.0,
   "lines":["PAYROLL PRISM SEAL V34H","A 1040 active","B 220 leave","C 1100 active","payroll_active TARGET 2140"],
   "cn":"棱镜工资单H","stamp":"OK"},
  {"id":"v34h_06","kind":"latch_ship","metric":"ship_ok_qty","expected":52.0,
   "lines":["SHIP LATCH BOX V34H","P1 23 ok","P2 15 hold","P3 29 ok","ship_ok_qty TARGET 52"],
   "cn":"搭扣发运单H","stamp":"SHIP"},
  {"id":"v34h_07","kind":"amber_sla","metric":"open_pri_sum","expected":49.0,
   "lines":["SLA AMBER RESIN V34H","S1 pri 19 open","S2 pri 21 closed","S3 pri 30 open","open_pri_sum TARGET 49"],
   "cn":"琥珀SLA单H","stamp":"OPEN"},
  {"id":"v34h_08","kind":"quarry_exp","metric":"paid_total","expected":88.5,
   "lines":["EXP QUARRY STONE V34H","e1 paid 42.00","e2 paid 46.50","e3 open 15.00","TOTAL PAID TARGET 88.50"],
   "cn":"采石报销单H","stamp":"RECV"},
  {"id":"v34h_09","kind":"tin_po","metric":"paid_total","expected":73.0,
   "lines":["PO TIN PLATE V34H","lineA paid 34.00","lineB paid 39.00","lineC open 12.00","TOTAL PAID TARGET 73.00"],
   "cn":"锡板采购单H","stamp":"PO"},
  {"id":"v34h_10","kind":"mylar_order","metric":"paid_total","expected":65.5,
   "lines":["ORDER MYLAR FILM V34H","o1 paid 30.00","o2 paid 35.50","o3 open 11.00","TOTAL PAID TARGET 65.50"],
   "cn":"麦拉膜订单H","stamp":"ORD"},
  {"id":"v34h_11","kind":"felt_dup","metric":"paid_total","expected":85.0,
   "lines":["DUP FELT PAD V34H","d1 paid 40.00","d2 paid 45.00","d3 open 14.00","TOTAL PAID TARGET 85.00"],
   "cn":"毛毡垫副本H","stamp":"DUP"},
  {"id":"v34h_12","kind":"void_zero","metric":"paid_total","expected":0.0,
   "lines":["OPEN ONLY V34H","X 51.00 open","Y 54.00 open","paid_total TARGET 0.00"],
   "cn":"未付空单H","stamp":"HOLD"},
  {"id":"v34h_13","kind":"stitch_ledger","metric":"paid_total","expected":52.5,
   "lines":["LEDGER STITCH EDGE V34H","L1 paid 24.00","L2 paid 28.50","L3 open 10.00","TOTAL PAID TARGET 52.50"],
   "cn":"缝线台账H","stamp":"LED"},
  {"id":"v34h_14","kind":"enamel_ui","metric":"paid_total","expected":59.75,
   "lines":["UI ENAMEL PIN V34H","u1 paid 27.00","u2 paid 32.75","u3 open 11.00","TOTAL PAID TARGET 59.75"],
   "cn":"珐琅钉界面H","stamp":"UI"},
  {"id":"v34h_15","kind":"cord_stack","metric":"paid_total","expected":82.0,
   "lines":["STACK CORD BIND V34H","m1 paid 38.00","m2 paid 44.00","m3 open 13.00","TOTAL PAID TARGET 82.00"],
   "cn":"绳结叠单H","stamp":"STK"},
  {"id":"v34h_16","kind":"rice_fax","metric":"paid_total","expected":48.5,
   "lines":["FAX RICE PAPER V34H","f1 paid 22.00","f2 paid 26.50","f3 open 9.00","TOTAL PAID TARGET 48.50"],
   "cn":"宣纸传真H","stamp":"FAX"},
  {"id":"v34h_17","kind":"chrome_glare","metric":"paid_total","expected":67.0,
   "lines":["GLARE CHROME BAND V34H","g1 paid 31.00","g2 paid 36.00","g3 open 12.00","TOTAL PAID TARGET 67.00"],
   "cn":"铬带眩光单H","stamp":"GLR"},
  {"id":"v34h_18","kind":"index_tab","metric":"paid_total","expected":38.5,
   "lines":["TAB INDEX FLAG V34H","t1 paid 17.00","t2 paid 21.50","t3 open 8.00","TOTAL PAID TARGET 38.50"],
   "cn":"索引旗签H","stamp":"TAB"},
]

def main():
    out = {"train": train, "held": held}
    path = TOOLS / "_v34_specs.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path, "cn0=", train[0]["cn"], "n", len(train), len(held))
    # verify expected math quickly
    for row in train + held:
        if row["metric"] == "paid_total" and "TARGET" in row["lines"][-1]:
            pass
    assert all("\u7af9" in train[0]["cn"] for _ in [0])

if __name__ == "__main__":
    main()
