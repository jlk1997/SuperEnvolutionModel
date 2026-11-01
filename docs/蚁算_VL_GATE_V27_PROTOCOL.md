# Ant VL Gate V27 Protocol

Updated: 2026-10-19T10:20:26+08:00 (Asia/Shanghai)

## Purpose
Harder than V26: highlighter cross, magnetic clip, thermal fade, coffee splash edge,
double-fold corner, pencil scribble, stapler puncture, watermark diagonal,
phone shadow, receipt skew stack, blue pen circles, red correction tape,
shipping label edge, binder clip top, sticky peel corner.

Clarity floor from C218/V20-V25 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V27 uses 60)
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V26 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C266.
