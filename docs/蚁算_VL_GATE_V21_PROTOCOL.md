# Ant VL Gate V21 Protocol

Updated: 2026-10-19T08:36:52+08:00 (Asia/Shanghai)

## Purpose
Harder than V20: stapler holes, highlighter lane, desk skew, stamp bleed,
paper tear, moire screen, dense watermark, desk shadow, rust staple, dogear.
Clarity floor from C218/V20 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V21 uses 60)
- photocopy downsample max **/2** (not /3)
- Gaussian blur radius <= **0.5**
- Protect text band y≈70–250 from glyph-wiping overlays
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C231)
- Claim only after smoke

## Honesty
- V20 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C230.
