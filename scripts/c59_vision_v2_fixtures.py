# -*- coding: utf-8 -*-
from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
GATE=0.6
OUT = ROOT/"evo/office/fixtures/vision_images_v2"
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def font(size, bold=False, mono=False):
    if mono: p=Path(r"C:\Windows\Fonts\consola.ttf")
    elif bold: p=Path(r"C:\Windows\Fonts\arialbd.ttf")
    else: p=Path(r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(p), size=size)
def save(img, name, meta):
    OUT.mkdir(parents=True, exist_ok=True)
    png=OUT/f"{name}.png"; img.save(png, format="PNG")
    digest=hashlib.sha256(png.read_bytes()).hexdigest()
    task=meta["task"]; key={"caption":"caption","ocr":"ocr_text","table_cells":"cells_csv"}[task]
    meta={**meta,"id":name,"sha256":digest,"synthetic_not_vl":False,"drawn_for_vl":True,"readable_v2":True,"harder_than_v1":True,"source":"c59_vision_v2","timestamp":ts(),"gold":meta.get("gold") or meta.get(key) or ""}
    (OUT/f"{name}.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"id":name,"png_bytes":png.stat().st_size,"task":meta["task"],"gold":meta["gold"]}
made=[]
img=Image.new("RGB",(640,480),(255,255,255)); d=ImageDraw.Draw(img)
d.rectangle([20,20,620,460],outline=(0,0,0),width=2)
d.text((40,30),"TAX INVOICE #TX-4402",fill=(0,0,0),font=font(28,bold=True))
d.text((40,80),"Vendor: Ant Hardware Ltd",fill=(0,0,0),font=font(20))
d.text((40,115),"Buyer: East Warehouse",fill=(0,0,0),font=font(20))
d.text((40,160),"Line1: Bolts M6 x100  @ 0.12 = 12.00",fill=(0,0,0),font=font(18,mono=True))
d.text((40,195),"Line2: Washers x200 @ 0.05 = 10.00",fill=(0,0,0),font=font(18,mono=True))
d.text((40,240),"Subtotal 22.00  Tax 2.20  TOTAL 24.20",fill=(160,0,0),font=font(22,bold=True))
d.text((40,290),"Due: 2026-11-15  PO: PO-8891",fill=(0,0,0),font=font(20))
g="TAX INVOICE TX-4402 Subtotal 22.00 Tax 2.20 TOTAL 24.20 Due 2026-11-15"
made.append(save(img,"v2-hard-ocr-001",{"task":"ocr","ocr_text":g,"caption":"","cells_csv":"","gold":g}))
img=Image.new("RGB",(640,360),(250,250,252)); d=ImageDraw.Draw(img)
d.text((20,10),"WAREHOUSE PICK LIST",fill=(0,0,0),font=font(22,bold=True))
headers=["sku","name","qty","unit","amt"]; rows=[["C9","Clamp","4","2.50","10.00"],["D1","Drill","1","45.00","45.00"],["E3","Epoxy","2","8.25","16.50"]]; x0=[20,100,220,340,440]
for i,h in enumerate(headers): d.text((x0[i],40),h,fill=(0,0,120),font=font(18,bold=True,mono=True))
y=80
for row in rows:
    for i,cell in enumerate(row): d.text((x0[i],y),cell,fill=(0,0,0),font=font(18,mono=True))
    y+=40
cg="sku,name,qty,unit,amt\nC9,Clamp,4,2.50,10.00\nD1,Drill,1,45.00,45.00\nE3,Epoxy,2,8.25,16.50"
made.append(save(img,"v2-hard-table-001",{"task":"table_cells","cells_csv":cg,"ocr_text":"","caption":"","gold":cg}))
img=Image.new("RGB",(640,400),(40,44,52)); d=ImageDraw.Draw(img)
d.rectangle([80,60,560,340],fill=(245,245,248),outline=(20,20,20),width=3)
d.text((120,90),"Confirm purge?",fill=(20,20,20),font=font(28,bold=True))
d.text((120,150),"Delete 12 archived logs forever.",fill=(60,60,60),font=font(20))
d.rectangle([140,240,280,300],fill=(200,200,200),outline=(0,0,0),width=2); d.text((170,255),"Cancel",fill=(0,0,0),font=font(22,bold=True))
d.rectangle([340,240,500,300],fill=(200,40,40),outline=(80,0,0),width=2); d.text((370,255),"Delete",fill=(255,255,255),font=font(22,bold=True))
g="Confirm purge? Delete 12 archived logs [Cancel] [Delete]"
made.append(save(img,"v2-hard-ui-001",{"task":"caption","caption":g,"ocr_text":"Cancel Delete","cells_csv":"","gold":g}))
img=Image.new("RGB",(640,320),(255,255,255)); d=ImageDraw.Draw(img)
d.rectangle([15,15,625,305],outline=(0,0,0),width=3)
d.text((40,40),"SHIP TO",fill=(0,0,0),font=font(24,bold=True))
d.text((40,90),"12 River Rd, Bay 4",fill=(0,0,0),font=font(22))
d.text((40,140),"SKU MIX: C9 x4, D1 x1",fill=(0,0,0),font=font(20,mono=True))
d.text((40,190),"DEADLINE 2026-12-01",fill=(180,0,0),font=font(24,bold=True))
d.text((40,250),"PRIORITY: HIGH",fill=(0,0,0),font=font(20,bold=True))
g="SHIP TO 12 River Rd Bay 4 DEADLINE 2026-12-01 PRIORITY HIGH"
made.append(save(img,"v2-hard-mixed-001",{"task":"ocr","ocr_text":g,"caption":"","cells_csv":"","gold":g,"heldout":True}))
img=Image.new("RGB",(640,360),(235,240,245)); d=ImageDraw.Draw(img)
d.rectangle([50,200,590,300],fill=(120,80,40),outline=(60,30,10),width=3)
d.rectangle([200,80,420,200],fill=(50,50,60),outline=(20,20,30),width=2)
d.rectangle([220,50,400,160],fill=(160,210,255),outline=(30,30,40),width=2)
d.ellipse([480,220,560,280],fill=(200,30,30),outline=(80,0,0),width=2)
d.text((40,20),"cluttered desk laptop red mug",fill=(10,10,10),font=font(22,bold=True))
g="cluttered desk laptop red mug"
made.append(save(img,"v2-caption-001",{"task":"caption","caption":g,"ocr_text":"","cells_csv":"","gold":g}))
img=Image.new("RGB",(480,560),(255,255,255)); d=ImageDraw.Draw(img)
d.text((40,30),"RECEIPT",fill=(0,0,0),font=font(32,bold=True))
d.text((40,90),"Store: Ant Mart #7",fill=(0,0,0),font=font(20))
d.text((40,140),"Coffee  3.50",fill=(0,0,0),font=font(20,mono=True))
d.text((40,180),"Bagel   2.00",fill=(0,0,0),font=font(20,mono=True))
d.text((40,240),"TOTAL  5.50",fill=(0,0,0),font=font(24,bold=True))
d.text((40,300),"Paid CARD ****4412",fill=(0,0,0),font=font(18))
g="RECEIPT TOTAL 5.50 Paid CARD"
made.append(save(img,"v2-ocr-002",{"task":"ocr","ocr_text":g,"caption":"","cells_csv":"","gold":g}))
img=Image.new("RGB",(560,300),(255,255,255)); d=ImageDraw.Draw(img)
d.text((20,15),"SHIFT LOG",fill=(0,0,0),font=font(22,bold=True))
for i,(a,b,c) in enumerate([("dept","hrs","ot"),("ENG","8","1"),("OPS","8","0"),("QA","7","2")]):
    d.text((30,60+i*45),f"{a}  {b}  {c}",fill=(0,0,0),font=font(22,mono=True))
cg="dept,hrs,ot\nENG,8,1\nOPS,8,0\nQA,7,2"
made.append(save(img,"v2-table-002",{"task":"table_cells","cells_csv":cg,"ocr_text":"","caption":"","gold":cg}))
img=Image.new("RGB",(560,360),(30,30,36)); d=ImageDraw.Draw(img)
d.text((40,30),"Preferences",fill=(240,240,240),font=font(26,bold=True))
d.text((40,100),"Auto-save",fill=(220,220,220),font=font(22))
d.rectangle([400,100,480,140],fill=(40,180,80),outline=(20,100,40),width=2)
d.text((40,180),"Telemetry",fill=(220,220,220),font=font(22))
d.rectangle([400,180,480,220],fill=(80,80,90),outline=(40,40,50),width=2)
d.text((40,280),"auto-save ON telemetry OFF",fill=(180,180,180),font=font(16))
g="Preferences auto-save ON telemetry OFF"
made.append(save(img,"v2-ui-002",{"task":"caption","caption":g,"ocr_text":"Preferences Auto-save Telemetry","cells_csv":"","gold":g}))
(ROOT/"docs").mkdir(exist_ok=True)
(ROOT/"docs/蚁算视_VL_GATE_V2_PROTOCOL.md").write_text(f"# 蚁算-视 VL Gate V2 Protocol\n\nUpdated: {ts()} (Asia/Shanghai)\n\nGate **{GATE}**. Harder readable drawn office. Softmatch stem/alias.\nClaim only if rate>=0.6 and n>=8. Not open-domain. V1 untouched. Gate2/3 untouched.\n",encoding="utf-8")
payload={"kind":"r50plus_c59_vision_v2_fixtures","timestamp":ts(),"n":len(made),"fixtures":made,"dir":"evo/office/fixtures/vision_images_v2","protocol":"docs/蚁算视_VL_GATE_V2_PROTOCOL.md","innovation":"Vision V2 harder readable set","vl_gate_v2_claim":False,"gate2_3_untouched":True,"v1_untouched":True}
(ROOT/"docs/r50/C59_vision_v2_harder_fixtures.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"docs/r50/C59b_vision_gate_v2_protocol.json").write_text(json.dumps({"kind":"vision_gate_v2_protocol","timestamp":ts(),"gate":GATE,"min_n":8,"vl_gate_v2_claim":False,"gate2_3_untouched":True,"v1_claim_untouched":True},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"n":len(made),"ids":[m["id"] for m in made]},ensure_ascii=False))
