# 蚁算 R50+ LOOP

Updated: 2026-10-19T00:16:43+08:00 (Asia/Shanghai)

Mandate: continuous evolution after R50 / Vision claims. Gate **0.6**. Gate2/3 untouched. No fake VL. gen11 HOLD unless fresh≥0.99.

## Progress

| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C65-C69 | prior batch | DONE | heldout 1.0 / LoRA -0.1 | C65-C69 |
| C70-C75 | prior batch | DONE | V3 dense 1.0 / LoRA ceiling | C70-C75 |
| C76 | v3-heldout-fix | DONE | n=9 | C76_*.json |
| C77 | v3-heldout-smoke | DONE | rate=1.0 claim=True | C77_*.json |
| C78 | vision-route-policy | DONE | rate=1.0 | C78_*.json |
| C79 | real-ocr-path | DONE | tess=False vl=1.0 | C79_*.json |
| C80 | dual-cost-refresh | DONE | replace=1.0 | C80_*.json |
| C81 | gen11-hold | DONE | HOLD | C81_*.json |
| C82 | docs | DONE | STAGE/CHECKPOINT | C82_*.json |

## Batch C76-C82 — DONE
- V3 heldout harder set claimed only if ≥0.6 (got 1.0)
- Routing policy code + smoke
- Honest OCR path (no tesseract; VL path works)
- gen11 HOLD


## Batch C83-C90 · DONE (2026-10-19T01:12:09+08:00)
| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C83 | ocr-weak-fixtures | DONE | train=8 test=8 | C83_*.json |
| C84 | ocr-weak-bare | DONE | rate=0.0 | C84_*.json |
| C85 | ocr-weak-lora-absorb | DONE | ok=True | C85_*.json |
| C86 | lora-vs-bare-weak | DONE | Δ=0.0 LORA_NEUTRAL_WEAK_OCR_PREFER_BARE | C86_*.json |
| C86b | lora-policy | DONE | default=bare | C86b_*.json |
| C87 | e2e-vision-office | DONE | pass=True | C87_*.json |
| C88 | user-sandbox-u2c | DONE | pass=True | C88_*.json |
| C89 | gen11-hold | DONE | HOLD | C89_*.json |
| C90 | docs | DONE | STAGE/CHECKPOINT | C90_*.json |

Knives closed: weak-LoRA hunt · e2e product loop · shadow U2C · tesseract skip · gen11 HOLD.

## Batch C91-C99 — DONE (2026-10-19T01:33:15+08:00)
| Cycle | Theme | Status | Key | Evidence |
| --- | --- | --- | --- | --- |
| C91 | e2e-multihop | DONE | ocr=1.0 atom=1.0 | C91_*.json |
| C92 | live-u2c-growth | DONE | crystal=1.0 n=6 | C92_*.json |
| C93 | replace-stress-mix | DONE | replace=1.0 ratio~3.2 | C93_*.json |
| C94 | desktop-capture | DONE | grab+VL hit | C94_*.json |
| C95 | gen11-hold | DONE | HOLD | C95_*.json |
| C96 | dissolve-refresh | DONE | pointers | C96_*.json |
| C97 | multihop-heldout | DONE | rate=1.0 | C97_*.json |
| C98 | hybrid-bare | DONE | rate=1.0 | C98_*.json |
| C99 | docs | DONE | STAGE/CHECKPOINT | C99_*.json |

Knives: harder multihop E2E · live U2C · replace stress · real desktop capture · gen11 HOLD.

## C100-C106 @ 2026-10-19T01:41:17+08:00
- C100 protocol pass=True
- C101 V4 rate=1.0 claim=True
- C102 desktop E2E pass=True paid=40.0
- C103 U2C crystal=1.0 reuse_ok=True
- C104 replace bare=1.0 ratio=3.3125
- C105 gen11 HOLD seal=False

## C107-C112 @ 2026-10-19T02:03:13+08:00
- C107 rate=1.0 claim=True
- C108 bare=0.0 trained=0.0 delta=0.0
- C109 pass=True paid=30.0
- C110 bare=None ratio=None
- C111 HOLD seal=False

## C107-C112 @ 2026-10-19T02:07:11+08:00
- C107 rate=1.0 claim=True
- C108 bare=0.0 trained=0.0 delta=0.0
- C109 pass=True paid=30.0
- C110 bare=1.0 ratio=3.3333
- C111 HOLD seal=False

