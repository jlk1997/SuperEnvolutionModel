# 蚁算 Capture Office 产品演示

Updated: 2026-10-19T03:27:37+08:00 (Asia/Shanghai)

## 一句话
截屏/面板 → OCR（可选 VL）→ **money_tool 求和** → 办公原子 → 证据 JSON。脚手架步数固定低，不走 agent 图。

## 一键命令
```bash
cd E:\envolution
python scripts/ant_capture_office.py --expected-paid 16.5 --title "ANT CAPTURE DEMO"
```

可选：
- `--no-vl` 跳过视觉（本演示默认 dry 已证明 money_tool）
- `--outdir PATH` 指定输出
- `--lines-file PATH` 自定义行文本
- `--dry-run` 仅构建面板与证据骨架

## 证据字段（schema）
`entry, timestamp, gate, capture_ok, size, use_vl, scaffold_steps, agent_graph, ocr_ok, paid_got, paid_expected, paid_ok, atom_ok, ok, pass, rate, errors`  
另含 `money_tool` / `money_policy`（C127+）。

## 本轮 one-shot
- expected_paid: **16.5**
- paid_got: **16.5**
- money_tool: **True**
- ok: **True**
- evidence: `docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json`

## 诚实边界
- 金额算术走 **tool**，不靠 1.5B LoRA 心算（C120 天花板）
- 稠密表视觉路由优先 **bare**
- 不冒充 Gate2/3；gen11 HOLD

## Regression C139 (2026-10-19T03:39:14+08:00)
- pass: **True** rate=1.0
- evidence: `docs/r50/C139_PRODUCT_DEMO_REGRESSION.json`
- V4/V5/V6 smoke pointers checked: 4/6
