# 蚁算截图办公 — 产品演示与使用说明

Updated: 2026-10-19 (Asia/Shanghai)

## 一句话
截屏 / 面板文字 → OCR（可走真实 VL）→ **money_tool 金额求和** → 办公原子 → 证据 JSON。  
脚手架步数固定很低，**不走**传统 agent 多跳图。

## 快速开始

```bash
cd E:\envolution
python scripts/ant_capture_office.py --expected-paid 16.5 --title "ANT CAPTURE DEMO"
```

常用参数：
- `--no-vl`：跳过视觉，只用给定行文本（干跑 / CI）
- `--outdir PATH`：指定输出目录
- `--lines-file PATH`：自定义行文本（每行一条）
- `--image PATH`：指定截图路径（有 VL 权重时用）

## 产物
- `evidence.json`：OCR 预览、paid 结果、money_tool 是否启用、是否通过
- 可选截图副本与中间 OCR 文本

## 能力边界（诚实）
- **能**：办公小票 / 订单 / 仓单类「paid / open / TARGET」求和；置信门控可在模型与工具打架时强制走 tool
- **不能**：开放域通用视觉、上游公开榜分数、无门控「已完全替代所有 agent」
- **多模态**：Qwen3.5-2B 本地 VL；Vision V0–V10 已有 scoped claim；heldout / 更高版以仓库 `docs/r50/` 为准

## 相关脚本
| 脚本 | 作用 |
| --- | --- |
| `scripts/ant_capture_office.py` | CLI 入口 |
| `scripts/ant_capture_office_lib.py` | 管道库（OCR→tool→原子） |
| `scripts/c133_capture_product_demo.py` | oneshot 演示证据 |
| `scripts/c139_product_demo_regression.py` | 产品回归 |

## 门控
- 产品与视觉 Gate：**0.6**
- Gate2 / Gate3 文本 claim：**不动**
- gen11：**HOLD**（密封包未开）

## 一键演示（推荐对外）
```bash
python scripts/c133_capture_product_demo.py
# 读 docs/蚁算_CAPTURE_OFFICE_DEMO.md 与 docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json
```


## 多指标（C227）
支持 `--metric` 与 `--expected`。详见 `docs/蚁算_MULTI_METRIC_CAPTURE.md`。

```bash
python scripts/ant_capture_office.py --no-vl --metric refund_done --expected 44.75 \
  --lines-file runs/multi_metric_capture_c227/mm_refund_lines.txt \
  --outdir runs/multi_metric_capture_c227/cli_refund
```

Updated C227: 2026-10-19T08:14:00+08:00

## Clarity floor
- jpeg_q >= 58 (V21 uses 60); photocopy max /2; blur <= 0.5
- Protect TARGET text band; see docs/蚁算_CLARITY_FLOOR.md
- Lesson: C218 jpeg crush → honest fail; do not reopen crush path
