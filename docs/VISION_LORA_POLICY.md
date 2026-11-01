# Vision LoRA Policy (蚁算-视)

Updated from C66 / C72 / C86 (Asia/Shanghai).

## Dense tables
**DEPRECATED → force bare.** Evidence: C66 Δ=-0.1, C72 retest still regresses on dense stock/defect cells.

## Weak OCR hunt (C83–C86)
- Harder `ocr_weak` fixtures: bare soft=0.0 strict=0.0 (weak domain found).
- Micro-LoRA absorb ok (16 steps) on train-only.
- LoRA vs bare on disjoint test (strict must_codes): **both 0.0, Δ=0.0**.
- Decision: `LORA_NEUTRAL_WEAK_OCR_PREFER_BARE`.

## Product default
**bare** for vision office. LoRA adapters may remain registered for research, but `vision_route` only enables LoRA on `WEAK_LORA_OK` domains when adapter present **and** future cycles prove Δ>0.

## OCR path
Tesseract infeasible on jlk → stick **VL OCR** (C79 / C90 reaffirm).

Gate 0.6. Gate2/3 untouched. No fake VL scores.
