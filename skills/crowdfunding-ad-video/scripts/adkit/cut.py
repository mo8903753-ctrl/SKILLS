"""Cut a TVC into frame-accurate 9:16 pieces (per-shot crop centre or blurred 'fit') + stitched audio.

Segment syntax in project.json (source seconds):
  [a, b]                                   plain range
  {"audio": [a, b], "video": [[s, e], ...]} keep the VO/music of [a, b] but lay other footage under it
                                           (used to open on a product shot or replace off-brief shots)
  "@name"                                  a named tail from tvc.tails (e.g. "@logo")
Video durations of an override must equal the audio duration after snapping to the frame grid."""
import hashlib, os, subprocess, sys
from . import proj_path

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


class Cutter:
    def __init__(self, cfg):
        t = cfg["tvc"]
        self.src = proj_path(cfg, t["source"])
        self.fps = t.get("fps", 25)
        self.sw, self.sh = t["src_size"]
        self.cw = round(self.sh * 9 / 16)
        self.vframe = [(float(a), m) for a, m in t["vframe"]]
        self.tails = t.get("tails", {})
        self.cache = proj_path(cfg, cfg.get("cache_dir", "work/pieces")); os.makedirs(self.cache, exist_ok=True)

    def frames(self, x):
        return round(x * self.fps) / self.fps

    def seg(self, s):
        if isinstance(s, str) and s.startswith("@"):
            return tuple(self.tails[s[1:]])
        return s

    def split(self, s):
        s = self.seg(s)
        if isinstance(s, dict):
            va = sum(self.frames(e) - self.frames(a) for a, e in s["video"])
            au = self.frames(s["audio"][1]) - self.frames(s["audio"][0])
            if abs(va - au) > 0.02:
                sys.exit(f"override length mismatch: video {va:.2f}s vs audio {au:.2f}s in {s}")
            return tuple(s["audio"]), [tuple(v) for v in s["video"]]
        return tuple(s), [tuple(s)]

    def duration(self, segs):
        return sum(self.frames(b) - self.frames(a) for a, b in (self.split(s)[0] for s in segs))

    def vframe_pieces(self, a, b):
        bounds = [t for t, _ in self.vframe]
        out = []
        for i, (t, mode) in enumerate(self.vframe):
            nt = bounds[i + 1] if i + 1 < len(bounds) else 1e9
            s, e = max(a, t), min(b, nt)
            if e - s > 0.001:
                out.append((s, e, mode))
        return out

    def vf(self, mode):
        if mode == "fit":
            return ("split[a][b];[a]scale=-2:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];"
                    "[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
        x = int(min(max(mode * self.sw - self.cw / 2, 0), self.sw - self.cw))
        return f"crop={self.cw}:{self.sh}:{x}:0,scale=1080:1920:flags=lanczos"

    def piece(self, s, e, mode):
        s, e = self.frames(s), self.frames(e)
        key = hashlib.md5(f"{self.src}{s}{e}{mode}".encode()).hexdigest()[:12]
        p = os.path.join(self.cache, f"v_{key}.mp4")
        if not os.path.exists(p):
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s:.3f}", "-i", self.src, "-t", f"{e - s:.3f}", "-an",
                 "-filter_complex", self.vf(mode), "-r", str(self.fps), "-c:v", "libx264", "-preset", "medium",
                 "-crf", "14", "-pix_fmt", "yuv420p", p])
        return p

    def video_list(self, name, segs):
        pieces = []
        for s in segs:
            for a, b in self.split(s)[1]:
                pieces += [self.piece(x, y, m) for x, y, m in self.vframe_pieces(a, b)]
        lst = os.path.join(self.cache, f"{name}.txt")
        with open(lst, "w") as f:
            f.writelines(f"file '{p}'\n" for p in pieces)
        return lst

    def audio(self, name, segs):
        """Concatenate the segments' audio with short fades at every join (VO+music are usually one mix)."""
        rngs = [self.split(s)[0] for s in segs]
        p = os.path.join(self.cache, f"{name}.wav")
        inputs, chains = [], []
        for i, (a, b) in enumerate(rngs):
            a, b = self.frames(a), self.frames(b); d = b - a
            fo = 0.6 if i == len(rngs) - 1 else 0.18
            inputs += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", self.src]
            chains.append(f"[{i}:a]afade=t=in:d={0.0 if i == 0 else 0.06},afade=t=out:st={d - fo:.3f}:d={fo}[a{i}]")
        graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(rngs))) + \
            f"concat=n={len(rngs)}:v=0:a=1[o]"
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[o]", "-ar", "48000", p])
        return p