## C107-C112 @ 2026-10-19T02:09:54+08:00
- C107 rate=1.0 claim=True
- C108 bare=0.0 trained=0.3333 delta=0.3333
- C109 pass=True paid=30.0
- C110 bare=1.0 ratio=3.3333
- C111 HOLD seal=False

## C107-C112 @ 2026-10-19T02:10:11+08:00
- C107 rate=1.0 claim=True
- C108 bare=0.0 trained=0.3333 delta=0.3333
- C109 pass=True paid=30.0
- C110 bare=1.0 ratio=3.3333
- C111 HOLD seal=False

## C113-C119 (2026-10-19T02:38:31+08:00)
- C113 grow pairs → C114 absorb push (trained=0.0, gate_pass=False, claim=False)
- C115 capture harden tests=1.0
- C116 V5 design/smoke claim=False
- C117 dashboards · C118 gen11 HOLD · C119 docs
- Iron: Gate 0.6, Gate2/3 untouched

## C125-C130 @ 2026-10-19T03:22:17+08:00
- C125 heldout fixtures pass=True n=12
- C126 heldout rate=1.0 claim=True
- C127 money_tool E2E pass=True rate=1.0
- C128 screenshot office pass=True rate=1.0
- C129 replace ratio=2.6
- C130 gen11 HOLD
- Iron: Gate 0.6, Gate2/3 untouched

## C131-C136 @ 2026-10-19T03:34:18+08:00
- C131 V6 design n=14 pass=True
- C132 V6 smoke rate=1.0 claim=True
- C133 capture demo oneshot=True
- C134 unified replace rate=1.0 mean_ratio=3.425
- C135 U2C money_tool rate=1.0 absorb_claim=False
- C136 gen11 HOLD
- Iron: Gate 0.6, Gate2/3 untouched
## C137-C142 @ 2026-10-19T03:44:18+08:00
- C137 heldout fixtures pass=True n=14
- C138 heldout rate=1.0 claim=True
- C139 regression pass=True rate=1.0
- C140 confidence-gate pass=True rate=1.0
- C141 replace mean_ratio=3.875 pass=True
- C142 gen11 HOLD
- Iron: Gate 0.6, Gate2/3 untouched

## C153–C157 (2026-10-19 04:26 Asia/Shanghai)
- C153: V7 linen/rowN fix → train **1.0** (was 0.875); fixed v7_09/v7_13
- C154: V8 fixtures n=18 harder than V7
- C155: V8 smoke **0.7222** CLAIM (≥0.6)
- C156: week sandbox 7d rate=1.0 week_paid=1526
- C157: scorecard refresh; gen11 HOLD; Gate2/3 untouched


## C162–C165 (2026-10-19T05:05:52+08:00)
- C162: fix OCR glue 14.ok → V8 heldout 0.9375→**1.0** (reparse claim refresh)
- C163: V9 smoke real VL **1.0 CLAIM** (after C160 arg-order fixture regen)
- C164: V9 heldout **1.0 CLAIM**
- C165: product regression overall **1.0**; gen11 HOLD; Gate2/3 untouched


## C166–C170 (2026-10-19T05:38:02+08:00)
- C166: V10 fixtures n=18 harder sticky/coffee/zorder/fade/chatbait
- C167: V10 smoke rate=1.0 claim=True fail=[]
- C168: desktop multiwin ImageGrab batches rate=1.0 pass=True
- C169: regression V4–V9 core=1.0 pass=True
- C170: scorecard composite=1.0; gen11 HOLD; Gate2/3 untouched

## C171-C174 @ 2026-10-19T06:11:18+08:00
- C171 V10 heldout rate=1.0 claim=True
- C172 V11 design n=18
- C173 V11 smoke rate=1.0 claim=True
- C174 scorecard composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C175-C179 @ 2026-10-19T06:25:07+08:00
- C175 V11 heldout rate=1.0 claim=True
- C176 V12 design n=18
- C177 V12 smoke rate=0.6111 claim=True
- C178 capture README regression pass=False
- C179 scorecard composite=0.8264 STAGE_READY=False
- gen11 HOLD; Gate2/3 untouched

