"""Drawing primitives. All layouts are drawn on 1080x1920 (9:16) or 1920x1080 (16:9) RGBA canvases and scaled
to the video size at render time. Every element reads its wording from project.json — nothing is hard-coded
here, so copy can always be traced to the pre-launch / campaign sources."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from . import proj_path

import glob as _glob
_PINGFANG = (_glob.glob("/System/Library/AssetsV2/com_apple_MobileAsset_Font*/*/AssetData/PingFang.ttc")
             or ["/System/Library/Fonts/PingFang.ttc"])[0]
_AVENIR = "/System/Library/Fonts/Avenir Next.ttc"   # 0 Bold, 2 Demi Bold, 5 Medium, 7 Regular
# Font presets per copy language (project.json "lang"); any key can be overridden with project.json "fonts".
#   serif   = headline / copy cards     bold = tags, CTA     regular = badge text, notes     number = big discount digits
LANG_FONTS = {
    "ja": {"serif": ["/System/Library/Fonts/ヒラギノ明朝 ProN.ttc", 0], "bold": ["/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 0],
           "regular": ["/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", 0], "number": [_AVENIR, 2], "heavy": [_AVENIR, 9]},
    "en": {"serif": ["/System/Library/Fonts/NewYork.ttf", 0], "bold": [_AVENIR, 0],
           "regular": [_AVENIR, 5], "number": [_AVENIR, 2], "heavy": [_AVENIR, 9]},
    "zh-Hant": {"serif": ["/System/Library/Fonts/Supplemental/Songti.ttc", 7], "bold": [_PINGFANG, 10],
                "regular": [_PINGFANG, 2], "number": [_AVENIR, 2], "heavy": [_AVENIR, 9]},
    "zh-Hans": {"serif": ["/System/Library/Fonts/Supplemental/Songti.ttc", 6], "bold": [_PINGFANG, 11],
                "regular": [_PINGFANG, 3], "number": [_AVENIR, 2], "heavy": [_AVENIR, 9]},
}
DEFAULT_FONTS = LANG_FONTS["ja"]
DEFAULT_COLORS = {"offer": [243, 112, 33], "cta": [24, 70, 52], "accent": [255, 196, 0],
                  "cta_number": [255, 140, 40], "band": [16, 42, 84], "band_accent": [255, 214, 0]}


class Kit:
    def __init__(self, cfg):
        self.cfg = cfg
        self.fonts = {**LANG_FONTS[cfg.get("lang", "ja")], **cfg.get("fonts", {})}
        self.colors = {k: tuple(v) for k, v in {**DEFAULT_COLORS, **cfg.get("colors", {})}.items()}
        self.offer = cfg["offer"]
        self.platform = cfg["platform"]
        self.brand = cfg["brand"]
        self._cache = {}

    # ---------- assets ----------
    def font(self, key, size):
        path, idx = self.fonts[key]
        return ImageFont.truetype(path, size, index=idx)

    def _img(self, key, path):
        if key not in self._cache:
            self._cache[key] = Image.open(proj_path(self.cfg, path)).convert("RGBA")
        return self._cache[key]

    def platform_logo(self, h):
        """Official platform logo (icon + wordmark), e.g. rasterised from the site's own SVG. Never redraw it."""
        im = self._img("plogo", self.platform["logo_png"])
        return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

    def brand_logo_white(self, width):
        im = self._img("blogo", self.brand["logo_png"])
        w = Image.new("RGBA", im.size, (255, 255, 255, 255))
        w.putalpha(im.getchannel("A"))
        return w.resize((width, int(im.height * width / im.width)), Image.LANCZOS)

    def product(self, h):
        im = self._img("product", self.brand["product_cutout"])
        return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

    def paste_product(self, b, x, bottom, h, shadow=150):
        pc = self.product(h)
        y = bottom - h
        sh = Image.new("RGBA", b.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, shadow), (x + 8, y + 12), pc.getchannel("A"))
        b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
        b.alpha_composite(pc, (x, y))

    # ---------- text ----------
    def glow_text(self, base, lines, f, x, y, align="center", gap=1.32, blur=10, alpha=160,
                  fill=(255, 255, 255, 255)):
        """White text with a soft dark glow; align center | left (x = left edge) | right (x = right edge)."""
        W = base.width
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); tx = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ds, dt = ImageDraw.Draw(sh), ImageDraw.Draw(tx)
        yy = y
        for ln in lines:
            w = dt.textlength(ln, font=f)
            xx = (W - w) / 2 if align == "center" else (x - w if align == "right" else x)
            ds.text((xx, yy + 2), ln, font=f, fill=(0, 0, 0, alpha))
            dt.text((xx, yy), ln, font=f, fill=fill)
            yy += f.size * gap
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
        base.alpha_composite(tx)
        return yy

    def wash(self, base, box, alpha=95, blur=70):
        """Soft dark rectangle behind thin copy so it stays readable on bright skies / ceilings."""
        w = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(w).rectangle(box, fill=(0, 0, 0, alpha))
        base.alpha_composite(w.filter(ImageFilter.GaussianBlur(blur)))

    # ---------- campaign elements ----------
    def badge(self, base, x, cy, align="center", size=40):
        """White strip: 「<pre> [official platform logo] <post>」 e.g. まもなく [Makuake] にて登場."""
        pre, post = self.platform.get("badge_pre", ""), self.platform.get("badge_post", "")
        f = self.font("regular", size); dr = ImageDraw.Draw(base)
        lg = self.platform_logo(int(size * 1.05))
        pad, gap = 18, 10
        w_pre, w_post = dr.textlength(pre, font=f), dr.textlength(post, font=f)
        bw = pad + w_pre + (gap if pre else 0) + lg.width + (gap if post else 0) + w_post + pad
        bh = int(size * 1.6)
        x0 = (base.width - bw) / 2 if align == "center" else (x - bw if align == "right" else x)
        y0 = cy - bh / 2
        box = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(box).rectangle((x0, y0, x0 + bw, y0 + bh), fill=(255, 255, 255, 240))
        base.alpha_composite(box)
        xx = x0 + pad
        if pre:
            dr.text((xx, cy - size * 0.62), pre, font=f, fill=(50, 50, 50, 255)); xx += w_pre + gap
        base.alpha_composite(lg, (int(xx), int(cy - lg.height / 2))); xx += lg.width + gap
        if post:
            dr.text((xx, cy - size * 0.62), post, font=f, fill=(50, 50, 50, 255))
        return y0 + bh

    def offer_tag(self, base, cx, cy, size=38, lines=None):
        """Solid orange block, centred lines (default = offer.tag_lines)."""
        lines = lines or self.offer["tag_lines"]
        dr = ImageDraw.Draw(base)
        while True:   # shrink long (e.g. English) lines until the block fits the canvas
            f = self.font("bold", size)
            ws = [dr.textlength(l, font=f) for l in lines]
            if max(ws) + 60 <= base.width - 40 or size <= 20:
                break
            size -= 2
        bw, lh = max(ws) + 60, size * 1.32
        bh = lh * len(lines) + 34
        x0, y0 = cx - bw / 2, cy - bh / 2
        dr.rectangle((x0, y0, x0 + bw, y0 + bh), fill=self.colors["offer"] + (255,))
        for i, l in enumerate(lines):
            dr.text((cx - ws[i] / 2, y0 + 17 + i * lh), l, font=f, fill=(255, 255, 255, 255))
        return y0 + bh

    def cta_bar(self, base, cy, bh=128):
        """Full-width dark-green bar: pre + big number + pct + post + double chevron, pixel accent top-left."""
        c = self.offer["cta"]
        W = base.width; dr = ImageDraw.Draw(base); y0 = cy - bh / 2
        dr.rectangle((0, y0, W, y0 + bh), fill=self.colors["cta"] + (255,))
        for dx, dy, col in [(0, 0, self.colors["accent"]), (22, 0, self.colors["offer"]), (0, 22, self.colors["offer"])]:
            dr.rectangle((dx, y0 + dy, dx + 20, y0 + dy + 20), fill=col + (255,))
        num = self.colors["cta_number"]
        k = 1.0
        while True:   # shrink until pre + number + pct + post + chevrons fit the bar
            parts = [(c["pre"], self.font("bold", int(40 * k)), (255, 255, 255)),
                     (c["number"], self.font("number", int(104 * k)), num),
                     (c.get("pct", "%"), self.font("bold", int(62 * k)), num),
                     (c["post"], self.font("bold", int(52 * k)), (255, 255, 255))]
            parts = [p for p in parts if p[0]]
            ws = [dr.textlength(t, font=f) for t, f, _ in parts]
            total = sum(ws) + 10 * (len(parts) - 1) + 24 + 92
            if total <= W - 60 or k < 0.5:
                break
            k -= 0.05
        x = (W - total) / 2
        for (t, f, col), w in zip(parts, ws):
            dr.text((x, cy + 30 - f.getmetrics()[0]), t, font=f, fill=col + (255,)); x += w + 10
        x += 14
        for k in range(2):
            px = x + k * 40
            dr.polygon([(px, cy - 34), (px + 22, cy - 34), (px + 50, cy), (px + 22, cy + 34), (px, cy + 34),
                        (px + 28, cy)], fill=(255, 255, 255, 255))

    def ticket(self, w=400, head_h=50, body_h=160):
        """Coupon in the KS 'SAVE UP TO $150' style: small bold header on orange, white perforated body where a
        heavy-italic discount numeral fills most of the height; optional small pre-word and a light note line."""
        t = self.offer["ticket"]
        im = Image.new("RGBA", (w, head_h + body_h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w, head_h + 12), 9, fill=self.colors["offer"] + (255,))
        d.rectangle((0, head_h, w, head_h + body_h), fill=(255, 255, 255, 255))
        r = 9   # semicircle bites along both body edges
        for y in range(head_h + 16, head_h + body_h - 8, 24):
            d.ellipse((-r, y - r, r, y + r), fill=(0, 0, 0, 0)); d.ellipse((w - r, y - r, w + r, y + r), fill=(0, 0, 0, 0))
        # header: bold, compact, slightly tracked; ASCII headers are set in caps
        head = t["head"].upper() if t["head"].isascii() else t["head"]
        hs, sp = 30, 2
        def hw(sz):
            f = self.font("bold", sz); return sum(d.textlength(ch, font=f) + sp for ch in head) - sp
        while hw(hs) > w - 40 and hs > 16:
            hs -= 1
        fh = self.font("bold", hs); x = (w - hw(hs)) / 2
        hy = (head_h - hs) / 2 - hs * 0.12
        for ch in head:
            d.text((x, hy), ch, font=fh, fill=(255, 255, 255, 255)); x += d.textlength(ch, font=fh) + sp
        # body: [pre] BIG [post] on one baseline — heavy italic for Latin/digits, bold gothic for CJK words
        note = t.get("note", "")
        avail_h = body_h - (40 if note else 14)
        big_sz = int(avail_h * 0.95)
        pre, post = t.get("pre", ""), t.get("post", "")
        def fnt(txt, sz):
            return self.font("heavy" if txt.isascii() else "bold", sz)
        while True:
            parts = [(pre, fnt(pre, int(big_sz * 0.36))), (t["big"], fnt(t["big"], big_sz)),
                     (post, fnt(post, int(big_sz * 0.42)))]
            parts = [p for p in parts if p[0]]
            ws = [d.textlength(s_, font=f) for s_, f in parts]
            if sum(ws) + 6 * (len(parts) - 1) <= w - 40 or big_sz < 30:
                break
            big_sz -= 2
        asc_big = self.font("heavy", big_sz).getmetrics()[0]
        base_y = head_h + 8 + (avail_h + asc_big * 0.78) / 2      # optical centre of cap height
        x = (w - sum(ws) - 6 * (len(parts) - 1)) / 2
        cap = asc_big * 0.72
        for (s_, f), wd in zip(parts, ws):
            y = base_y - f.getmetrics()[0]
            if s_ in ("$", "€", "£", "¥", "US$", "NT$", "HK$"):   # currency sits raised and tight, like "$150"
                y = base_y - cap - f.getmetrics()[0] * 0.18
            d.text((x, y), s_, font=f, fill=(17, 17, 17, 255)); x += wd + (1 if s_ in ("$", "€", "£", "¥") else 6)
        if note:
            ns = 24
            while d.textlength(note, font=self.font("regular", ns)) > w - 36 and ns > 14:
                ns -= 1
            fn = self.font("regular", ns)
            d.text(((w - d.textlength(note, font=fn)) / 2, head_h + body_h - ns - 12), note, font=fn, fill=(110, 110, 110, 255))
        return im
