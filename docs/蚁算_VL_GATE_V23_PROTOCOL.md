# Ant VL Gate V23 Protocol

Updated: 2026-10-19T09:09:33+08:00 (Asia/Shanghai)

## Purpose
Harder than V22: highlighter bleed, paperclip shadow, hole punch,
rubber stamp overlap, folded corner, thermal fade, dust speckle,
red ink bleed, laminated glare, stapler dent, margin crop, barcode occlusion.
Clarity floor from C218/V20/V21 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V23 uses 60)
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C238)
- Claim only after smoke

## Honesty
- V21 train refresh (C236) / heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C242.
