"""Prepare the ARMS-UP subject cutout (July 2026 "What's New" thumbnail).

This plate needs no un-mirroring and no white balance: measured skin R/B is
already 1.58 (the tungsten-cast plates were 2.15). Two passes only:

1. Speck removal — the matte leaves ~10 one-to-two-pixel islands (beard/glasses
   highlights plus a stray dot out at x=129). Keep only the largest connected
   component.
2. Matte hardening + brand grade — same treatment as grade_subject_r.py so the
   cutout sits on the dark violet frame the same way.

    python3 assets/img/grade_subject_july.py
    hussain-plate-july-cut.png -> hussain-plate-july-graded.png
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = "assets/img/hussain-plate-july-cut.png"
DST = "assets/img/hussain-plate-july-graded.png"

SATURATION = 0.95
VIOLET = np.array([0.47, 0.34, 0.93], dtype=np.float32)  # --brand #7757ee
SHADOW_TINT = 0.14
CONTRAST = 1.06
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
ALPHA_LO, ALPHA_HI = 0.35, 0.92
ALPHA_FEATHER = 0.6  # px

im = np.array(Image.open(SRC).convert("RGBA")).astype(np.float32)
rgb, alpha = im[:, :, :3] / 255.0, im[:, :, 3] / 255.0

# 1. keep only the largest connected component of the matte
labels, n = ndimage.label(alpha > 0.06)
sizes = ndimage.sum(alpha > 0.06, labels, range(1, n + 1))
alpha = np.where(labels == (int(np.argmax(sizes)) + 1), alpha, 0.0)

# 2. brand grade
lum = (rgb * LUMA).sum(axis=2, keepdims=True)
rgb = lum + (rgb - lum) * SATURATION
shadow = np.clip(1.0 - lum * 2.2, 0.0, 1.0) ** 1.5
rgb = rgb * (1.0 - SHADOW_TINT * shadow) + VIOLET * (SHADOW_TINT * shadow) * lum.clip(0.04, 1.0)
rgb = np.clip((rgb - 0.5) * CONTRAST + 0.5, 0.0, 1.0)

# harden the matte: drop the low-alpha halo, keep a crisp soft edge
a = np.clip((alpha - ALPHA_LO) / (ALPHA_HI - ALPHA_LO), 0.0, 1.0)
a = np.array(Image.fromarray((a * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(ALPHA_FEATHER))).astype(np.float32)

out = np.concatenate([rgb * 255.0, a[:, :, None]], axis=2)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(DST)
print(f"wrote {DST} ({n} components -> 1, matte hardened {ALPHA_LO}-{ALPHA_HI})")
