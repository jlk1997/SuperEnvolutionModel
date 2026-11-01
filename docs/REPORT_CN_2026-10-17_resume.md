# 硬结果（2026-10-17 03:30 CST）— 不宣称 Gate2

门控 **0.6**。`docs/BLAST_PLAN.md` 已在。

## Office model
1. **F3 v1**：informative，dual=agent=**0**（tool 地板）。
2. **F3c v3**：dual **practice 8/8**、exam **0/8**、train_tokens=6400 — 学习通路打开，exam 未动。
3. **F3d/F3e**：去掉 chat_template `tools=`；放宽解析 `<function>shell>` / 匿名 parameter。
4. **v6 正在跑**（primer+parse+bootstrap）— GPU 未闲。

## Stack
Offset holdout ✅。Affine signal ❌。`affine_easy` 排队在 v6 后。

## Gate2
**未达成**。F1 proxy 与 practice-only 均不可作 Gate2。需 model exam 上 dual>agent 且 rate>0 再扩 n。