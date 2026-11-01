# Ant VL Gate V20 Protocol

Updated: 2026-10-19T08:05:34+08:00 (Asia/Shanghai)

## Purpose
Harder than V19 mild: crease grid, tape glare, carbon blue, halftone dots,
fold corner, wet edge, thermal stripe, fax header, fingerprint edge, clip shadow.
Clarity floor from C218 lesson (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V20 uses 60)
- photocopy downsample max **/2** (not /3)
- Gaussian blur radius <= **0.5**
- Protect text band y≈70–250 from glyph-wiping overlays
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C225)
- Claim only after smoke

## Honesty
- V19 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C224.
