#!/usr/bin/env python3
"""Render ad videos from project.json.

  render.py PROJECT.json tvc     [--style grey|frame] [EDIT ...]   cut the TVC into 9:16 edits + overlays
  render.py PROJECT.json overlay [--style band|frame] [JOB ...]    overlays only, on client-finished videos
  render.py PROJECT.json stills  [EDIT|JOB ...]                    write the overlay PNGs only (for mock-ups)

No args after the mode = everything in that section. Outputs go to project.out_dir with the naming prefixes
from project.naming; durations are appended (e.g. A_灰调_02_VoiceCoach_9x16_23s.mp4)."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adkit import load_project, proj_path
from adkit.draw import Kit
from adkit.cut import Cutter, run
from adkit import layouts as L

FADE = 0.35
DEFAULT_GRADE = ("eq=saturation=0.5:contrast=0.85:brightness=0.04:gamma=1.05,"
                 "curves=all='0/0.09 0.5/0.54 1/0.93',colorbalance=rs=0.02:gs=0.005:bs=0.012")


def video_size(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", out)
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    return int(m.group(1)), int(m.group(2)), int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))


def compose(base_inputs, base_vf, ovs, dur, out, audio_map, audio_codec, scale=None, rate=None):
    n0 = sum(1 for x in base_inputs if x == "-i")
    inputs = list(base_inputs)
    graph = [f"[0:v]{base_vf},format=yuv420p[v0]"]
    for i, (a, b, png) in enumerate(ovs):
        inputs += ["-loop", "1", "-t", f"{dur:.2f}", "-i", png]
        fo = b - FADE if b < dur - 0.05 else dur + 1
        sc = f"scale={scale}:flags=lanczos," if scale else ""
        # elements present from t=0 get no fade-in: the first frame is the platforms' thumbnail
        fin = f"fade=t=in:st={a:.2f}:d={FADE}:alpha=1," if a > 0 else ""
        graph.append(f"[{n0 + i}:v]{sc}format=rgba,{fin}fade=t=out:st={fo:.2f}:d={FADE}:alpha=1[o{i}]")
        graph.append(f"[v{i}][o{i}]overlay=shortest=1:enable='between(t,{a:.2f},{b:.2f})'[v{i + 1}]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(graph),
           "-map", f"[v{len(ovs)}]", "-map", audio_map, "-t", f"{dur:.2f}"]
    if rate:
        cmd += ["-r", str(rate)]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", *audio_codec,
            "-movflags", "+faststart", out]
    run(cmd)
    print("done", os.path.basename(out), flush=True)


def card_t(c):
    return float(c["t"][0]), float(c["t"][1])


# ---------------------------------------------------------------- TVC → 9:16 edits
def render_tvc(cfg, k, names, styles, stills_only=False):
    cut = Cutter(cfg)
    cards_dir = proj_path(cfg, cfg.get("cards_dir", "work/cards")); os.makedirs(cards_dir, exist_ok=True)
    out_dir = proj_path(cfg, cfg["out_dir"]); os.makedirs(out_dir, exist_ok=True)
    naming = cfg.get("naming", {})
    for ed in cfg["tvc"]["edits"]:
        if names and ed["name"] not in names:
            continue
        segs = ed["segs"]
        dur = cut.duration(segs)
        tail = cut.duration([segs[-1]])
        end_a = dur - tail + 0.1
        for style in ed.get("styles", ["grey"]):
            if styles and style not in styles:
                continue
            ov = []
            base = os.path.join(cards_dir, f"{style}_{ed['name']}")
            if style == "grey":
                for i, c in enumerate(ed["cards"]):
                    a, b = card_t(c)
                    ov.append((a, b, L.grey_card(k, f"{base}_{i}.png", c.get("head"), c.get("sub"), c.get("badge", False),
                                                 c.get("offer", False), y=c.get("y", 1220))))
                ov.append((end_a, dur, L.grey_end(k, f"{base}_end.png")))
                vf = cfg.get("grade", DEFAULT_GRADE)
            else:
                for i, c in enumerate(ed["cards"]):
                    a, b = card_t(c)
                    ov.append((a, b, L.frame_card_tvc(k, f"{base}_{i}.png", c.get("head"), c.get("sub"))))
                ov.append((end_a, dur, L.frame_end_tvc(k, f"{base}_end.png")))
                ov.append((0, dur + 1, L.frame(k, os.path.join(cards_dir, "frame.png"))))
                vf = "null"
            if stills_only:
                print("stills", base, flush=True); continue
            lst = cut.video_list(ed["name"], segs)
            wav = cut.audio(ed["name"], segs)
            out = os.path.join(out_dir, f"{naming.get(style, style + '_')}{ed['name']}_9x16_{round(dur)}s.mp4")
            compose(["-f", "concat", "-safe", "0", "-i", lst, "-i", wav], vf, ov, dur, out, "1:a",
                    ["-c:a", "aac", "-b:a", "192k"], rate=cut.fps)


# ---------------------------------------------------------------- overlays on client-finished videos
def render_overlay(cfg, k, names, styles, stills_only=False):
    cards_dir = proj_path(cfg, cfg.get("cards_dir", "work/cards")); os.makedirs(cards_dir, exist_ok=True)
    out_dir = proj_path(cfg, cfg["out_dir"]); os.makedirs(out_dir, exist_ok=True)
    naming = cfg.get("naming", {})
    for job in cfg.get("overlay_jobs", []):
        if names and job["name"] not in names:
            continue
        src = proj_path(cfg, job["source"])
        w, h, dur = video_size(src)
        vert = h > w
        ratio = "9x16" if vert else "16x9"
        end = float(job["end"])
        for style in job.get("styles", ["band"]):
            if styles and style not in styles:
                continue
            if style == "frame" and not vert:
                continue
            base = os.path.join(cards_dir, f"{style}_{job['name']}_{ratio}")
            ov = []
            if style == "band" and vert:
                for i, c in enumerate(job["cards"]):
                    a, b = card_t(c)
                    ov.append((a, min(b, end - 0.05), L.band_v_card(k, f"{base}_{i}.png", c["head"], c.get("sub"))))
                ov.append((end, dur + 1, L.band_v_end(k, f"{base}_end.png")))
                ov.append((0, dur + 1, L.band_v_static(k, f"{base}_static.png")))
                ov.append((0, end, L.band_v_top_offer(k, f"{base}_top_offer.png")))
                ov.append((end, dur + 1, L.band_v_top_title(k, f"{base}_top_title.png",
                                                            with_logo=job.get("end_title_logo", True))))
            elif style == "band":
                o = job.get("h_opts", {})
                for i, c in enumerate(job["cards"]):
                    a, b = card_t(c)
                    side = c.get("side", "left")
                    ov.append((a, min(b, end - 0.05), L.band_h_card(k, f"{base}_{i}.png", c["head"], c.get("sub"),
                                                                    side=side, top=250 if side == "right" else 70)))
                ov.append((end, dur + 1, L.band_h_end(k, f"{base}_end.png", o.get("bar_y", 840), o.get("bar_x", 340),
                                                      o.get("text_above", False))))
                ov.append((0, dur + 1, L.band_h_static(k, f"{base}_static.png", o.get("px", 30), o.get("ph", 300))))
            else:  # frame over a blurred-band 9:16 client video
                for i, c in enumerate(job["cards"]):
                    a, b = card_t(c)
                    ov.append((a, b, L.frame_card_band(k, f"{base}_{i}.png", c["head"], c.get("sub"))))
                ov.append((end, dur + 1, L.frame_card_band(k, f"{base}_end.png", end=True)))
                ov.append((0, dur + 1, L.frame(k, os.path.join(cards_dir, "frame.png"))))
            if stills_only:
                print("stills", base, flush=True); continue
            prefix = naming.get("overlay_frame" if style == "frame" else "overlay", "")
            out = os.path.join(out_dir, f"{prefix}{job['name']}_{ratio}_{round(dur)}s.mp4")
            compose(["-i", src], "null", ov, dur, out, "0:a", ["-c:a", "copy"], scale=f"{w}:{h}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cfg = load_project(sys.argv[1]); mode = sys.argv[2]; rest = sys.argv[3:]
    styles = []
    if "--style" in rest:
        i = rest.index("--style"); styles = [rest[i + 1]]; rest = rest[:i] + rest[i + 2:]
    k = Kit(cfg)
    if mode == "tvc":
        render_tvc(cfg, k, rest, styles)
    elif mode == "overlay":
        render_overlay(cfg, k, rest, styles)
    elif mode == "stills":
        if cfg.get("tvc"):
            render_tvc(cfg, k, rest, styles, stills_only=True)
        render_overlay(cfg, k, rest, styles, stills_only=True)
    else:
        sys.exit(__doc__)
