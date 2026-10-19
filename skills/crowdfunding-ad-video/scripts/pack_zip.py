#!/usr/bin/env python3
"""Zip deliverables with UTF-8 (NFC) filenames so Chinese/Japanese names survive on Windows / JP machines.
macOS `zip` and `ditto` do NOT set the UTF-8 flag (names turn into mojibake) — always pack with this.

  pack_zip.py DIR NAME            → DIR/NAME.zip containing NAME/<every .mp4 in DIR>"""
import glob, os, sys, unicodedata, zipfile

if len(sys.argv) < 3:
    sys.exit(__doc__)
d, name = sys.argv[1], sys.argv[2]
out = os.path.join(d, name + ".zip")
files = sorted(glob.glob(os.path.join(d, "*.mp4")))
with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
    for f in files:
        z.write(f, unicodedata.normalize("NFC", f"{name}/{os.path.basename(f)}"))
z = zipfile.ZipFile(out)
ok = all(i.flag_bits & 0x800 or i.filename.isascii() for i in z.infolist())
print(f"{out}: {len(files)} files, utf8-flag ok={ok}, {os.path.getsize(out) / 1e6:.0f} MB")
