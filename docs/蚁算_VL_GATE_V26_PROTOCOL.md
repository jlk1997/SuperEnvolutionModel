# Ant VL Gate V26 Protocol

Updated: 2026-10-19T10:02:09+08:00 (Asia/Shanghai)

## Purpose
Harder than V25: highlighter bleed, crumpled corner, rubber band, paperclip shadow,
grease smear, carbon copy, stamp overlap, folded pocket, dust speckle,
binder hole, ticket perforation, polaroid frame, whiteboard glare,
sticky-note cover, pen underline noise, fax header bait, envelope window, laminate shine.
Clarity floor from C218/V20-V25 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V26 uses 60)
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V25 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C260.
