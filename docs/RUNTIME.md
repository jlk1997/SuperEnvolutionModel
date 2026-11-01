# 运行

可塑性进化的搜索分两截。推演要快，更新要能按基因组给不同位置不同的学习率。一台 8GB 笔记本做不了种群推演，只跑机制模型和冒烟。

## 这台机器

```text
python -m evo plast --stage all
python -m evo plast --stage m0 --config configs/evoplast_m0.yaml
python -m evo unit
```

默认 `actor: reference`，不加载语言模型。`backend` 默认 `transformers`。

语言模型的 M0 把配置里的 `actor` 改成 `model`，并指向本地权重。闸门是出生成功率低于 0.2，预算内不低于 0.6。没过就换 Qwen3.5-2B 或 4B，或把难度调到首回合 0.1 到 0.4。不要把闸门改低。



## 语言模型 M0（Epoch A-2）

参考体 M0 与语言模型 M0 不是同一道闸。

- **参考体**：`python -m evo plast --stage m0 --config configs/evoplast_m0.yaml`（`actor: reference`，不加载权重）。看顶层 `m0.passed`。
- **语言模型**：必须用 fit 配置，不要只改 `evoplast_m0.yaml` 的 actor：

```text
python -m evo plast --stage m0 --config configs/evoplast_fit.yaml
```

成功标准看 **`m0.model.passed`**（以及 `m0.lm_passed`），**不要**只看顶层 `m0.passed`——后者只表示参考体通过。CLI 会同时打印 `m0_reference` 与 `m0_lm`。

闸门：held-out 相关成功率仍为 **0.6**。失败时先试 `configs/evoplast_fit_add.yaml`（只学加法）或加强 replay；仍失败再换更大基座。**禁止降低 0.6。**

`actor: model` 时会经 `evo.registry.require_ready` 校验本地权重，缺权重直接失败，不会静默回退到残缺的 0.8B。



## 语言模型可塑性普查（Epoch A-3）

预注册路径（先 dry / smoke，再全速）：

```text
python -m evo plast --stage census --config configs/evoplast_census_dry.yaml
python -m evo plast --stage census --config configs/evoplast_census_smoke.yaml
python -m evo plast --stage census --config configs/evoplast_census.yaml
```

产物：`runs/evoplast_census*.json`。闸门仍为 0.6。全速 = 3 seeds × {mlp, attn, attn_mlp} × skill，笔记本上很长；smoke 只跑 seed0 + mlp + add。

## Linux GPU

24GB 以上的卡，用来跑种群。一个冻结基座，每个个体一块 LoRA。vLLM 只负责按温度采样，更新仍走本仓库的 LoRA 步。

```text
pip install vllm
export EVO_BACKEND=vllm
python -m evo plast --stage es --config configs/evoplast_es.yaml
```

没装 vLLM 就设 `EVO_BACKEND=vllm` 会直接失败，不会悄悄退回慢路径。采样组大小至少 8，温度大于 0，这两项在 [evo/plastic/signal.py](../evo/plastic/signal.py) 里，配置写得再小也会被抬上去。

Unsloth 可以替换训练那一截，不替换基因组、任务流和指标。换训练器时保持三件事：按位置分组的学习率、执行器判分、考题不进更新。

## Stack M0 status (Epoch A)

Addition-only LM M0 (`configs/evoplast_fit_add.yaml`) **passes** on Qwen2.5-1.5B (MLP LoRA, gate 0.6).

Stack (addition + second skill) now picks an affine `(n*a+b) mod 50` with **birth &lt; 0.5**, so the birth gate works. On 1.5B + MLP-only + solo replay, **second_report stayed ~0.25** and did not clear 0.6. Do **not** lower the gate. Next capacity knobs (future): `lora_preset` / sites including attention (`configs/evoplast_fit_stack_attn.yaml`), more `solo_epochs`, or a larger base — still keep competence ≥ 0.6.

