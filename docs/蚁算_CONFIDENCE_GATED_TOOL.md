# 蚁算 · 置信门控工具（Confidence-Gated Tool Use）

Updated: 2026-10-19T03:39:14+08:00 (Asia/Shanghai)

## 创新点
模型给出金额猜测时，不盲目信模型算术；与 **money_tool** 比对：
- **一致** → confidence=high，仍取 tool 值（可审计）
- **不一致** → confidence=low，**强制用 tool**（安全）
- **无模型猜测** → confidence=low，用 tool

## 证据
- `docs/r50/C140_CONFIDENCE_GATED_TOOL.json`
- rate=1.0000 pass=True
- 政策：`evo/office/product_money_policy.json`

## 边界
- 不构成 U2C 算术 absorb claim（C120 天花板仍在）
- Gate2/3 不动；gen11 HOLD
