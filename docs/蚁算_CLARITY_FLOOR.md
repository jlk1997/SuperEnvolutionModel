# 蚁算 Clarity Floor（截图办公可读性地板）

Updated: 2026-10-19T08:40:33+08:00 (Asia/Shanghai)

## Why
C218 jpeg_q22 + photocopy/3 crushed digits → V19 prior rate≈0.056.
V20+ enforce a **clarity floor** so VL gates test document understanding,
not jpeg destruction.

## Mandatory floor
| Knob | Min / Max | V21 value |
| --- | --- | --- |
| jpeg quality | >= **58** | 60 |
| photocopy downsample | max **/2** (not /3) | /2 |
| Gaussian blur radius | <= **0.5** | 0.45 |
| Text band protect | y≈70–250 | no glyph-wipe overlays on TARGET lines |

## Product rule
Capture-office demos and Vision V20+ fixtures MUST respect this floor.
Gate remains **0.6**. Gate2/3 untouched. gen11 HOLD.
