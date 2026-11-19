#!/usr/bin/env python3
"""
Sweetmyo Gen2 — v4 "Signal" redesign asset pipeline.
Sources:
  _source/official/   (fresh pull from sweetmyo.com/gen2-kickstarter + product page, 2026-11-18)
  assets/             (previously approved exports reused as-is: hero montage, motion trio, couch, banners)
Outputs: assets/v4/*
Run: arch -arm64 python3 scripts/process_assets_v4.py
"""
import os, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source", "official")
VID = os.path.join(SRC, "videos")
IMG = os.path.join(SRC, "images")
OUT = os.path.join(ROOT, "assets", "v4")
os.makedirs(OUT, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
BRAND_FILM = os.path.join(VID, "3b6edd6d4c4b75b2442738e91789bbc3.mp4")


def ff(args, label):
    cmd = [FF, "-y", "-loglevel", "error"] + args
    subprocess.run(cmd, check=True)
    out = args[-1]
    print(f"  [{label}] {os.path.relpath(out, ROOT)} {os.path.getsize(out)/1024:.0f} KB")


def x264(crf=26, gop=None, extra=None):
    a = ["-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if gop:
        a += ["-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0"]
    return a + (extra or [])


def poster(video, t, out, w=None):
    vf = f"scale={w}:-2" if w else "null"
    ff(["-ss", str(t), "-i", video, "-frames:v", "1", "-vf", vf, "-c:v", "libwebp", "-quality", "82", out], "POSTER")


print("1) Zones body scrub (679e72: lime body, zones light up in sequence) — scrub-friendly GOP 2")
zones_src = os.path.join(VID, "679e72bde9d641669ac9bd6fb5ea64b1.mp4")
ff(["-ss", "0.15", "-t", "1.95", "-i", zones_src,
    "-vf", "crop=720:1360:920:40,scale=540:1020:flags=lanczos,fps=30",
    *x264(crf=24, gop=2), os.path.join(OUT, "zones-body.mp4")], "MP4")
poster(os.path.join(OUT, "zones-body.mp4"), 0.0, os.path.join(OUT, "zones-body.webp"))

print("2) Scan chapter (brand film 51.0–55.0s glass body-composition cards on lime)")
ff(["-ss", "51.05", "-t", "3.9", "-i", BRAND_FILM,
    "-vf", "scale=1600:900:flags=lanczos,fps=30",
    *x264(crf=25), os.path.join(OUT, "scan-glass.mp4")], "MP4")
poster(os.path.join(OUT, "scan-glass.mp4"), 1.9, os.path.join(OUT, "scan-glass.webp"))

print("3) Smart Hub snap & lock (2cf83, HD square)")
hub_src = os.path.join(VID, "2cf83adb4a504be7966c48e79915441d.mp4")
ff(["-i", hub_src, "-vf", "crop=1440:1440:560:0,scale=960:960:flags=lanczos,fps=30",
    *x264(crf=24), os.path.join(OUT, "hub-lock.mp4")], "MP4")
poster(os.path.join(OUT, "hub-lock.mp4"), 3.3, os.path.join(OUT, "hub-lock.webp"))
poster(hub_src, 0.05, os.path.join(OUT, "hub-float.webp"), w=1400)

print("4) Two-piece fit (brand film 10.4–13.4s, studio, 4:5) — lime-hub colourway only")
for f in ("put-on.mp4", "put-on.webp"):
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        os.remove(p)
ff(["-ss", "11.12", "-i", BRAND_FILM, "-frames:v", "1",
    "-vf", "crop=864:1080:528:0,scale=1080:1350:flags=lanczos", "-c:v", "libwebp", "-quality", "86",
    os.path.join(OUT, "fit-two-piece.webp")], "WEBP")
for f in ("fit-two-piece.mp4",):
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        os.remove(p)

print("5) Official app screenshots (gen2-kickstarter/APP)")
for slug, fn in [("mode", "site_gen2-kickstarter_46eac.png"), ("zone", "site_gen2-kickstarter_47a85.png"),
                 ("summary", "site_gen2-kickstarter_4c0c6.png"), ("trends", "site_gen2-kickstarter_6b89f.png")]:
    im = Image.open(os.path.join(IMG, fn)).convert("RGB")
    im = im.resize((620, int(620 * im.height / im.width)), Image.Resampling.LANCZOS)
    dest = os.path.join(OUT, f"app-{slug}.webp")
    im.save(dest, "WEBP", quality=86, method=6)
    print(f"  [WEBP] {os.path.relpath(dest, ROOT)} {im.size}")

print("6) Pre-rendered volt glow (no runtime blur)")
S = 900
yy, xx = np.mgrid[0:S, 0:S]
r = np.sqrt((xx - S / 2) ** 2 + (yy - S / 2) ** 2) / (S / 2)
a = np.clip(1 - r, 0, 1) ** 2.2
rgba = np.zeros((S, S, 4), np.uint8)
rgba[..., 0], rgba[..., 1], rgba[..., 2] = 206, 245, 52
rgba[..., 3] = (a * 255).astype(np.uint8)
Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, "glow-volt.png"), optimize=True)
print("  [PNG] assets/v4/glow-volt.png")

print("7) Tote (first 100 backers perk)")
im = Image.open(os.path.join(IMG, "site_gen2-kickstarter_sweetmyo-tote.jpg")).convert("RGB")
im.thumbnail((720, 960))
im.save(os.path.join(OUT, "tote.webp"), "WEBP", quality=84, method=6)
print("  [WEBP] assets/v4/tote.webp", im.size)
print("done")
