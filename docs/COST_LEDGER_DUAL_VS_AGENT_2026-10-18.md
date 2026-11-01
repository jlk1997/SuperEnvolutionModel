# Dual vs Agent 成本账本（蚁算 v0.2.5 stub）

时间：2026-10-18T22:41:15+08:00（Asia/Shanghai）
方法：archival_summary_steps ｜ Gate **0.6** ｜ tokens 暂不可用

判断：**PASS**（有归档摘要可聚合）

## 汇总
- reports=4
- dual_steps_mean=9.125
- agent_steps_mean=5.625
- step_delta (agent−dual)=-3.5
- dual_fail_rate_mean=0.28125
- agent_fail_rate_mean=0.875

| summary | seed | dual_ok | agent_ok | dual_steps | agent_steps | dual_fail | agent_fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `runs/office_gate2_full_slate_s0/20261017-201213/summary.json` | 0 | 0.75 | 0.25 | 8.5 | 6.0 | 0.25 | 0.75 |
| `runs/office_gate2_full_slate_s1/20261017-210105/summary.json` | 1 | 0.5 | 0.0 | 8.5 | 5.25 | 0.5 | 1.0 |
| `runs/office_gate2_mid_n_dual_s0/20261018-105958/summary.json` | 0 | 0.875 | 0.25 | 10.5 | 5.625 | 0.125 | 0.75 |
| `runs/office_gate2_mid_n_dual_s1/20261018-114219/summary.json` | 1 | 0.75 | 0.0 | 9.0 | 5.625 | 0.25 | 1.0 |

## 说明
- Gate2/3 CLAIM 不动。
- tokens 需后续从 model_turn_log 补齐。
- 无 VL。

