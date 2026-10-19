# Layout styles

All overlays are drawn on 1080×1920 (9:16) or 1920×1080 (16:9) and scaled to the video. Coordinates below are
in those canvases.

| style | source | use when | file prefix (naming) |
|---|---|---|---|
| `grey` | TVC cut to 9:16 (full-bleed crop) | "滤镜用灰度高的", Halliday-like soft JP look | `naming.grey` |
| `frame` (tvc) | TVC cut to 9:16 | KS "Live Now"-like frame wanted | `naming.frame` |
| `band` | client 9:16 (16:9 picture on blurred bands) or 16:9 | client-finished edits, overlays only | `naming.overlay` |
| `frame` (overlay) | client 9:16 | same frame on client videos | `naming.overlay_frame` |

## grey (TVC)
- Grade: `eq=saturation=0.5:contrast=0.85:brightness=0.04:gamma=1.05,curves=all='0/0.09 0.5/0.54 1/0.93',...`
  (override with `grade` in project.json).
- Card: Mincho headline 62 px at y=1220 (centre), sub 32 px, optional badge under it. Card `y` up to 1480 when
  the footage has its own text at ~y 1300 (e.g. TVC "Insufficient knee bend" label).
- `offer: true` card → orange tag at y=760. End (logo tail): CTA bar y=1530 + cta_sub + badge y=1740.

## frame (bottom band)
- Top gradient + white brand logo (250 px) at (50, 70).
- Navy band y 1670–1920: x=430 「band_line1」, then white pill with official logo (h 60) + 「band_line2」 in yellow.
- Product cut-out h=470 at x=40 bursting above the band; ticket (400×210) right, 24 px above the band.
- TVC: copy cards y=1000; end = `cta_sub_lines` in Mincho 56 at y=1080.
- Client 9:16: copy in the upper blurred band (y≈300) with a wash 250–600; end = `cta_sub_lines` at y=330.

### Discount ticket spec (matches the KS reference ad "SAVE UP TO $150"; `draw.Kit.ticket`)
- 400×210: orange header 50 px (top corners r=9) + white body 160 px with semicircle bites (r=9, every 24 px)
  down both edges.
- Header: bold (`fonts.bold`), ~30 px, tracked +2, ASCII set in CAPS ("SAVE UP TO", "EARLY BIRD"), white.
- Body: ONE line, discount numeral in **heavy italic** (`fonts.heavy` = Avenir Next Heavy Italic) sized to fill
  ~95 % of the free body height; `pre`/`post` at ~36 % / ~42 % of it (heavy italic for Latin, bold gothic for
  CJK like 「最大」「最低」「折」). Currency (`$ € £ ¥ NT$`) is small, raised to cap height and tight to the digits.
  Near-black #111.
- Optional `note` (one short line, regular 24 px, grey #6E6E6E) at the bottom — the reference has none; use it
  only when the client asks for a 3rd line (Makuake job did: 「お得な情報をお届け」).
- Everything auto-shrinks to fit; never let the numeral touch the bites.

## band (client videos)
9:16 (picture ≈ y 637–1245):
- Upper band, whole video until `end`: badge y=215 + `top_tag_lines` tag at y=405 (size 48).
  From `end`: badge + `brand.title` (Mincho 60, y=315) + white brand logo (skip with `end_title_logo:false` if the
  footage's own end card shows the logo).
- Lower band: copy Mincho 60 at y=1295; product cut-out h=360 at x=36, bottom 1890; end CTA bar y=1340.
16:9:
- Copy top-left (x=90, y=70) with dark wash; `"side":"right"` puts it right-aligned at y=250 (under the tag).
- Offer tag top-right (1560, 130) whole video; product bottom-left (`h_opts.px`, `ph`, default 30/300).
- End: CTA bar from `bar_x` (default 340, right of the product) at `bar_y` (840); `text_above` puts cta_sub
  above the bar (use when the bar sits at the bottom edge).

## Mocking a layout
`render.py project.json stills` writes every PNG to `work/cards/`. Composite on a real frame:
`ffmpeg -ss T -i SRC -i card.png -filter_complex "[1]scale=W:H[o];[0][o]overlay,scale=540:-2" -frames:v 1 mock.jpg`
and Read the result before rendering.
