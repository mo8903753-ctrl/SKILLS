#!/usr/bin/env python3
"""Product render on a white background → transparent cut-out (for the bottom-left product image).

  cutout.py RENDER.png OUT.png [--thresh 236] [--max 1400]

Flood-fills near-white regions connected to the border, so white/light parts inside the product survive.
Pick a 3/4 (≈45°) studio render; check the result on a dark background before using it."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

args = sys.argv[1:]
if len(args) < 2:
    sys.exit(__doc__)
th = int(args[args.index("--thresh") + 1]) if "--thresh" in args else 236
mx = int(args[args.index("--max") + 1]) if "--max" in args else 1400
im = Image.open(args[0]).convert("RGB")
im.thumbnail((mx, mx * 3 // 2), Image.LANCZOS)
a = np.asarray(im).astype(int)
lab, _ = ndimage.label(a.min(axis=2) > th)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
alpha = (~np.isin(lab, list(border))).astype(np.uint8) * 255
alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
out = Image.fromarray(np.dstack([np.asarray(im), alpha]).astype(np.uint8), "RGBA")
out = out.crop(out.getbbox())
out.save(args[1])
print("saved", args[1], out.size)
