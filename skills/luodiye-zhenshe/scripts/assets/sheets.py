import os
from PIL import Image, ImageDraw, ImageFont
T = os.environ.get("KS_THUMBS", "./work/thumbs")
O = os.environ.get("KS_SHEETS", "./work/sheets")
COLS, ROWS, CW, CH, LB = 7, 6, 288, 196, 20
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
os.makedirs(O, exist_ok=True)
tags = {d: "F%02d" % i for i, d in enumerate(sorted(x for x in os.listdir(T) if os.path.isdir(os.path.join(T, x))))}  # one prefix per folder
for d, tag in tags.items():
    fs = sorted(f for f in os.listdir(os.path.join(T, d)) if f.endswith(".jpg") and not f.startswith("._"))
    per = COLS * ROWS
    for i in range(0, len(fs), per):
        chunk = fs[i:i + per]
        rows = (len(chunk) + COLS - 1) // COLS
        sh = Image.new("RGB", (COLS * CW, rows * (CH + LB)), (24, 24, 24))
        dr = ImageDraw.Draw(sh)
        for k, f in enumerate(chunk):
            im = Image.open(os.path.join(T, d, f)); im.thumbnail((CW - 4, CH - 2))
            x = (k % COLS) * CW; y = (k // COLS) * (CH + LB)
            sh.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
            dr.text((x + 6, y + CH + 1), f[:-4], fill=(255, 220, 90), font=font)
        name = f"{tag}_{i // per + 1:02d}.jpg"
        sh.save(os.path.join(O, name), quality=80)
        print(name, chunk[0][:-4], "→", chunk[-1][:-4])
