# 蚁算 C149–C152 阶段交付

- **C149** 修复 atom parse（`qty_sum` / `tax_base_paid` / `payroll_active` / `N paid` 词序）并复测 V7；门控仍 0.6
- **C150** V7 heldout 不相交集；claim 条件 rate≥0.6
- **C151** 业务日沙箱扩到多日多文件
- **C152** 统一计分板刷新
- **gen11** HOLD；Gate2/3 不动


## Results (2026-10-19T04:11:27+08:00)

| cycle | result |
|-------|--------|
| C149 | V7 rate 0.875 (was 0.75); fixed stamp_wh/tax/payroll/expense |
| C150 | V7 heldout rate 1.0 CLAIM |
| C151 | 3 days / 18 files; week_paid=691.5 |
| C152 | composite 0.9857 |

gen11 HOLD. Gate 0.6. Gate2/3 untouched.
