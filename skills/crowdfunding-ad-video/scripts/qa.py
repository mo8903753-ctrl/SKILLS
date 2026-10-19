#!/usr/bin/env python3
"""QA finished videos.

  qa.py DIR_OR_FILES... [--sheet OUT.jpg] [--every 2.5] [--transcribe MODEL_DIR] [--open3s OUT.jpg]

  * table: duration / resolution / audio stream per file
  * --sheet     one row of frames (every N s) per video → check copy legibility, overlaps, logo, end card
  * --open3s    frames at 0 / 0.8 / 1.6 / 2.4 s per video → product visible in the first 3 s, and the t=0 frame
                (platform thumbnail) already shows every persistent overlay at full opacity
  * --transcribe re-transcribe each file → first/last words must be whole (no clipped sentences)"""
import glob, os, re, subprocess, sys, tempfile
from PIL import Image

def probe(p):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", p], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o)
    if not d:
        return 0.0, "UNREADABLE (still rendering or corrupt)", 0
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))
    wh = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", o)
    if not wh:
        return dur, "NO VIDEO", o.count("Audio:")
    return dur, f"{wh.group(1)}x{wh.group(2)}", o.count("Audio:")

def frames_row(p, times, h=360):
    ims = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(times):
            fp = os.path.join(td, f"{i}.jpg")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1",
                            "-vf", f"scale=-2:{h}", fp])
            if os.path.exists(fp):
                ims.append(Image.open(fp).convert("RGB"))
    row = Image.new("RGB", (sum(i.width for i in ims) or 1, h))
    x = 0
    for im in ims:
        row.paste(im, (x, 0)); x += im.width
    return row

def stack(rows, out):
    W = max(r.width for r in rows); o = Image.new("RGB", (W, sum(r.height for r in rows)))
    y = 0
    for r in rows:
        o.paste(r, (0, y)); y += r.height
    o.save(out); print("sheet →", out)

def main():
    a = sys.argv[1:]
    opt = {}
    for k in ("--sheet", "--every", "--transcribe", "--open3s"):
        if k in a:
            i = a.index(k); opt[k] = a[i + 1]; a = a[:i] + a[i + 2:]
    files = []
    for x in a:
        files += sorted(glob.glob(os.path.join(x, "*.mp4"))) if os.path.isdir(x) else [x]
    for f in files:
        d, wh, au = probe(f)
        print(f"{os.path.basename(f)} | {d:6.2f}s | {wh} | audio={au}")
    if "--sheet" in opt:
        ev = float(opt.get("--every", 2.5))
        stack([frames_row(f, [t * ev for t in range(int(probe(f)[0] // ev) + 1)], 240) for f in files], opt["--sheet"])
    if "--open3s" in opt:   # t=0 is the thumbnail: frame / product / offer must already be fully visible
        stack([frames_row(f, [0.0, 0.8, 1.6, 2.4], 320) for f in files], opt["--open3s"])
    if "--transcribe" in opt:
        from faster_whisper import WhisperModel
        m = WhisperModel(os.path.expanduser(opt["--transcribe"]), device="cpu", compute_type="int8")
        for f in files:
            segs, _ = m.transcribe(f, vad_filter=True)
            segs = list(segs)
            print("==", os.path.basename(f))
            for s in segs:
                print(f"  {s.start:6.2f}-{s.end:6.2f} {s.text.strip()}")

if __name__ == "__main__":
    main()
