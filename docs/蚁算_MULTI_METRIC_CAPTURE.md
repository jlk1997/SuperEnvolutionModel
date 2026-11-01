# 蚁算多指标截图办公（C227）

Updated: 2026-10-19T08:14:00+08:00 (Asia/Shanghai)

## 一句话
一次 capture 会话可按 `--metric` 评估：`paid_total` / `qty_sum` / `refund_done` /
`tax_base_paid` / `payroll_active` / `ship_ok_qty` / `open_pri_sum`。
模型与工具不一致时 **置信门控强制走 tool**。

## CLI

```bash
python scripts/ant_capture_office.py --no-vl --metric qty_sum --expected 78 \
  --lines-file path/to/lines.txt --outdir runs/demo_qty
```

兼容：未传 `--metric` 时仍为 `paid_total`；`--expected-paid` 仍可用。

## 指标表
| metric | 工具语义 |
| --- | --- |
| paid_total | 求和 status=paid |
| qty_sum | 求和 `qty N ok` |
| refund_done | 求和 `N done` |
| tax_base_paid | 求和 `N paid`（税基） |
| payroll_active | 求和 `N active` |
| ship_ok_qty | 求和 `N ok` |
| open_pri_sum | 求和 `pri N open` |

## 门控
Gate **0.6**。Gate2/3 不动。gen11 HOLD。
