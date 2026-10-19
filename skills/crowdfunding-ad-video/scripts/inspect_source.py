#!/usr/bin/env python3
"""Watch a source video completely before cutting.

  inspect_source.py VIDEO OUT_DIR [--model ~/.cache/adkit/fw-base]

Writes to OUT_DIR:
  proxy.mp4             640px proxy (fast to sample)
  sheet_NN.jpg          1 fps contact sheets, 30 s each, timestamps burned in   → Read every sheet
  shots.json, shots_N.jpg  shot list (scene > 0.12) + mid-frame thumbs with the 9:16 centre-crop box and
                        10 % ticks along the bottom → pick a crop centre (0–1) or "fit" per shot
  words.txt             word-level transcript (faster-whisper) → cut only at sentence ends
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get("ADKIT_INSPECT_FONT", "/System/Library/Fonts/Helvetica.ttc")

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    src, out = args[0], args[1]
    model = os.path.expanduser(args[args.index("--model") + 1]) if "--model" in args else \
        os.path.expanduser("~/.cache/adkit/fw-base")
    os.makedirs(out, exist_ok=True)
    proxy = os.path.join(out, "proxy.mp4")
    if not os.path.exists(proxy):
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=640:-2", "-c:v", "libx264", "-preset",
            "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "128k", proxy])
    info = sh(["ffmpeg", "-hide_banner", "-i", src]).stderr
    print("\n".join(l for l in info.splitlines() if "Duration" in l or "Stream" in l))

    # 1 fps contact sheets
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", proxy, "-vf",
        f"fps=1,scale=320:-2,drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=4:y=4:fontsize=18:fontcolor=yellow:"
        "box=1:boxcolor=black@0.6,tile=6x5", os.path.join(out, "sheet_%02d.jpg")])

    # shot list + crop-guide thumbs
    r = sh(["ffmpeg", "-hide_banner", "-i", proxy, "-vf", "select='gt(scene,0.12)',showinfo", "-an", "-f", "null", "-"])
    cuts = [float(t.split(":")[1]) for t in r.stderr.split() if t.startswith("pts_time:")]
    dur_s = [l for l in info.splitlines() if "Duration" in l][0].split("Duration: ")[1].split(",")[0]
    h, m, s = dur_s.split(":"); total = int(h) * 3600 + int(m) * 60 + float(s)
    c = [0.0]
    for x in cuts:
        if x - c[-1] >= 0.3:
            c.append(x)
    c.append(total)
    shots = [(c[i], c[i + 1]) for i in range(len(c) - 1)]
    json.dump(shots, open(os.path.join(out, "shots.json"), "w"))
    f = ImageFont.truetype(FONT, 20)
    thumbs = []
    for i, (a, b) in enumerate(shots):
        p = os.path.join(out, f"_s{i:03d}.jpg")
        sh(["ffmpeg", "-loglevel", "error", "-y", "-ss", str((a + b) / 2), "-i", proxy, "-frames:v", "1",
            "-vf", "scale=320:180", p])
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
        for k in range(1, 10):
            d.line([(k * 32, 170), (k * 32, 180)], fill=(255, 0, 0), width=2)
        w = 180 * 9 / 16
        d.rectangle([160 - w / 2, 0, 160 + w / 2, 179], outline=(0, 255, 255))
        d.text((3, 3), f"#{i} {a:.2f}-{b:.2f}", font=f, fill=(255, 255, 0), stroke_width=2, stroke_fill=(0, 0, 0))
        thumbs.append(im); os.remove(p)
    for n in range(0, len(thumbs), 48):
        grp = thumbs[n:n + 48]; rows = (len(grp) + 7) // 8
        o = Image.new("RGB", (8 * 320, rows * 180))
        for j, im in enumerate(grp):
            o.paste(im, ((j % 8) * 320, (j // 8) * 180))
        o.save(os.path.join(out, f"shots_{n // 48}.jpg"))
    print(f"{len(shots)} shots → shots_*.jpg ; contact sheets → sheet_*.jpg")

    # transcript
    if not os.path.exists(os.path.join(model, "model.bin")):
        print(f"[transcript skipped] no whisper model at {model} — run get_whisper_model.sh first")
        return
    wav = os.path.join(out, "audio.wav")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", proxy, "-vn", "-ac", "1", "-ar", "16000", wav])
    from faster_whisper import WhisperModel
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    segs, info = wm.transcribe(wav, word_timestamps=True, vad_filter=True)
    with open(os.path.join(out, "words.txt"), "w") as fo:
        fo.write(f"LANG {info.language}\n")
        for sgm in segs:
            fo.write(" ".join(f"{w.word.strip()}[{w.start:.2f}-{w.end:.2f}]" for w in sgm.words) + "\n")
    print("transcript → words.txt (whisper mishears brand names: fix them via the project glossary).\n"
          "Music-only sources produce hallucinated 'lyrics' (e.g. a few long words spanning 10+ s) — treat as no VO.")

if __name__ == "__main__":
    main()
