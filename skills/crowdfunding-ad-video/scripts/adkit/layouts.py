"""Overlay layouts. Each function writes one transparent PNG and returns its path.

Styles (see references/layouts.md for when to use which):
  grey_*      full-bleed 9:16 crop of a TVC + grey film grade, Mincho copy cards, badge, offer tag, end CTA
  frame_*     KS-"Live Now"-style bottom band: brand logo top-left, product cut-out bottom-left,
              「line1 / [platform logo] line2」 band, discount ticket above the band
  band_v_*    client-made 9:16 videos = 16:9 picture on blurred bands (picture ≈ y 637–1245 of 1920):
              offer always in the upper band, copy in the lower band, product bottom-left
  band_h_*    16:9 versions of the same: copy top-left (or right), offer tag top-right, product bottom-left
"""
from PIL import Image, ImageDraw

V, H = (1080, 1920), (1920, 1080)

def _new(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))

# ---------------- grey (TVC, full-bleed 9:16) ----------------
def grey_card(k, path, head=None, sub=None, badge=False, offer=False, cta=False, head_size=62, y=1220):
    b = _new(V)
    if offer:
        k.offer_tag(b, 540, 760)
    if head:
        yy = k.glow_text(b, head.split("\n"), k.font("serif", head_size), 0, y, alpha=150)
        if sub:
            yy = k.glow_text(b, sub.split("\n"), k.font("serif", 32), 0, yy + 18, gap=1.45, blur=6, alpha=170)
        if badge:
            k.badge(b, 0, yy + 50)
    elif badge:
        k.badge(b, 0, y)
    if cta:
        k.cta_bar(b, 1530)
        k.glow_text(b, [k.offer["cta_sub"]], k.font("bold", 36), 0, 1610, blur=6)
    b.save(path); return path

def grey_end(k, path):
    return grey_card(k, path, badge=True, cta=True, y=1740)

# ---------------- frame (bottom band) ----------------
def frame(k, path, band_h=250):
    W, Hh = V
    b = _new(V)
    grad = Image.new("L", (1, 300))
    for y in range(300):
        grad.putpixel((0, y), int(110 * (1 - y / 300) ** 1.6))
    top = Image.new("RGBA", (W, 300), (0, 0, 0, 255)); top.putalpha(grad.resize((W, 300)))
    b.alpha_composite(top)
    lg = k.brand_logo_white(250)
    sh = _new(V); sh.paste((0, 0, 0, 170), (54, 74), lg.getchannel("A"))
    from PIL import ImageFilter
    b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); b.alpha_composite(lg, (50, 70))
    d = ImageDraw.Draw(b); y0 = Hh - band_h
    d.rectangle((0, y0, W, Hh), fill=k.colors["band"] + (255,))
    # 2 lines: 「line1」 / [official logo on white pill] line2 — never break the logo line into a 3rd line
    xr = 430
    d.text((xr, y0 + 40), k.platform["band_line1"], font=k.font("bold", 46), fill=(255, 255, 255, 255))
    pl = k.platform_logo(60)
    py0 = y0 + 112
    pill = (xr - 2, py0, xr + pl.width + 30, py0 + 86)
    d.rounded_rectangle(pill, 43, fill=(255, 255, 255, 255))
    b.alpha_composite(pl, (xr + 14, py0 + 13))
    f3 = k.font("bold", 46)
    d.text((pill[2] + 16, py0 + 43 - f3.getmetrics()[0] * 0.55), k.platform["band_line2"], font=f3,
           fill=k.colors["band_accent"] + (255,))
    pc = k.product(470); px, py = 40, Hh - 470 - 18
    psh = _new(V); psh.paste((0, 0, 0, 140), (px + 10, py + 14), pc.getchannel("A"))
    b.alpha_composite(psh.filter(ImageFilter.GaussianBlur(14))); b.alpha_composite(pc, (px, py))
    tk = k.ticket(); b.alpha_composite(tk, (W - tk.width - 30, y0 - tk.height - 24))
    b.save(path); return path

def frame_card_tvc(k, path, head=None, sub=None, y=1000):
    """Copy for the frame style over a full-bleed TVC crop (band/ticket already carry the offer)."""
    return grey_card(k, path, head, sub, y=y)

