# 简报（2026-10-17 01:50）— Office 墙诊断与 F1

门控 **0.6 未降**。

## 诊断（docs/OFFICE_DIAGNOSIS.md）

n=160 mean=0 **不是** dual 学不会，而是 **reference 天花板**：各臂 exam≈1.0，paired 差分为 0；dual writes=80 但 train_tokens=0。

## 最高杠杆修复 F1

`reference_gate: notes_open_book`：agent/dual_agent 无检索轨迹则失败；dual 保留 scripted（内化代理）。

短烟：`mean=1.0`，`informative=true`，**明确非 Gate2**（`gate2_claim=false`）。

## 其它

- Judge 增加 ceiling_tie / informative
- Router：model generate 可加载 atom LoRA（单测）
- Affine H-signal：配置已写，排在 overnight model office 之后
- Overnight 已启：`office_model_signal_smoke`（actor=model, steps=16）

## 提交将含

OFFICE_DIAGNOSIS、open_book/model smoke 配置、stream/judge 补丁、测试。