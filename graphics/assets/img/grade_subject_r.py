"""Prepare the RIGHT-facing subject cutout (mirror thumbnail variant).

Same corrections as grade_subject.py (un-mirror + tungsten white-balance), plus
an alpha-matte hardening pass: the background-removal model leaves a soft
semi-transparent halo (alpha ~0.1-0.9) around the wrist/cuff. On the dark frame
that halo shows the retained wall pixels as a faint patch, so we remap alpha
[0.55..0.90] -> [0..1] (dropping the low fringe) and feather 0.6px for a crisp
but non-jagged edge.

    python3 assets/img/grade_subject_r.py
    hussain-plate-r-cut.png -> hussain-plate-r-graded.png
"""
import numpy as np
from PIL import Image, ImageFilter

SRC = "assets/img/hussain-plate-r-codex-cut.png"   # codex-produced matte (cleaner)
DST = "assets/img/hussain-plate-r-graded.png"

GAIN = np.array([0.94, 0.98, 1.26], dtype=np.float32)   # lit skin R/B 2.15 -> ~1.6
SATURATION = 0.90
VIOLET = np.array([0.47, 0.34, 0.93], dtype=np.float32)  # --brand #7757ee
SHADOW_TINT = 0.14
CONTRAST = 1.06
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
ALPHA_LO, ALPHA_HI = 0.35, 0.92   # light matte tidy (codex matte is already clean)
ALPHA_FEATHER = 0.6               # px

im = np.array(Image.open(SRC).convert("RGBA")).astype(np.float32)
rgb, alpha = im[:, :, :3] / 255.0, im[:, :, 3:4] / 255.0

rgb *= GAIN
lum = (rgb * LUMA).sum(axis=2, keepdims=True)
rgb = lum + (rgb - lum) * SATURATION
shadow = np.clip(1.0 - lum * 2.2, 0.0, 1.0) ** 1.5
rgb = rgb * (1.0 - SHADOW_TINT * shadow) + VIOLET * (SHADOW_TINT * shadow) * lum.clip(0.04, 1.0)
rgb = np.clip((rgb - 0.5) * CONTRAST + 0.5, 0.0, 1.0)

# harden the matte: drop the low-alpha halo, keep a crisp soft edge
a = np.clip((alpha[:, :, 0] - ALPHA_LO) / (ALPHA_HI - ALPHA_LO), 0.0, 1.0)
a = np.array(Image.fromarray((a * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(ALPHA_FEATHER))).astype(np.float32)

out = np.concatenate([rgb * 255.0, a[:, :, None]], axis=2)
out = np.fliplr(out)          # un-mirror selfie: faces RIGHT, BWH logo reads correctly
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(DST)
print(f"wrote {DST} (un-mirrored, matte hardened {ALPHA_LO}-{ALPHA_HI})")