def frame_end_tvc(k, path):
    return grey_card(k, path, "\n".join(k.offer["cta_sub_lines"]), head_size=56, y=1080)

def frame_card_band(k, path, head=None, sub=None, end=False):
    """Copy for the frame style over a blurred-band client video: upper band (y≈260–600) with a soft wash."""
    b = _new(V)
    if head or end:
        k.wash(b, (0, 250, 1080, 600))
    if end:
        k.glow_text(b, k.offer["cta_sub_lines"], k.font("serif", 58), 0, 330)
    if head:
        yy = k.glow_text(b, head.split("\n"), k.font("serif", 62), 0, 300)
        if sub:
            k.glow_text(b, sub.split("\n"), k.font("serif", 32), 0, yy + 14, gap=1.45, blur=6, alpha=170)
    b.save(path); return path

# ---------------- blurred-band client videos, 9:16 ----------------
def _top(k, b):
    k.wash(b, (0, 120, 1080, 560), alpha=80)
    k.badge(b, 0, 215, size=44)

def band_v_static(k, path):
    b = _new(V); k.paste_product(b, 36, 1890, 360); b.save(path); return path

def band_v_top_offer(k, path):
    """Upper band is never empty: badge + offer for the whole video (until the end card)."""
    b = _new(V); _top(k, b)
    k.offer_tag(b, 540, 405, size=48, lines=k.offer["top_tag_lines"])
    b.save(path); return path

def band_v_top_title(k, path, with_logo=True):
    """During the end card the CTA bar already shows the discount → swap the top offer for the product title
    (never the same discount twice in one frame). Skip the brand logo if the footage already shows it."""
    b = _new(V); _top(k, b)
    k.glow_text(b, [k.brand["title"]], k.font("serif", 60), 0, 315)
    if with_logo:
        lg = k.brand_logo_white(300)
        b.alpha_composite(lg, ((1080 - lg.width) // 2, 425))
    b.save(path); return path

def band_v_card(k, path, head, sub=None):
    b = _new(V)
    yy = k.glow_text(b, head.split("\n"), k.font("serif", 60), 0, 1295)
    if sub:
        k.glow_text(b, sub.split("\n"), k.font("serif", 32), 0, yy + 12, gap=1.45, blur=6, alpha=170)
    b.save(path); return path

def band_v_end(k, path):
    b = _new(V)
    k.cta_bar(b, 1340)
    k.glow_text(b, [k.offer["cta_sub"]], k.font("bold", 38), 0, 1430, blur=6)
    b.save(path); return path

# ---------------- blurred-band client videos, 16:9 ----------------
def band_h_static(k, path, px=30, ph=300):
    b = _new(H)
    k.offer_tag(b, 1560, 130, size=34)
    k.paste_product(b, px, 1065, ph)
    b.save(path); return path

def band_h_card(k, path, head, sub=None, side="left", top=70):
    b = _new(H)
    cx0 = 0 if side == "left" else 1920 - 1100
    k.wash(b, (cx0, top - 70, cx0 + 1100, top + 260), alpha=120, blur=90)
    x = 90 if side == "left" else 1830
    yy = k.glow_text(b, head.split("\n"), k.font("serif", 58), x, top, align=side)
    if sub:
        k.glow_text(b, sub.split("\n"), k.font("serif", 30), x, yy + 12, align=side, gap=1.45, blur=6, alpha=170)
    b.save(path); return path

def band_h_end(k, path, bar_y=840, bar_x=340, text_above=False):
    """CTA bar starts right of the product cut-out (bar_x) so it never covers it or a burned-in label."""
    b = _new(H)
    bw = 1920 - bar_x
    bar = Image.new("RGBA", (bw, 120), (0, 0, 0, 0)); k.cta_bar(bar, 60, bh=120)
    b.alpha_composite(bar, (bar_x, bar_y))
    t = Image.new("RGBA", (bw, 80), (0, 0, 0, 0))
    k.glow_text(t, [k.offer["cta_sub"]], k.font("bold", 34), 0, 10, blur=6)
    b.alpha_composite(t, (bar_x, bar_y - 62 if text_above else bar_y + 128))
    b.save(path); return path