## C175-C179 @ 2026-10-19T06:25:48+08:00
- C175 V11 heldout rate=1.0 claim=True
- C176 V12 design n=18
- C177 V12 smoke rate=0.6111 claim=True
- C178 capture README regression pass=True
- C179 scorecard composite=0.9514 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C175-C179 @ 2026-10-19T06:28:59+08:00
- C175 V11 heldout rate=1.0 claim=True
- C176 V12 design n=18
- C177 V12 smoke rate=1.0 claim=True
- C178 capture README regression pass=True
- C179 scorecard composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C181-C185 (2026-10-19T06:38:59+08:00)
- V12 heldout rate=1.0 claim=True
- V13 rate=1.0 claim=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C186-C190 (2026-10-19T06:48:00+08:00)
- V13 heldout rate=1.0 claim=True
- V14 rate=1.0 claim=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C191-C195 (2026-10-19T06:59:40+08:00)
- V14 heldout rate=1.0 claim=True
- V15 rate=1.0 claim=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C196-C200 (2026-10-19T07:11:31+08:00)
- V15 heldout rate=1.0 claim=True
- V16 rate=1.0 claim=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C201-C206 (2026-10-19T07:23:34+08:00)
- V15 heldout rate=1.0 claim=True
- V16 rate=1.0 claim=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C201-C206 (2026-10-19T07:24:09+08:00)
- V16 heldout rate=1.0 claim=True
- V17 rate=1.0 claim=True
- conf_gate rate=1.0 pass=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C207-C212 (2026-10-19T07:34:49+08:00)
- V17 heldout rate=1.0 claim=True
- V18 rate=0.6667 claim=True fail=['v18_02', 'v18_06', 'v18_08', 'v18_09', 'v18_16', 'v18_17']
- conf_gate_wire rate=1.0 pass=True
- capture_pass=True composite=0.9667 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C213-C216 (2026-10-19T07:46:58+08:00)
- V18 refresh rate=1.0 (was 0.6667) claim=True fail=[]
- V18 heldout rate=1.0 claim=True disjoint
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C217-C223 (2026-10-19T08:01:43+08:00)
- V19 prior rate=0.0556 (honest crush jpeg_q22)
- V19 refresh rate=1.0 (was 0.0556) claim=True fail=[]
- V19 heldout rate=1.0 claim=True disjoint
- multi_metric rate=1.0 pass=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C224-C229 (2026-10-19T08:14:57+08:00)
- V20 design clarity_floor jpeg_q=60 (no C218 crush)
- V20 rate=1.0 claim=True
- V20 heldout rate=1.0 claim=True disjoint
- multi_metric deepen rate=1.0 pass=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C230-C235 (2026-10-19T08:40:34+08:00)
- V21 design staple/HL/skew/bleed/tear/moire clarity_floor jpeg_q=60
- V21 rate=0.9444 claim=True
- V21 heldout rate=1.0 claim=True disjoint
- clarity_floor product pass=True
- capture_pass=True composite=1.0 stage_ready=True
- gen11 HOLD; Gate2/3 untouched

## C236-C241 (2026-10-19T09:00:33+08:00)
- V21 refresh rate=1.0 claim=True
- V22 smoke=1.0 heldout=1.0 claims=True/True
- composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C242-C247 (2026-10-19T09:18:14+08:00)
- V23 smoke=1.0 heldout=1.0 claims=True/True
- cost_ledger pass=True replace_ratio=3.4788
- composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C248-C253 (2026-10-19T09:33:51+08:00)
- V24 smoke=1.0 heldout=1.0 claims=True/True
- polish pass=True; capture pass=True
- composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C248-C253 (2026-10-19T09:34:08+08:00)
- V24 smoke=1.0 heldout=1.0 claims=True/True
- polish pass=True; capture pass=True
- composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C254-C259 (2026-10-19T09:51:23+08:00)
- V25 smoke=1.0 heldout=1.0 claims=True/True
- innov pass=True; capture pass=True
- composite=1.0 STAGE_READY=True
- gen11 HOLD; Gate2/3 untouched

## C260-C265 (2026-10-19T10:10:34+08:00)
- V26 smoke=1.0 claim=True; heldout=1.0 claim=True
- C263 dissolve/cost/shadow pass=False; replace≈3.9188
- composite=0.8333 STAGE_READY=False; gen11 HOLD

## C260-C265 (2026-10-19T10:11:02+08:00)
- V26 smoke=1.0 claim=True; heldout=1.0 claim=True
- C263 dissolve/cost/shadow pass=False; replace≈3.9188
- composite=0.8333 STAGE_READY=False; gen11 HOLD

