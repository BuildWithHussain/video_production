"""Prepare the subject cutout for the dark violet thumbnail frame.

Two corrections, both to the image as captured — never to the subject himself:

1. Un-mirror. The source is a selfie, so the front camera flipped it: the BWH
   chest logo reads "HWB". Flipping restores reality.
2. Colour. The source is tungsten-lit: measured R/B on the lit hand is 2.15,
   where neutral skin sits ~1.5-1.6 — that's what reads as "orange" against the
   cool #171717 surface. This corrects white balance, calms the residual
   saturation, and tints only the shadows toward the brand violet so the subject
   shares the frame's ambient light.

Geometry beyond the flip is untouched, and the matte is preserved as-is.

    python3 assets/img/grade_subject.py
    hussain-plate.png -> hussain-plate-graded.png
"""
import numpy as np
from PIL import Image

SRC = "assets/img/hussain-plate.png"
DST = "assets/img/hussain-plate-graded.png"

# white balance: takes lit skin from R/B 2.15 -> ~1.6
GAIN = np.array([0.94, 0.98, 1.26], dtype=np.float32)
SATURATION = 0.90
VIOLET = np.array([0.47, 0.34, 0.93], dtype=np.float32)  # --brand #7757ee, normalised
SHADOW_TINT = 0.14      # how far shadows drift toward violet
CONTRAST = 1.06         # gentle S-curve around mid
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

im = np.array(Image.open(SRC).convert("RGBA")).astype(np.float32)
rgb, alpha = im[:, :, :3] / 255.0, im[:, :, 3:4]

rgb *= GAIN

lum = (rgb * LUMA).sum(axis=2, keepdims=True)
rgb = lum + (rgb - lum) * SATURATION

# push shadows toward the frame's violet ambient; leave highlights (skin) alone
shadow = np.clip(1.0 - lum * 2.2, 0.0, 1.0) ** 1.5
rgb = rgb * (1.0 - SHADOW_TINT * shadow) + VIOLET * (SHADOW_TINT * shadow) * lum.clip(0.04, 1.0)

rgb = np.clip((rgb - 0.5) * CONTRAST + 0.5, 0.0, 1.0)

# report the corrected balance on the lit-hand patch (before the flip moves it)
p = (rgb[430:470, 1450:1650].reshape(-1, 3) * 255).mean(0)

out = np.concatenate([rgb * 255.0, alpha], axis=2)
out = np.fliplr(out)          # un-mirror the selfie: BWH logo reads correctly
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(DST)

print(f"wrote {DST} (un-mirrored)")
print(f"lit hand now R={p[0]:.1f} G={p[1]:.1f} B={p[2]:.1f}  R/B={p[0]/p[2]:.2f} (was 2.15)")
