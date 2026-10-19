import os, sys, json
from multiprocessing import Pool
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
SRC = os.environ.get("KS_RAW", "./raw")
OUT = os.environ.get("KS_THUMBS", "./work/thumbs")
DIRS = sorted(d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)) and not d.startswith("."))  # every sub-folder of the raw folder

def job(a):
    d, f = a
    src = os.path.join(SRC, d, f)
    stem = f.replace(" ", "_")
    dst = os.path.join(OUT, d, os.path.splitext(stem)[0] + ("_" + stem.rsplit("_",1)[1] if ".png_" in f else "") + ".jpg")
    if os.path.exists(dst):
        return None
    try:
        im = Image.open(src)
        w, h = im.size
        if im.format == "JPEG":
            im.draft("RGB", (1400, 1400))
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        im.thumbnail((1200, 1200), Image.LANCZOS)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im.save(dst, quality=84)
        return (d, f, w, h, os.path.getsize(src))
    except Exception as e:
        return (d, f, "ERR", str(e), 0)

if __name__ == "__main__":
    jobs = []
    for d in DIRS:
        for f in sorted(os.listdir(os.path.join(SRC, d))):
            if f.startswith("._") or f == ".DS_Store":
                continue
            jobs.append((d, f))
    # root-level loose files not in 键盘图已修
    with Pool(8) as p:
        res = [r for r in p.imap_unordered(job, jobs, chunksize=4) if r]
    json.dump(res, open(os.path.join(OUT, "meta.json"), "w"), ensure_ascii=False)
    print("done", len(jobs), "new", len(res), "errors", [r for r in res if r[2] == "ERR"])
