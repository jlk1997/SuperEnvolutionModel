# Ant VL Gate V360 Protocol

Updated: 2026-10-29T18:35:03+08:00 (Asia/Shanghai)

## Purpose
Harder than V358: rust clip, wet smudge, hole punch, rubber band slant,
desk glare, label overlap, fountain blot, paperclip chain,
fax noise, sticky tab, crease X, stamp over-ink,
tape residue, pencil shade, coffee ring center.

Clarity floor from C218/V20-V25 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V360 uses 62)
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V26 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C2267.
