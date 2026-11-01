# 蚁算-视 · VL Gate 协议草案

更新日期：2026-10-18（Asia/Shanghai）  
状态：**PROTOCOL_DRAFT + STUBS_READY** · **无本地 VL 权重 · 禁止假训 / 假分**

## 1. 定位

**蚁算-视**是蚁算模型五层里的「视」感官生长轨：把图像（以及以后的页面截图/表格拍照）纳入同一条 **用 → 原子 → 核 → 双脑 → 迁** 进化链，而不是另起一套多模态 agent。

- 产品名：蚁算-视（Ant Compute Vision track）
- 引擎：仍属 Envolution / `evo`
- 与文本轨共享 Gate **0.6**；不因「有图」降门

## 2. 开闸硬条件（缺一不可）

1. 本地存在可用 VL/vision 权重目录（例如 `models/` 下可 `require_ready` 的多模态检查点）。
2. `docs/EPOCH_D_PREVIEW.md` 与本协议对齐后，CHECKPOINT 将 `OPEN_ONLY_VL` 改为可调度刀。
3. 至少一条 **CPU fixture stub** 绿（本仓库已预置），证明接线不依赖真权重。
4. 禁止：用文本模型假装看图、用人工标签冒充 dissolve bare、把上游 VL 榜成绩写进 CLAIM。

未满足 → **HARD defer**。可继续写协议、schema、fixture；不可写「已训 VL / 已过 VL Gate」。

## 3. 闸门草案（与文本对称）

| 闸门 | 名称 | 通过条件（草案） | 失败转向 |
| --- | --- | --- | --- |
| V0 | 权重就位 | registry 能加载 VL；smoke generate 含图输入不崩 | 停在 stub；不跑 GPU 长训 |
| V1 | 用-视 | use_log 写入 `image_ref` + 可回放事件；fixture 轮转绿 | 修 schema / 事件总线 |
| V2 | 原子-视 | 结晶出 `vision_*` atom 元数据（可无真权重，仅 stub） | 修 crystallizer 接口 |
| V3 | 核-视 | 有权重后：held-out 看图任务 bare≥0.6 且 D≤0.05 | 先查格式/泄漏，再加 n |
| V4 | 双脑-视 | dual-vision 对照 vision-agent 或文本-only 臂；配对 CI 规则同 Gate2 精神 | 吸收高频视觉工作流 |
| V5 | 迁-视 | 密封视觉包 transfer（Branch A/B 对齐 GATE3_PROTOCOL） | 烧包；只改学法 |

**CLAIM 规则**：V3 之前任何数字只能标 `fixture` / `protocol`；V3+ 才允许 `vl_gate_claim` 字段，且必须 `weights_local=true`。

## 4. use_log 图像字段（草案）

每条工具/观测事件可带：

```json
{
  "event": "observation",
  "modality": "image",
  "image_ref": {
    "uri": "runs/use_log/images/<hash>.png",
    "sha256": "<hex>",
    "width": 0,
    "height": 0,
    "mime": "image/png"
  },
  "text_caption": null,
  "task_id": "...",
  "family": "vision_table|vision_ui|vision_doc",
  "split": "practice|exam"
}
```

约束：

- 图文件落在仓库相对路径；考试题图不得进夜间训练清单（held-out 纪律同文本）。
- `text_caption` 若由模型生成，须标 `caption_source=model|human|none`，防止泄漏当监督。
- 无图事件 `modality=text`（默认），旧日志仍合法。

## 5. dissolve 视原子路径（草案）

1. `use_log`（含 image_ref）→ grade → pairs（多模态 pair：图像+指令 → tool_call/答案）
2. `crystallize` → `CapabilityAtom` 名约定 `vision_<family>_uselog`
3. `dissolve`：bare（无检索笔记）vs scaffold；算 D
4. 路由：`prefer_atoms` 可选视原子；与文本原子冲突时用既有 multi-atom 裁决

无权重时：只跑到「schema + fixture atom 元数据」；`dissolution.json` 可写 `status=stub_pending_weights`。

## 6. 与文本轨关系

- 共享：影子沙箱、审计、Gate0.6、密封包纪律、不降门。
- 不共享：在未 V0 前占用 GPU 长训队列；不得阻塞蚁算 v0.1 文本 STAGE_READY。

## 7. 近端（可无权重完成）

- [x] 本协议草案落盘
- [x] use_log 图像 schema fixture
- [x] vision atom stub + dissolve pending 标记
- [x] CHECKPOINT 多模态轨段落
- [ ] 本地 VL 权重就位后开 V0 smoke（未来刀）