## C260-C265 (2026-10-19T10:11:21+08:00)
- V26 smoke=1.0 claim=True; heldout=1.0 claim=True
- C263 dissolve/cost/shadow pass=True; replace≈3.9188
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C266-C271 (2026-10-19T10:37:44+08:00)
- V27 smoke=0.9444 claim=True; heldout=1.0 claim=True
- C269 conf-gate stretch pass=True rate=1.0; replace≈3.9188
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C277 (2026-10-19T11:39:00+08:00)
- V28 smoke=1.0 claim=True; heldout=1.0 claim=True
- C275 u2c-replace stretch pass=True rate=1.0; replace≈3.725
- composite=0.9286 STAGE_READY=False; gen11 HOLD

## C272-C277 (2026-10-19T11:39:48+08:00)
- V28 smoke=1.0 claim=True; heldout=1.0 claim=True
- C275 u2c-replace stretch pass=True rate=1.0; replace≈3.725
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C277 (2026-10-19T11:39:53+08:00)
- V28 smoke=1.0 claim=True; heldout=1.0 claim=True
- C275 u2c-replace stretch pass=True rate=1.0; replace≈3.725
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C283 (2026-10-19T12:22:48+08:00)
- V29 smoke=1.0 claim=True; heldout=1.0 claim=True
- C275 u2c-replace stretch pass=True rate=1.0; replace≈3.725
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C289 (2026-10-19T12:41:52+08:00)
- V30 smoke=1.0 claim=True; heldout=1.0 claim=True
- C287 confidence-gate stretch pass=True rate=1.0; replace≈3.9188
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C289 (2026-10-19T12:42:07+08:00)
- V30 smoke=1.0 claim=True; heldout=1.0 claim=True
- C287 confidence-gate stretch pass=True rate=1.0; replace≈3.9188
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C289 (2026-10-19T12:42:21+08:00)
- V30 smoke=1.0 claim=True; heldout=1.0 claim=True
- C287 confidence-gate stretch pass=True rate=1.0; replace≈3.725
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C295 (2026-10-19T13:15:02+08:00)
- V31 smoke=1.0 claim=True; heldout=1.0 claim=True
- C293 dissolve/shadow pass=True; conf-gate=True/1.0; replace≈3.725
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C295 (2026-10-19T13:15:47+08:00)
- V31 smoke=1.0 claim=True; heldout=1.0 claim=True
- C293 dissolve/shadow pass=True; conf-gate=True/1.0; replace≈4.1625
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C272-C301 (2026-10-19T16:33:33+08:00)
- V32 smoke=1.0 claim=True; heldout=1.0 claim=True
- C299 product/U2C pass=True rate=1.0; conf-gate=True/1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C296-C301 (2026-10-19T16:35:07+08:00)
- V32 smoke=1.0 claim=True; heldout=1.0 claim=True
- C299 product/U2C pass=True rate=1.0; conf-gate=True/1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C296-C307 (2026-10-19T17:11:11+08:00)
- V33 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C296-C313 (2026-10-19T18:20:20+08:00)
- V34 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C296-C313 (2026-10-19T18:21:53+08:00)
- V34 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C296-C313 (2026-10-19T18:23:31+08:00)
- V34 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C308-C313 (2026-10-19T18:26:34+08:00)
- V34 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C308-C313 (2026-10-19T18:28:42+08:00)
- V34 smoke=1.0 claim=True; heldout=1.0 claim=True
- C305 conf-gate pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C314-C319 (2026-10-19T23:48:34+08:00)
- V35 smoke=1.0 claim=True; heldout=1.0 claim=True
- C317 product/u2c pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C314-C325 (2026-10-20T00:53:14+08:00)
- V36 smoke=0.8889 claim=True; heldout=1.0 claim=True
- C317 dissolve/shadow pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C314-C331 (2026-10-20T01:24:44+08:00)
- V37 smoke=1.0 claim=True; heldout=1.0 claim=True
- C317 confidence/stretch pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C314-C337 (2026-10-20T02:01:27+08:00)
- V38 smoke=0.9444 claim=True; heldout=1.0 claim=True
- C317 product/u2c pass=True rate=1.0; product C299=1.0; replace≈4.0694
- composite=1.0 STAGE_READY=True; gen11 HOLD

## C345 scorecard (2026-10-20T03:14:55+08:00)
- V39 smoke/heldout 1.0/1.0 claim=True/True
- C344 product/u2c pass=True replace=4.0694
- C343 capture pass=True; composite=1.0; STAGE_READY=True
- entry: docs/STAGE_ANT_C343.md


## C351 tip
- composite=1.0 STAGE_READY=True v40=1.0/1.0


## C357 tip
- composite=1.0 STAGE_READY=True v41=0.9444/1.0
